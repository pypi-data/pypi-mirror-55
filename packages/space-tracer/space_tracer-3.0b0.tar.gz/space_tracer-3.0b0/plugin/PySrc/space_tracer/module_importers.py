import inspect
import io
import os
import sys
import types
from ast import parse
from importlib import import_module
from base64 import standard_b64encode

try:
    from importlib.abc import MetaPathFinder, Loader
    from importlib.machinery import ModuleSpec
    from importlib.util import find_spec
    imp = None
except ImportError:
    # Stub out the classes for older versions of Python.
    class MetaPathFinder(object):
        pass

    Loader = ModuleSpec = object
    find_spec = None
    import imp
try:
    builtins = import_module('__builtin__')
except ImportError:
    import builtins

from .code_tracer import trace_source_tree, CONTEXT_NAME
from .mock_turtle import MockTurtle, monkey_patch_pyglet
from .traced_finder import DEFAULT_MODULE_NAME, LIVE_MODULE_NAME, \
    PSEUDO_FILENAME, TracedFinder


class DelegatingModuleFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target):
        for finder in self.following_finders:
            finder_find_spec = getattr(finder, 'find_spec', None)
            if finder_find_spec:
                spec = finder_find_spec(fullname, path, target)
                if spec is not None:
                    return spec

    # find_module() and load_module() are used in Python 2.
    def find_module(self, fullname, path):
        for finder in self.following_finders:
            loader = finder.find_module(fullname, path)
            if loader is not None:
                return loader

    @property
    def following_finders(self):
        is_after = False
        for finder in sys.meta_path:
            if not is_after:
                is_after = finder is self
                continue
            yield finder


