#
# Copyright (c) 2009- Spyder Kernels Contributors
#
# Licensed under the terms of the MIT License
# (see spyder_kernels/__init__.py for details)
# -----------------------------------------------------------------------------
#
# IMPORTANT NOTE: Don't add a coding line here! It's not necessary for
# site files
#
# Spyder consoles sitecustomize
#

import bdb
from distutils.version import LooseVersion
import io
import os
import os.path as osp
import pdb
import re
import shlex
import sys
import sysconfig
import time
import warnings
import logging
import traceback

from IPython.core.getipython import get_ipython

from spyder_kernels.py3compat import TimeoutError, PY2
from spyder_kernels.comms import CommError
from spyder_kernels.customize.namespace_manager import NamespaceManager

if not PY2:
    from IPython.core.inputtransformer2 import TransformerManager
else:
    from IPython.core.inputsplitter import IPythonInputSplitter as TransformerManager


logger = logging.getLogger(__name__)



#==============================================================================
# sys.argv can be missing when Python is embedded, taking care of it.
# Fixes Issue 1473 and other crazy crashes with IPython 0.13 trying to
# access it.
#==============================================================================
if not hasattr(sys, 'argv'):
    sys.argv = ['']


#==============================================================================
# Main constants
#==============================================================================
IS_EXT_INTERPRETER = os.environ.get('SPY_EXTERNAL_INTERPRETER') == "True"
HIDE_CMD_WINDOWS = os.environ.get('SPY_HIDE_CMD') == "True"

#==============================================================================
# Important Note:
#
# We avoid importing spyder here, so we are handling Python 3 compatiblity
# by hand.
#==============================================================================
def _print(*objects, **options):
    end = options.get('end', '\n')
    file = options.get('file', sys.stdout)
    sep = options.get('sep', ' ')
    string = sep.join([str(obj) for obj in objects])
    if not PY2:
        # Python 3
        local_dict = {}
        exec('printf = print', local_dict) # to avoid syntax error in Python 2
        local_dict['printf'](string, file=file, end=end, sep=sep)
    else:
        # Python 2
        if end:
            print >>file, string
        else:
            print >>file, string,


#==============================================================================
# Execfile functions
#
# The definitions for Python 2 on Windows were taken from the IPython project
# Copyright (C) The IPython Development Team
# Distributed under the terms of the modified BSD license
#==============================================================================
try:
    # Python 2
    import __builtin__ as builtins
    if os.name == 'nt':
        def encode(u):
            return u.encode('utf8', 'replace')

    else:
        def encode(u):
            return u.encode(sys.getfilesystemencoding())

except ImportError:
    # Python 3
    import builtins
    basestring = (str,)


#==============================================================================
# Setting console encoding (otherwise Python does not recognize encoding)
# for Windows platforms
#==============================================================================
if os.name == 'nt' and PY2:
    try:
        import locale, ctypes
        _t, _cp = locale.getdefaultlocale('LANG')
        try:
            _cp = int(_cp[2:])
            ctypes.windll.kernel32.SetConsoleCP(_cp)
            ctypes.windll.kernel32.SetConsoleOutputCP(_cp)
        except (ValueError, TypeError):
            # Code page number in locale is not valid
            pass
    except:
        pass


#==============================================================================
# Prevent subprocess.Popen calls to create visible console windows on Windows.
# See issue #4932
#==============================================================================
if os.name == 'nt' and HIDE_CMD_WINDOWS:
    import subprocess
    creation_flag = 0x08000000  # CREATE_NO_WINDOW

    class SubprocessPopen(subprocess.Popen):
        def __init__(self, *args, **kwargs):
            kwargs['creationflags'] = creation_flag
            super(SubprocessPopen, self).__init__(*args, **kwargs)

    subprocess.Popen = SubprocessPopen

#==============================================================================
# Importing user's sitecustomize
#==============================================================================
try:
    import sitecustomize  #analysis:ignore
except:
    pass


#==============================================================================
# Add default filesystem encoding on Linux to avoid an error with
# Matplotlib 1.5 in Python 2 (Fixes Issue 2793)
#==============================================================================
if PY2 and sys.platform.startswith('linux'):
    def _getfilesystemencoding_wrapper():
        return 'utf-8'

    sys.getfilesystemencoding = _getfilesystemencoding_wrapper


