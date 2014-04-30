""" Color Log.
    Clint module required.

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
IS_CLINT = True
try:
    from clint.textui import colored
except ImportError:
    IS_CLINT = False


def disable_color():
    """ Disable all colors

    """
    if IS_CLINT:
        colored.disable()


def __get_message(prefix, message, color_function):
    """ Print colored message if possible

    Args:
        prefix (str): will be prepend to message

        message (str): message to display

        color_function (colored function): red, green, yellow, blue, black,
        magenta, cyan or white.

    """
    message = "{0} {1}".format(prefix, message)
    if IS_CLINT:
        return color_function(message)
    else:
        return message


def get_error_message(message):
    """ Get error message

    Args:
        message (str): message to display

    """
    if IS_CLINT:
        func = colored.red
    else:
        func = None
    return __get_message("Error:", message, func)


def get_warning_message(message):
    """ Get warning message

    Args:
        message (str): message to display

    """
    if IS_CLINT:
        func = colored.yellow
    else:
        func = None
    return __get_message("Warning:", message, func)


def get_success_message(message):
    """ Get warning message

    Args:
        message (str): message to display

    """
    if IS_CLINT:
        func = colored.green
    else:
        func = None
    return __get_message("Success:", message, func)


def print_error_message(message):
    """ Print error message

    Args:
        message (str): message to display

    """
    print get_error_message(message)


def print_warning_message(message):
    """ Print warning message

    Args:
        message (str): message to display

    """
    print get_warning_message(message)


def print_success_message(message):
    """ Print success message

    Args:
        message (str): message to display

    """
    print get_success_message(message)