# noinspection PyAbstractClass
class TracedModuleImporter(DelegatingModuleFinder, Loader):
    def __init__(self,
                 traced,
                 traced_file,
                 driver,
                 is_module,
                 is_live,
                 report_builder):
        """ Import the code that has been instrumented for live coding.

        :param traced_file: name of the file to replace with source code from
            stdin, or None if all source code comes from files
        :param str driver: command-line arguments for the driver script
        :param bool is_module: True if the driver is a module, not a script
        :param bool is_live: True if in live coding mode
        :param ReportBuilder report_builder: to record events when the code
            runs.
        """
        self.traced = traced
        self.environment = {CONTEXT_NAME: report_builder}
        self.traced_file = traced_file
        self.source_code = traced_file and sys.stdin.read()
        self.driver = driver
        self.driver_module = driver[0] if is_module else None
        self.is_module = is_module
        self.is_live = is_live
        self.source_finder = None
        self.driver_finder = None
        self.report_builder = report_builder
        if self.traced is not None and self.traced == self.driver_module:
            self.traced = LIVE_MODULE_NAME if is_live else DEFAULT_MODULE_NAME

    def find_spec(self, fullname, path, target=None):
        spec = super(TracedModuleImporter, self).find_spec(fullname,
                                                           path,
                                                           target)
        if spec is not None:
            if spec.origin == self.traced_file:
                self.record_module(fullname)
                return ModuleSpec(fullname, self, origin=self.traced_file)
            if self.traced_file is None and self.traced.startswith(fullname):
                return ModuleSpec(fullname, self, origin=spec.origin)

        if fullname == self.traced:
            return ModuleSpec(fullname, self, origin=self.traced_file)
        return None

    def record_module(self, module_name):
        """ Record the module that was traced. """
        if self.traced is None:
            if module_name != self.driver_module:
                self.traced = module_name
            elif self.is_live:
                self.traced = LIVE_MODULE_NAME
            else:
                self.traced = DEFAULT_MODULE_NAME

    def exec_module(self, module):
        module_spec = getattr(module, '__spec__', None)
        if module_spec:
            module_file = module_spec.origin
        else:
            module_file = self.traced_file
        parsed_filename = module_file
        if (self.traced.startswith(DEFAULT_MODULE_NAME) or
                self.traced.startswith(LIVE_MODULE_NAME)):
            source_code = self.source_code
            parsed_filename = PSEUDO_FILENAME
        elif self.traced_file is not None and module_file == self.traced_file:
            if self.source_code is None:
                with open(self.traced_file) as source_file:
                    self.source_code = source_file.read()
            source_code = self.source_code
        else:
            with open(module_file) as source_file:
                source_code = source_file.read()
        module_name = module.__name__
        is_module_traced = False
        source_tree = None
        if self.traced == module_name:
            is_module_traced = True
            self.source_finder = TracedFinder(source_code, '', parsed_filename)
        else:
            if self.traced.startswith(module_name):
                traced_child = self.traced[len(module_name)+1:]
            elif self.traced in (DEFAULT_MODULE_NAME, LIVE_MODULE_NAME):
                traced_child = self.traced
            else:
                traced_child = None
            if traced_child:
                source_finder = TracedFinder(source_code,
                                             traced_child,
                                             parsed_filename)
                source_tree = source_finder.source_tree
                if source_finder.traced_node is not None:
                    is_module_traced = True
                    self.source_finder = source_finder
        if source_tree is None:
            source_tree = parse(source_code, parsed_filename)
        if is_module_traced:
            source_tree = trace_source_tree(source_tree)
        if (module_name in (DEFAULT_MODULE_NAME, LIVE_MODULE_NAME) and
                self.driver_module):
            target_module = self.driver_module
        else:
            target_module = module_name
        if '.' in target_module:
            package_name, child_name = target_module.rsplit('.', 1)
        else:
            package_name = None
        module.__package__ = package_name
        module.__file__ = module_file
        module.__builtins__ = builtins
        module.__dict__.update(self.environment)
        self.environment = module.__dict__
        # from ast import dump
        # print(dump(source_tree, include_attributes=True))
        compiled_code = compile(source_tree, PSEUDO_FILENAME, 'exec')

        exec(compiled_code, self.environment)

    # find_module() and load_module() are used in Python 2.
    def find_module(self, fullname, path=None):
        if (fullname == self.traced or
                fullname in (DEFAULT_MODULE_NAME, LIVE_MODULE_NAME) and
                self.traced.startswith(fullname)):
            return self

    def load_module(self, fullname):
        # noinspection PyDeprecation
        new_mod = imp.new_module(fullname)
        sys.modules[fullname] = new_mod

        self.exec_module(new_mod)
        return new_mod

    def run_main(self):
        if self.driver_module is None:
            self.run_python_file(
                self.driver and self.driver[0],
                source_code=(self.source_code
                             if (not self.driver or
                                 self.traced_file == self.driver[0])
                             else None))
        else:
            self.run_python_module(self.driver_module)

    def run_python_module(self, modulename):
        """ Run a python module, as though with ``python -m name args...``.

        :param str modulename: the name of the module, possibly dot separated.

        This is based on code from coverage.py, by Ned Batchelder.
        https://bitbucket.org/ned/coveragepy
        """
        if find_spec:
            spec = find_spec(modulename)
            if spec is not None:
                pathname = spec.origin
                packagename = spec.name
            elif (self.traced in (DEFAULT_MODULE_NAME,
                                  LIVE_MODULE_NAME) and
                  self.source_code):
                pathname = self.traced_file
                packagename = self.driver_module
            else:
                raise ImportError(modulename)
            if pathname.endswith("__init__.py") and not modulename.endswith("__init__"):
                mod_main = modulename + ".__main__"
                spec = find_spec(mod_main)
                if not spec:
                    raise ImportError(
                        "No module named %s; "
                        "%r is a package and cannot be directly executed"
                        % (mod_main, modulename))
                pathname = spec.origin
                packagename = spec.name
            packagename = packagename.rpartition(".")[0]
        else:
            openfile = None
            glo, loc = globals(), locals()
            try:
                # Search for the module - inside its parent package, if any -
                # using standard import mechanics.
                try:
                    if '.' in modulename:
                        packagename, name = modulename.rsplit('.', 1)
                        package = __import__(packagename, glo, loc, ['__path__'])
                        searchpath = package.__path__
                    else:
                        packagename, name = None, modulename
                        searchpath = None  # "top-level search" in imp.find_module()
                    # noinspection PyDeprecation
                    openfile, pathname, _ = imp.find_module(name, searchpath)

                    # If `modulename` is actually a package, not a mere module,
                    # then we pretend to be Python 2.7 and try running its
                    # __main__.py script.
                    if openfile is None:
                        packagename = modulename
                        name = '__main__'
                        package = __import__(packagename, glo, loc, ['__path__'])
                        searchpath = package.__path__
                        # noinspection PyDeprecation
                        openfile, pathname, _ = imp.find_module(name, searchpath)
                    if pathname == self.traced_file:
                        self.record_module(modulename)
                except ImportError:
                    if (self.traced in (DEFAULT_MODULE_NAME,
                                        LIVE_MODULE_NAME) and
                            self.source_code):
                        pathname = self.traced_file
                        packagename = self.driver_module
                        packagename = packagename.rpartition(".")[0]
                    else:
                        raise
            finally:
                if openfile:
                    openfile.close()

        # Finally, hand the file off to run_python_file for execution.
        pathname = os.path.abspath(pathname)
        self.run_python_file(pathname, package=packagename)

    def run_python_file(self, filename, package=None, source_code=None):
        """Run a python file as if it were the main program on the command line.

        :param str filename: the path to the file to execute.
        :param str package: the package name to set on the module.
        :param str source_code: custom source code to replace the file contents.
        """
        call_stack_files = [frame[0].f_code.co_filename
                            for frame in inspect.stack()]
        top_file = call_stack_files[-1]
        if os.path.basename(top_file) == 'runpy.py':
            # Exclude runpy.py, used for python -m.
            call_stack_files = [
                frame_filename
                for frame_filename in call_stack_files
                if os.path.basename(frame_filename) != 'runpy.py']
            top_file = os.path.dirname(call_stack_files[-1])
        expected_path0 = os.path.abspath(os.path.dirname(top_file))
        # Check that sys.path is as expected, otherwise leave it alone.
        if os.path.abspath(sys.path[0]) == expected_path0:
            # Set sys.path to target script's folder instead of space_tracer.
            sys.path[0] = os.path.abspath(os.path.dirname(filename))

        # Create a module to serve as __main__
        module_name = (LIVE_MODULE_NAME
                       if self.traced == LIVE_MODULE_NAME
                       else DEFAULT_MODULE_NAME)
        main_mod = types.ModuleType(module_name)
        sys.modules[module_name] = main_mod
        main_mod.__file__ = filename
        main_mod.__builtins__ = builtins
        if package:
            main_mod.__package__ = package

        code = self.make_code_from_py(filename, source_code)

        if self.driver_finder.is_tracing:
            main_mod.__dict__.update(self.environment)
            self.environment = main_mod.__dict__
        # Execute the code object.
        exec(code, main_mod.__dict__)

    def make_code_from_py(self, filename, source):
        """Get source from `filename` and make a code object of it."""
        traced = self.traced
        if source is None:
            if (self.traced_file is not None and
                    (os.path.abspath(self.traced_file) ==
                     os.path.abspath(filename)) and
                    self.source_code is not None):
                source = self.source_code
                traced = self.traced or DEFAULT_MODULE_NAME
            else:
                with open(filename, 'rU') as f:
                    source = f.read()

        if traced:
            if traced.startswith(DEFAULT_MODULE_NAME):
                traced = traced[len(DEFAULT_MODULE_NAME)+1:]
            elif traced.startswith(LIVE_MODULE_NAME):
                traced = traced[len(LIVE_MODULE_NAME)+1:]
            parsed_file = PSEUDO_FILENAME if traced == '' else filename
            self.driver_finder = TracedFinder(source,
                                              traced,
                                              parsed_file)
            to_compile = self.driver_finder.source_tree
            if (traced == '' or
                    self.driver_finder.traced_node is not None):
                to_compile = trace_source_tree(to_compile)
                self.driver_finder.is_tracing = True
        else:
            self.driver_finder = TracedFinder(source, '', PSEUDO_FILENAME)
            to_compile = self.driver_finder.source_tree
        code = compile(to_compile, filename or PSEUDO_FILENAME, "exec")

        return code