#==============================================================================
# Set PyQt API to #2
#==============================================================================
if os.environ.get("QT_API") == 'pyqt':
    try:
        import sip
        for qtype in ('QString', 'QVariant', 'QDate', 'QDateTime',
                      'QTextStream', 'QTime', 'QUrl'):
            sip.setapi(qtype, 2)
    except:
        pass
else:
    try:
        os.environ.pop('QT_API')
    except KeyError:
        pass


#==============================================================================
# IPython kernel adjustments
#==============================================================================
# Use ipydb as the debugger to patch on IPython consoles
from IPython.core.debugger import Pdb as ipyPdb
pdb.Pdb = ipyPdb

# Patch unittest.main so that errors are printed directly in the console.
# See http://comments.gmane.org/gmane.comp.python.ipython.devel/10557
# Fixes Issue 1370
import unittest
from unittest import TestProgram
class IPyTesProgram(TestProgram):
    def __init__(self, *args, **kwargs):
        test_runner = unittest.TextTestRunner(stream=sys.stderr)
        kwargs['testRunner'] = kwargs.pop('testRunner', test_runner)
        kwargs['exit'] = False
        TestProgram.__init__(self, *args, **kwargs)
unittest.main = IPyTesProgram

# Ignore some IPython/ipykernel warnings
try:
    warnings.filterwarnings(action='ignore', category=DeprecationWarning,
                            module='ipykernel.ipkernel')
except:
    pass

#==============================================================================
# Turtle adjustments
#==============================================================================
# This is needed to prevent turtle scripts crashes after multiple runs in the
# same IPython Console instance.
# See Spyder issue #6278
try:
    import turtle
    from turtle import Screen, Terminator

    def spyder_bye():
        try:
            Screen().bye()
            turtle.TurtleScreen._RUNNING = True
        except Terminator:
            pass
    turtle.bye = spyder_bye
except:
    pass


#==============================================================================
# Pandas adjustments
#==============================================================================
try:
    import pandas as pd

    # Set Pandas output encoding
    pd.options.display.encoding = 'utf-8'

    # Filter warning that appears for DataFrames with np.nan values
    # Example:
    # >>> import pandas as pd, numpy as np
    # >>> pd.Series([np.nan,np.nan,np.nan],index=[1,2,3])
    # Fixes Issue 2991
    # For 0.18-
    warnings.filterwarnings(action='ignore', category=RuntimeWarning,
                            module='pandas.core.format',
                            message=".*invalid value encountered in.*")
    # For 0.18.1+
    warnings.filterwarnings(action='ignore', category=RuntimeWarning,
                            module='pandas.formats.format',
                            message=".*invalid value encountered in.*")
except:
    pass


# =============================================================================
# Numpy adjustments
# =============================================================================
try:
    # Filter warning that appears when users have 'Show max/min'
    # turned on and Numpy arrays contain a nan value.
    # Fixes Issue 7063
    # Note: It only happens in Numpy 1.14+
    warnings.filterwarnings(action='ignore', category=RuntimeWarning,
                            module='numpy.core._methods',
                            message=".*invalid value encountered in.*")
except:
    pass


# =============================================================================
# Multiprocessing adjustments
# =============================================================================
# This patch is only needed on Windows and Python 3
if os.name == 'nt' and not PY2:
    # This could fail with changes in Python itself, so we protect it
    # with a try/except
    try:
        import multiprocessing.spawn
        _old_preparation_data = multiprocessing.spawn.get_preparation_data

        def _patched_preparation_data(name):
            """
            Patched get_preparation_data to work when all variables are
            removed before execution.
            """
            try:
                return _old_preparation_data(name)
            except AttributeError:
                main_module = sys.modules['__main__']
                # Any string for __spec__ does the job
                main_module.__spec__ = ''
                return _old_preparation_data(name)

        multiprocessing.spawn.get_preparation_data = _patched_preparation_data
    except Exception:
        pass


