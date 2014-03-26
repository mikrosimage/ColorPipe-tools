""" CSP (Cinespace LUTs) helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import itertools
from utils.lut_utils import check_arrays_length


class CSPHelperException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


def get_1d_csp_header(size, input_range=None):
    """Return CSP default pre-LUT header

    Args:
        size (int): lut array size. Ex: 65536

    Kwargs:
        input_range ([nb, nb]): input range

    Returns:
        .str

    """
    if input_range == None:
        input_range = [0, 1]
    default_header = (
        "CSPLUTV100\n1D\n\n"
        "2\n{0} {1}\n0.0 1.0\n\n"
        "2\n{0} {1}\n0.0 1.0\n\n"
        "2\n{0} {1}\n0.0 1.0\n\n".format(input_range[0], input_range[1])
    )
    return "{0}{1}\n".format(default_header, size)


def write_2d_csp_lut(filename, xvalues, yvalues, zvalues,  input_range=None):
    """Write a 2D CSP LUT

    Args:
        filename (str): out LUT path

        xvalues (float array): 1st channel values

        yvalues (float array): 2nd channel values

        zvalues (float array): 3rd channel values

    Kwargs:
        input_range ([nb, nb]): input range

    """
    check_arrays_length(xvalues, yvalues, zvalues)
    lutfile = open(filename, 'w+')
    lutfile.write(get_1d_csp_header(len(xvalues), input_range))
    for x, y, z in itertools.izip(xvalues, yvalues, zvalues):
        lutfile.write("{0:.6f} {1:.6f} {2:.6f}\n".format(x, y, z))
    lutfile.close()


def write_1d_csp_lut(filename, values, input_range=None):
    """ Write a 1D CSP LUT

    Args:
        filename (str): out LUT path

        values (float array): 1st channel values

    Kwargs:
        input_range ([nb, nb]): input range

    """
    write_2d_csp_lut(filename, values, values, values, input_range)