class PatchedModuleFinder(DelegatingModuleFinder):
    is_desperate = False

    def __init__(self, is_zoomed):
        self.is_zoomed = is_zoomed

    def find_spec(self, fullname, path, target=None):
        if fullname not in ('matplotlib',
                            'matplotlib.pyplot',
                            'numpy.random',
                            'random',
                            'pyglet'):
            return None
        spec = super(PatchedModuleFinder, self).find_spec(fullname, path, target)
        if spec is not None:
            spec.loader = PatchedModuleLoader(fullname,
                                              spec.loader,
                                              self.is_zoomed)
            return spec

    # find_module() and load_module() are used in Python 2.
    def find_module(self, fullname, path=None):
        if fullname not in ('matplotlib',
                            'matplotlib.pyplot',
                            'numpy.random',
                            'random',
                            'pyglet'):
            return None
        loader = super(PatchedModuleFinder, self).find_module(fullname, path)
        if loader is not None:
            return PatchedModuleLoader(fullname, loader, self.is_zoomed)
        if sys.version_info < (3, 0) and not PatchedModuleFinder.is_desperate:
            # Didn't find anyone to load the module, get desperate.
            PatchedModuleFinder.is_desperate = True
            return PatchedModuleLoader(fullname, None, self.is_zoomed)