#==============================================================================
# Pdb adjustments
#==============================================================================
class SpyderPdb(pdb.Pdb, object):  # Inherits `object` to call super() in PY2

    send_initial_notification = True
    starting = True

    def __init__(self, completekey='tab', stdin=None, stdout=None,
                 skip=None, nosigint=False):
        """Init Pdb."""
        # Only set to true when calling debugfile
        self.continue_if_has_breakpoints = False
        self.pdb_ignore_lib = False
        super(SpyderPdb, self).__init__()
        self._pdb_breaking = False

    # --- Methods overriden by us
    def set_continue(self):
        """
        Stop only at breakpoints or when finished.

        Reimplemented to avoid stepping out of debugging if there are no
        breakpoints. We could add more later.
        """
        # Don't stop except at breakpoints or when finished
        self._set_stopinfo(self.botframe, None, -1)

    def sigint_handler(self, signum, frame):
        """
        Handle a sigint signal. Break on the frame above this one.

        This method is not present in python2 so this won't be called there.
        """
        if self.allow_kbdint:
            raise KeyboardInterrupt
        self.message("\nProgram interrupted. (Use 'cont' to resume).")
        # avoid stopping in set_trace
        sys.settrace(None)
        self._pdb_breaking = True
        self.set_step()
        self.set_trace(sys._getframe())

    def preloop(self):
        """Ask Spyder for breakpoints before the first prompt is created."""
        try:
            _frontend_request(blocking=True).set_debug_state(True)
            pdb_settings = _frontend_request().get_pdb_settings()
            self.pdb_ignore_lib = pdb_settings['pdb_ignore_lib']
            if self.starting:
                self.set_spyder_breakpoints(pdb_settings['breakpoints'])

        except (CommError, TimeoutError):
            logger.debug("Could not get breakpoints from the frontend.")

    def postloop(self):
        """Notifies spyder that the loop has ended."""
        try:
            _frontend_request(blocking=True).set_debug_state(False)
        except (CommError, TimeoutError):
            logger.debug("Could not send debugging state to the frontend.")
        super(SpyderPdb, self).postloop()

    # --- Methods defined by us
    def set_spyder_breakpoints(self, breakpoints):
        self.clear_all_breaks()
        #------Really deleting all breakpoints:
        for bp in bdb.Breakpoint.bpbynumber:
            if bp:
                bp.deleteMe()
        bdb.Breakpoint.next = 1
        bdb.Breakpoint.bplist = {}
        bdb.Breakpoint.bpbynumber = [None]
        #------
        i = 0
        for fname, data in list(breakpoints.items()):
            for linenumber, condition in data:
                i += 1
                self.set_break(self.canonic(fname), linenumber,
                               cond=condition)

        # Jump to first breakpoint.
        # Fixes issue 2034
        if self.starting:
            # Only run this after a Pdb session is created
            self.starting = False

            # Get all breakpoints for the file we're going to debug
            frame = self.curframe
            if not frame:
                # We are not debugging, return. Solves #10290
                return
            lineno = frame.f_lineno
            breaks = self.get_file_breaks(frame.f_code.co_filename)

            # Do 'continue' if the first breakpoint is *not* placed
            # where the debugger is going to land.
            # Fixes issue 4681
            if (self.continue_if_has_breakpoints and
                    breaks and
                    lineno < breaks[0]):
                try:
                    get_ipython().kernel.pdb_continue()
                except (CommError, TimeoutError):
                    logger.debug(
                        "Could not send a Pdb continue call to the frontend.")

    def notify_spyder(self, frame):
        """Send kernel state to the frontend."""
        if not frame:
            return

        kernel = get_ipython().kernel

        # Get filename and line number of the current frame
        fname = self.canonic(frame.f_code.co_filename)
        if PY2:
            try:
                fname = unicode(fname, "utf-8")
            except TypeError:
                pass
        lineno = frame.f_lineno

        # Set step of the current frame (if any)
        step = {}
        if isinstance(fname, basestring) and isinstance(lineno, int):
            step = dict(fname=fname, lineno=lineno)

        # Publish Pdb state so we can update the Variable Explorer
        # and the Editor on the Spyder side
        kernel._pdb_step = step
        try:
            kernel.publish_pdb_state()
        except (CommError, TimeoutError):
            logger.debug("Could not send Pdb state to the frontend.")

    def user_return(self, frame, return_value):
        """This function is called when a return trap is set here."""
        # This is useful when debugging in an active interpreter (otherwise,
        # the debugger will stop before reaching the target file)
        if self._wait_for_mainpyfile:
            if (self.mainpyfile != self.canonic(frame.f_code.co_filename)
                    or frame.f_lineno <= 0):
                return
            self._wait_for_mainpyfile = 0
        super(SpyderPdb, self).user_return(frame, return_value)

    def default(self, line):
        """
        Default way of running pdb statment.

        The only difference with Pdb.default is that if line contains multiple
        statments, the code will be compiled with 'exec'. It will not print the
        result but will run without failing.
        """
        if line[:1] == '!':
            line = line[1:]
        line = TransformerManager().transform_cell(line)
        locals = self.curframe_locals
        globals = self.curframe.f_globals
        try:
            try:
                code = compile(line + '\n', '<stdin>', 'single')
            except SyntaxError:
                # support multiline statments
                code = compile(line + '\n', '<stdin>', 'exec')
            save_stdout = sys.stdout
            save_stdin = sys.stdin
            save_displayhook = sys.displayhook
            try:
                sys.stdin = self.stdin
                sys.stdout = self.stdout
                sys.displayhook = self.displayhook
                exec(code, globals, locals)
            finally:
                sys.stdout = save_stdout
                sys.stdin = save_stdin
                sys.displayhook = save_displayhook
        except:
            if PY2:
                t, v = sys.exc_info()[:2]
                if type(t) == type(''):
                    exc_type_name = t
                else: exc_type_name = t.__name__
                print >>self.stdout, '***', exc_type_name + ':', v
            else:
                exc_info = sys.exc_info()[:2]
                self.error(
                    traceback.format_exception_only(*exc_info)[-1].strip())

    def completenames(self, text, line, begidx, endidx):
        """
        Try to complete with command names, otherwise goes to default.
        """
        matched_names = super(SpyderPdb, self).completenames(
            text, line, begidx, endidx)
        matched_default = self.completedefault(text, line, begidx, endidx)
        return matched_names + matched_default

    def completedefault(self, text, line, begidx, endidx):
        """
        Default completion.
        """
        return self._complete_expression(text, line, begidx, endidx)

    def interaction(self, frame, traceback):
        if self._pdb_breaking:
            self._pdb_breaking = False
            if frame and frame.f_back:
                return self.interaction(frame.f_back, traceback)
        if (frame is not None
                and "spydercustomize.py" in frame.f_code.co_filename):
            self.onecmd('exit')
        else:
            self.setup(frame, traceback)
            if self.send_initial_notification:
                self.notify_spyder(frame)
            if get_ipython().kernel._pdb_print_code:
                self.print_stack_entry(self.stack[self.curindex])
            self._cmdloop()
            self.forget()

    def stop_here(self, frame):
        """Check if pdb should stop here."""
        if not super(SpyderPdb, self).stop_here(frame):
            return False
        filename = frame.f_code.co_filename
        if filename.startswith('<'):
            # This is not a file
            return True
        if self.pdb_ignore_lib and path_is_library(filename):
            return False
        return True

    def _cmdloop(self):
        while True:
            try:
                # keyboard interrupts allow for an easy way to cancel
                # the current command, so allow them during interactive input
                self.allow_kbdint = True
                self.cmdloop()
                self.allow_kbdint = False
                break
            except KeyboardInterrupt:
                _print("--KeyboardInterrupt--\n"
                       "For copying text while debugging, use Ctrl+Shift+C",
                       file=self.stdout)

    def reset(self):
        super(SpyderPdb, self).reset()
        kernel = get_ipython().kernel
        kernel._register_pdb_session(self)

    # XXX: notify spyder on any pdb command (is that good or too lazy?
    #     i.e. is more specific behaviour desired?)
    def postcmd(self, stop, line):
        if '!get_ipython().kernel' not in line:
            self.notify_spyder(self.curframe)
        return super(SpyderPdb, self).postcmd(stop, line)

    # Breakpoints don't work for files with non-ascii chars in Python 2
    # Fixes Issue 1484
    if PY2:
        def break_here(self, frame):
            from bdb import effective
            filename = self.canonic(frame.f_code.co_filename)
            try:
                filename = unicode(filename, "utf-8")
            except TypeError:
                pass
            if filename not in self.breaks:
                return False
            lineno = frame.f_lineno
            if lineno not in self.breaks[filename]:
                # The line itself has no breakpoint, but maybe the line is the
                # first line of a function with breakpoint set by function name
                lineno = frame.f_code.co_firstlineno
                if lineno not in self.breaks[filename]:
                    return False

            # flag says ok to delete temp. bp
            (bp, flag) = effective(filename, lineno, frame)
            if bp:
                self.currentbp = bp.number
                if (flag and bp.temporary):
                    self.do_clear(str(bp.number))
                return True
            else:
                return False


