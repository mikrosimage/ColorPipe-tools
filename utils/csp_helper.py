""" CSP (Cinespace LUTs) helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import itertools
from utils.lut_utils import check_arrays_length


class CSPHelperException(Exception):
    pass


def get_1d_csp_header(size):
    """Return CSP default pre-LUT header

    Args:
        size (int): lut array size. Ex: 65536

    Returns:
        .str

    """
    default_header = (
        "CSPLUTV100\n1D\n\n"
        "2\n0.0 1.0\n0.0 1.0\n\n"
        "2\n0.0 1.0\n0.0 1.0\n\n"
        "2\n0.0 1.0\n0.0 1.0\n\n"
    )
    return "{0}{1}\n".format(default_header, size)


def write_2d_csp_lut(filename, xvalues, yvalues, zvalues):
    """Write a 2D CSP LUT

    Args:
        filename (str): out LUT path

        xvalues (float array): 1st channel values

        yvalues (float array): 2nd channel values

        zvalues (float array): 3rd channel values

    """
    check_arrays_length(xvalues, yvalues, zvalues)
    f = open(filename, 'w+')
    f.write(get_1d_csp_header(len(xvalues)))
    for x, y, z in itertools.izip(xvalues, yvalues, zvalues):
        f.write("{0:.6f} {1:.6f} {2:.6f}\n".format(x, y, z))
    f.close()


def write_1d_csp_lut(filename, values):
    """ Write a 1D CSP LUT

    Args:
        filename (str): out LUT path

        values (float array): 1st channel values

    """
    write_2d_csp_lut(filename, values, values, values)