# noinspection PyAbstractClass
class PatchedModuleLoader(Loader):
    def __init__(self, fullname, main_loader, is_zoomed):
        self.fullname = fullname
        self.main_loader = main_loader
        self.is_zoomed = is_zoomed
        self.plt = None

    def exec_module(self, module):
        if self.main_loader is not None:
            self.main_loader.exec_module(module)
        if self.fullname in ('numpy.random', 'random'):
            module.seed(0)
        elif self.fullname == 'matplotlib':
            module.use('Agg')
        elif self.fullname == 'matplotlib.pyplot':
            self.plt = module
            # noinspection PyProtectedMember
            turtle_screen = MockTurtle._screen
            screen_width = turtle_screen.cv.cget('width')
            screen_height = turtle_screen.cv.cget('height')
            module.show = self.mock_show
            module.live_coding_size = (screen_width, screen_height)
            module.live_coding_zoom = self.live_coding_zoom
            if self.is_zoomed:
                self.live_coding_zoom()
        elif self.fullname == 'pyglet':
            # noinspection PyProtectedMember
            monkey_patch_pyglet(MockTurtle._screen.cv)

    def load_module(self, fullname):
        if self.main_loader is not None:
            module = self.main_loader.load_module(fullname)
        else:
            module = import_module(fullname)
            PatchedModuleFinder.is_desperate = False
        self.exec_module(module)
        return module

    def mock_show(self, *_args, **_kwargs):
        figure = self.plt.gcf()
        # noinspection PyProtectedMember
        turtle_screen = MockTurtle._screen
        screen_width = turtle_screen.cv.cget('width')
        screen_height = turtle_screen.cv.cget('height')
        figure_width = figure.get_figwidth()*figure.dpi
        figure_height = figure.get_figheight()*figure.dpi
        if figure_width < screen_width:
            x = (screen_width - figure_width) // 2
        else:
            x = 0
        if figure_height < screen_height:
            y = (screen_height - figure_height) // 2
        else:
            y = 0
        # noinspection PyUnresolvedReferences
        data = io.BytesIO()
        self.plt.savefig(data, format='PNG')

        image = data.getvalue()
        encoded = standard_b64encode(image)
        image_text = str(encoded.decode('UTF-8'))
        MockTurtle.display_image(x, y, image=image_text)

    def live_coding_zoom(self):
        screen_width, screen_height = self.plt.live_coding_size
        fig = self.plt.gcf()
        fig_width, fig_height = fig.get_figwidth(), fig.get_figheight()
        x_dpi = screen_width/fig_width
        y_dpi = screen_height/fig_height
        fig.dpi = min(x_dpi, y_dpi)