pdb.Pdb = SpyderPdb


def create_pathlist():
    """
    Create list of Python library paths to be skipped from module
    reloading and Pdb steps.
    """
    # Get standard installation paths
    try:
        paths = sysconfig.get_paths()
        standard_paths = [paths['stdlib'],
                          paths['purelib'],
                          paths['scripts'],
                          paths['data']]
    except Exception:
        standard_paths = []

    # Get user installation path
    # See spyder-ide/spyder#8776
    try:
        import site
        if getattr(site, 'getusersitepackages', False):
            # Virtualenvs don't have this function but
            # conda envs do
            user_path = [site.getusersitepackages()]
        elif getattr(site, 'USER_SITE', False):
            # However, it seems virtualenvs have this
            # constant
            user_path = [site.USER_SITE]
        else:
            user_path = []
    except Exception:
        user_path = []

    return standard_paths + user_path


def path_is_library(path, initial_pathlist=None):
    """Decide if a path is in user code or a library according to its path."""
    # Compute DEFAULT_PATHLIST only once and make it global to reuse it
    # in any future call of this function.
    if 'DEFAULT_PATHLIST' not in globals():
        global DEFAULT_PATHLIST
        DEFAULT_PATHLIST = create_pathlist()

    if initial_pathlist is None:
        initial_pathlist = []

    pathlist = initial_pathlist + DEFAULT_PATHLIST

    if path is None:
        # Path probably comes from a C module that is statically linked
        # into the interpreter. There is no way to know its path, so we
        # choose to ignore it.
        return True
    elif any([p in path for p in pathlist]):
        # We don't want to consider paths that belong to the standard
        # library or installed to site-packages.
        return True
    elif not os.name == 'nt':
        # Paths containing the strings below can be part of the default
        # Linux installation, Homebrew or the user site-packages in a
        # virtualenv.
        patterns = [
            r'^/usr/lib.*',
            r'^/usr/local/lib.*',
            r'^/usr/.*/dist-packages/.*',
            r'^/home/.*/.local/lib.*',
            r'^/Library/.*',
            r'^/Users/.*/Library/.*',
            r'^/Users/.*/.local/.*',
        ]

        if [p for p in patterns if re.search(p, path)]:
            return True
        else:
            return False
    else:
        return False


