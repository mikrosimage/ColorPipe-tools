""" Debug helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import os
import argparse
import sys


def get_imported_modules_versions(modules, glob):
    """Return a string containing imported modules versions.
    (It isn't intended to be exhautive)

    Args:
        modules: sys.modules
        glob: globals()

    Returns:
        .string

    """
    # Retrieve ColorPipe-tools modules
    path = os.path.dirname(os.path.dirname(__file__))
    res = "ColorPipe-tools modules:\n-----------------------------"
    for name in modules:
        if (path in str(modules[name])
           and "debug_helper" not in str(modules[name])):
            try:
                res = "{0}\n{1} - version {2}".format(res, name,
                                                      modules[name].__version__
                                                      )
            except AttributeError:
                pass
    # Retrieve "interesting" external modules
    module_selection = set(modules) & set(glob)
    res = "{0}\n\nExternal modules:\n-----------------------------".format(res)
    for name in module_selection:
        if "built-in" not in name and path not in str(modules[name]):
            try:
                res = "{0}\n{1} - version {2}".format(res, name,
                                                      modules[name].__version__
                                                      )
            except AttributeError:
                pass
    return res


def make_full_version_action(version_text):
    """Return a multi-lines version action for argparse

    Args:
        version_text (str): version text to print

    Returns:
        .argparse.Action

    """
    class FullVersionAction(argparse.Action):
        """Argparse action that enable multi-line version

        """
        def __init__(self, option_strings, dest=None, nargs=0, default=None,
                     required=False, typ=None, metavar=None,
                     help_str=("show version number of the program and its "
                               "dependencies. And then exit")):
            super(FullVersionAction, self).__init__(
                option_strings=option_strings,
                dest=dest, nargs=nargs, default=default, required=required,
                metavar=metavar, type=typ, help=help_str)

        def __call__(self, parser, namespace, values, option_string=None):
            print version_text
            sys.exit()
    return FullVersionAction
