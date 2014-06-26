#!/usr/bin/python

""" Display RGB colorspaces to XYZ conversion matrices and their inverses

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.3"
from utils.colors_helper import get_RGB_to_XYZ_matrix
from utils.colorspaces import COLORSPACES
from utils.private_colorspaces import PRIVATE_COLORSPACES
import argparse
import sys
from utils import debug_helper


class RGBToXYZMatrixException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


def matrix_to_string(matrix, extra=""):
    """Return a string version of the matrix

    Args:
        matrix (numpy.matrix (3x3)): matrix to convert
        extra (float): additionnal 4th column value

    Returns:
        string

    """
    return ("{0:.10f} {1:.10f} {2:.10f} {9}\n"
            "{3:.10f} {4:.10f} {5:.10f} {10}\n"
            "{6:.10f} {7:.10f} {8:.10f} {11} \n").format(matrix.item(0, 0),
                                                         matrix.item(0, 1),
                                                         matrix.item(0, 2),
                                                         matrix.item(1, 0),
                                                         matrix.item(1, 1),
                                                         matrix.item(1, 2),
                                                         matrix.item(2, 0),
                                                         matrix.item(2, 1),
                                                         matrix.item(2, 2),
                                                         extra,
                                                         extra,
                                                         extra)


def display_matrix(colorspace, matrix_format):
    """Display RGB to XYZ matrix corresponding to colorspace and formatting
    as format

    Args:
        colorspace (str): input colorspace.

        matrix_format (str): output format. simple, matrix, spimtx.

    """
    try:
        colorspace_obj = COLORSPACES[colorspace]
    except KeyError:
        colorspace_obj = PRIVATE_COLORSPACES[colorspace]
    matrix = get_RGB_to_XYZ_matrix(colorspace_obj.get_red_primaries(),
                                   colorspace_obj.get_green_primaries(),
                                   colorspace_obj.get_blue_primaries(),
                                   colorspace_obj.get_white_point())
    if matrix_format == 'simple':
        matrix_dump = matrix_to_string(matrix)
        inv_matrix_dump = matrix_to_string(matrix.I)
    elif matrix_format == 'spimtx':
        matrix_dump = matrix_to_string(matrix, "0")
        inv_matrix_dump = matrix_to_string(matrix.I, "0")
    else:
        matrix_dump = "{0}".format(matrix)
        inv_matrix_dump = "{0}".format(matrix.I)
    print "{0} to XYZ matrix ({1} output):\n".format(colorspace, matrix_format)
    print matrix_dump
    print "XYZ to {0} matrix ({1} output):\n".format(colorspace, matrix_format)
    print inv_matrix_dump


def __get_options():
    """ Return rgb_to_xyz option parser

    Returns:
        .argparse.ArgumentParser.args

    """
    # Define parser
    description = 'Print RGB -> XYZ matrix'
    parser = argparse.ArgumentParser(description=description)
    # RGB colorspace
    parser.add_argument("-c", "--colorspace",
                        help=("Input RGB Colorspace."),
                        type=str,
                        choices=sorted(COLORSPACES.keys() +
                                       PRIVATE_COLORSPACES.keys()),
                        default='Rec709')
    # Output format
    parser.add_argument("-f", "--format",
                        help=("Output formatting."),
                        type=str,
                        choices=['matrix', 'spimtx', 'simple'],
                        default='matrix')
    # version
    parser.add_argument('-v', "--version", action='version',
                        version='{0} - version {1}'.format(description,
                                                           __version__))
    # full version
    versions = debug_helper.get_imported_modules_versions(sys.modules,
                                                          globals())
    versions = '{0} - version {1}\n\n{2}'.format(description,
                                                 __version__,
                                                 versions)
    parser.add_argument('-V', "--full-versions",
                        action=debug_helper.make_full_version_action(versions))
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = __get_options()
    display_matrix(ARGS.colorspace, ARGS.format)