# =============================================================================
# User module reloader
# =============================================================================
class UserModuleReloader(object):
    """
    User Module Reloader (UMR) aims at deleting user modules
    to force Python to deeply reload them during import

    pathlist [list]: blacklist in terms of module path
    namelist [list]: blacklist in terms of module name
    """

    def __init__(self, namelist=None, pathlist=None):
        if namelist is None:
            namelist = []
        else:
            try:
                namelist = namelist.split(',')
            except Exception:
                namelist = []

        # Spyder modules
        spy_modules = ['spyder_kernels']

        # Matplotlib modules
        mpl_modules = ['matplotlib', 'tkinter', 'Tkinter']

        # Add other, necessary modules to the UMR blacklist
        # astropy: see issue 6962
        # pytorch: see issue 7041
        # fastmat: see issue 7190
        # pythoncom: see issue 7190
        # tensorflow: see issue 8697
        other_modules = ['pytorch', 'pythoncom', 'tensorflow']
        if PY2:
            py2_modules = ['astropy', 'fastmat']
            other_modules = other_modules + py2_modules
        self.namelist = namelist + spy_modules + mpl_modules + other_modules

        self.pathlist = pathlist

        # List of previously loaded modules
        self.previous_modules = list(sys.modules.keys())

        # List of module names to reload
        self.modnames_to_reload = []

        # Activate Cython support
        self.has_cython = False
        self.activate_cython()

        # Check if the UMR is enabled or not
        enabled = os.environ.get("SPY_UMR_ENABLED", "")
        self.enabled = enabled.lower() == "true"

        # Check if the UMR should print the list of reloaded modules or not
        verbose = os.environ.get("SPY_UMR_VERBOSE", "")
        self.verbose = verbose.lower() == "true"

    def is_module_reloadable(self, module, modname):
        """Decide if a module is reloadable or not."""
        if self.has_cython:
            # Don't return cached inline compiled .PYX files
            return False
        else:
            if (path_is_library(getattr(module, '__file__', None),
                                self.pathlist) or
                    self.is_module_in_namelist(modname)):
                return False
            else:
                return True

    def is_module_in_namelist(self, modname):
        """Decide if a module can be reloaded or not according to its name."""
        return set(modname.split('.')) & set(self.namelist)

    def activate_cython(self):
        """
        Activate Cython support.

        We need to run this here because if the support is
        active, we don't to run the UMR at all.
        """
        run_cython = os.environ.get("SPY_RUN_CYTHON") == "True"

        if run_cython:
            try:
                __import__('Cython')
                self.has_cython = True
            except Exception:
                pass

            if self.has_cython:
                # Import pyximport to enable Cython files support for
                # import statement
                import pyximport
                pyx_setup_args = {}

                # Add Numpy include dir to pyximport/distutils
                try:
                    import numpy
                    pyx_setup_args['include_dirs'] = numpy.get_include()
                except Exception:
                    pass

                # Setup pyximport and enable Cython files reload
                pyximport.install(setup_args=pyx_setup_args,
                                  reload_support=True)

    def run(self):
        """
        Delete user modules to force Python to deeply reload them

        Do not del modules which are considered as system modules, i.e.
        modules installed in subdirectories of Python interpreter's binary
        Do not del C modules
        """
        self.modnames_to_reload = []
        for modname, module in list(sys.modules.items()):
            if modname not in self.previous_modules:
                # Decide if a module can be reloaded or not
                if self.is_module_reloadable(module, modname):
                    self.modnames_to_reload.append(modname)
                    del sys.modules[modname]
                else:
                    continue

        # Report reloaded modules
        if self.verbose and self.modnames_to_reload:
            modnames = self.modnames_to_reload
            _print("\x1b[4;33m%s\x1b[24m%s\x1b[0m"\
                   % ("Reloaded modules", ": "+", ".join(modnames)))


__umr__ = UserModuleReloader(namelist=os.environ.get("SPY_UMR_NAMELIST",
                                                     None))


#==============================================================================
# Handle Post Mortem Debugging and Traceback Linkage to Spyder
#==============================================================================
def clear_post_mortem():
    """
    Remove the post mortem excepthook and replace with a standard one.
    """
    ipython_shell = get_ipython()
    ipython_shell.set_custom_exc((), None)


def post_mortem_excepthook(type, value, tb):
    """
    For post mortem exception handling, print a banner and enable post
    mortem debugging.
    """
    clear_post_mortem()
    ipython_shell = get_ipython()
    ipython_shell.showtraceback((type, value, tb))
    p = pdb.Pdb(ipython_shell.colors)

    if not type == SyntaxError:
        # wait for stderr to print (stderr.flush does not work in this case)
        time.sleep(0.1)
        _print('*' * 40)
        _print('Entering post mortem debugging...')
        _print('*' * 40)
        #  add ability to move between frames
        p.send_initial_notification = False
        p.reset()
        frame = tb.tb_frame
        prev = frame
        while frame.f_back:
            prev = frame
            frame = frame.f_back
        frame = prev
        # wait for stdout to print
        time.sleep(0.1)
        p.interaction(frame, tb)


def set_post_mortem():
    """
    Enable the post mortem debugging excepthook.
    """
    def ipython_post_mortem_debug(shell, etype, evalue, tb,
               tb_offset=None):
        post_mortem_excepthook(etype, evalue, tb)
    ipython_shell = get_ipython()
    ipython_shell.set_custom_exc((Exception,), ipython_post_mortem_debug)

# Add post mortem debugging if requested and in a dedicated interpreter
# existing interpreters use "runfile" below
if "SPYDER_EXCEPTHOOK" in os.environ:
    set_post_mortem()


# ==============================================================================
# runfile and debugfile commands
# ==============================================================================
def _frontend_request(blocking=True):
    """
    Send a request to the frontend.

    If blocking is true, The return value will be returned.
    """
    if not get_ipython().kernel.frontend_comm.is_open():
        raise CommError("Can't make a request to a closed comm")
    # Get a reply from the last frontend to have sent a message
    return get_ipython().kernel.frontend_call(
        blocking=blocking, broadcast=False)


def get_current_file_name():
    """Get the current file name."""
    try:
        return _frontend_request().current_filename()
    except Exception:
        _print("This command failed to be executed because an error occurred"
               " while trying to get the current file name from Spyder's"
               " editor. The error was:\n\n")
        get_ipython().showtraceback(exception_only=True)
        return None


def get_debugger(filename):
    """Get a debugger for a given filename."""
    debugger = pdb.Pdb()
    filename = debugger.canonic(filename)
    debugger._wait_for_mainpyfile = 1
    debugger.mainpyfile = filename
    debugger._user_requested_quit = 0
    if os.name == 'nt':
        filename = filename.replace('\\', '/')
    return debugger, filename


def exec_code(code, filename, namespace):
    """Execute code and display any exception."""
    if PY2 and isinstance(filename, unicode):
        filename = encode(filename)

    if PY2 and isinstance(code, unicode):
        code = encode(code)

    ipython_shell = get_ipython()
    is_ipython = os.path.splitext(filename)[1] == '.ipy'
    try:
        if is_ipython:
            # transform code
            tm = TransformerManager()
            if not PY2:
                # Avoid removing lines
                tm.cleanup_transforms = []
            code = tm.transform_cell(code)
        exec(compile(code, filename, 'exec'), namespace)
    except SystemExit as status:
        # ignore exit(0)
        if status.code:
            ipython_shell.showtraceback(exception_only=True)
    except BaseException as error:
        if (isinstance(error, bdb.BdbQuit)
                and ipython_shell.kernel._pdb_obj):
            # Ignore BdbQuit if we are debugging, as it is expected.
            ipython_shell.kernel._pdb_obj = None
        else:
            # We ignore the call to exec
            ipython_shell.showtraceback(tb_offset=1)


def get_file_code(filename):
    """Retrive the content of a file."""
    # Get code from spyder
    try:
        file_code = _frontend_request().get_file_code(filename)
    except (CommError, TimeoutError):
        file_code = None
    if file_code is None:
        with open(filename, 'r') as f:
            return f.read()
    return file_code


def runfile(filename=None, args=None, wdir=None, namespace=None,
            post_mortem=False, current_namespace=False):
    """
    Run filename
    args: command line arguments (string)
    wdir: working directory
    namespace: namespace for execution
    post_mortem: boolean, whether to enter post-mortem mode on error
    current_namespace: if true, run the file in the current namespace
    """
    ipython_shell = get_ipython()
    if filename is None:
        filename = get_current_file_name()
        if filename is None:
            return
    else:
        # get_debugger replaces \\ by / so we must undo that here
        # Otherwise code caching doesn't work
        if os.name == 'nt':
            filename = filename.replace('/', '\\')

    try:
        filename = filename.decode('utf-8')
    except (UnicodeError, TypeError, AttributeError):
        # UnicodeError, TypeError --> eventually raised in Python 2
        # AttributeError --> systematically raised in Python 3
        pass
    if PY2 and isinstance(filename, unicode):
        filename = encode(filename)
    if __umr__.enabled:
        __umr__.run()
    if args is not None and not isinstance(args, basestring):
        raise TypeError("expected a character buffer object")
    try:
        file_code = get_file_code(filename)
    except Exception:
        _print(
            "This command failed to be executed because an error occurred"
            " while trying to get the file code from Spyder's"
            " editor. The error was:\n\n")
        get_ipython().showtraceback(exception_only=True)
        return
    if file_code is None:
        _print("Could not get code from editor.\n")
        return

    with NamespaceManager(filename, namespace, current_namespace,
                          file_code=file_code) as namespace:
        sys.argv = [filename]
        if args is not None:
            for arg in shlex.split(args):
                sys.argv.append(arg)
        if wdir is not None:
            try:
                wdir = wdir.decode('utf-8')
            except (UnicodeError, TypeError, AttributeError):
                # UnicodeError, TypeError --> eventually raised in Python 2
                # AttributeError --> systematically raised in Python 3
                pass
            if os.path.isdir(wdir):
                os.chdir(wdir)
            else:
                _print("Working directory {} doesn't exist.\n".format(wdir))
        if post_mortem:
            set_post_mortem()

        if __umr__.has_cython:
            # Cython files
            with io.open(filename, encoding='utf-8') as f:
                ipython_shell.run_cell_magic('cython', '', f.read())
        else:
            exec_code(file_code, filename, namespace)

        clear_post_mortem()
        sys.argv = ['']


builtins.runfile = runfile


def debugfile(filename=None, args=None, wdir=None, post_mortem=False,
              current_namespace=False):
    """
    Debug filename
    args: command line arguments (string)
    wdir: working directory
    post_mortem: boolean, included for compatiblity with runfile
    """
    if filename is None:
        filename = get_current_file_name()
        if filename is None:
            return
    debugger, filename = get_debugger(filename)
    debugger.continue_if_has_breakpoints = True
    debugger.run("runfile(%r, args=%r, wdir=%r, current_namespace=%r)" % (
        filename, args, wdir, current_namespace))


builtins.debugfile = debugfile


def runcell(cellname, filename=None):
    """
    Run a code cell from an editor as a file.

    Currently looks for code in an `ipython` property called `cell_code`.
    This property must be set by the editor prior to calling this function.
    This function deletes the contents of `cell_code` upon completion.

    Parameters
    ----------
    cellname : str or int
        Cell name or index.
    filename : str
        Needed to allow for proper traceback links.
    """
    if filename is None:
        filename = get_current_file_name()
        if filename is None:
            return
    else:
        # get_debugger replaces \\ by / so we must undo that here
        # Otherwise code caching doesn't work
        if os.name == 'nt':
            filename = filename.replace('/', '\\')
    try:
        filename = filename.decode('utf-8')
    except (UnicodeError, TypeError, AttributeError):
        # UnicodeError, TypeError --> eventually raised in Python 2
        # AttributeError --> systematically raised in Python 3
        pass
    ipython_shell = get_ipython()
    try:
        # Get code from spyder
        cell_code = _frontend_request().run_cell(cellname, filename)
    except Exception:
        _print("This command failed to be executed because an error occurred"
               " while trying to get the cell code from Spyder's"
               " editor. The error was:\n\n")
        get_ipython().showtraceback(exception_only=True)
        return

    if not cell_code or cell_code.strip() == '':
        _print("Nothing to execute, this cell is empty.\n")
        return

    # Trigger `post_execute` to exit the additional pre-execution.
    # See Spyder PR #7310.
    ipython_shell.events.trigger('post_execute')
    try:
        file_code = get_file_code(filename)
    except Exception:
        file_code = None
    with NamespaceManager(filename, current_namespace=True,
                          file_code=file_code) as namespace:
        exec_code(cell_code, filename, namespace)


builtins.runcell = runcell


def debugcell(cellname, filename=None):
    """Debug a cell."""
    if filename is None:
        filename = get_current_file_name()
        if filename is None:
            return

    debugger, filename = get_debugger(filename)
    # The breakpoint might not be in the cell
    debugger.continue_if_has_breakpoints = False
    debugger.run("runcell({}, {})".format(
        repr(cellname), repr(filename)))


builtins.debugcell = debugcell


def cell_count(filename=None):
    """
    Get the number of cells in a file.

    Parameters
    ----------
    filename : str
        The file to get the cells from. If None, the currently opened file.
    """
    if filename is None:
        filename = get_current_file_name()
        if filename is None:
            raise RuntimeError('Could not get cell count from frontend.')
    try:
        # Get code from spyder
        cell_count = _frontend_request().cell_count(filename)
        return cell_count
    except Exception:
        etype, error, tb = sys.exc_info()
        raise etype(error)


builtins.cell_count = cell_count


#==============================================================================
# Restoring original PYTHONPATH
#==============================================================================
try:
    os.environ['PYTHONPATH'] = os.environ['OLD_PYTHONPATH']
    del os.environ['OLD_PYTHONPATH']
except KeyError:
    pass
