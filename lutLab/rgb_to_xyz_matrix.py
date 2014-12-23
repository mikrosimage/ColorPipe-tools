#!/usr/bin/python

""" Display RGB colorspaces to XYZ conversion matrices and their inverses

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.4"
from utils.colors_helper import get_RGB_to_XYZ_matrix, get_primaries_matrix
from utils.colorspaces import COLORSPACES
from utils.private_colorspaces import PRIVATE_COLORSPACES
from utils.matrix_helper import matrix_to_string, matrix_to_spimtx_string
import argparse
import sys
from utils import debug_helper


class RGBToXYZMatrixException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


def display_matrix(colorspace, matrix_format, primaries_only=False):
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
    if primaries_only:
        matrix = get_primaries_matrix(colorspace_obj.get_red_primaries(),
                                      colorspace_obj.get_green_primaries(),
                                      colorspace_obj.get_blue_primaries())
        matrix_type = "Primaries"
    else:
        matrix = get_RGB_to_XYZ_matrix(colorspace_obj.get_red_primaries(),
                                       colorspace_obj.get_green_primaries(),
                                       colorspace_obj.get_blue_primaries(),
                                       colorspace_obj.get_white_point())
        matrix_type = "Primaries + white point"
    if matrix_format == 'simple':
        matrix_dump = matrix_to_string(matrix)
        inv_matrix_dump = matrix_to_string(matrix.I)
    elif matrix_format == 'spimtx':
        matrix_dump = matrix_to_spimtx_string(matrix)
        inv_matrix_dump = matrix_to_spimtx_string(matrix.I)
    else:
        matrix_dump = "{0}".format(matrix)
        inv_matrix_dump = "{0}".format(matrix.I)
    print "{0} to XYZ matrix ({1}, {2} output):\n".format(colorspace, matrix_type, matrix_format)
    print matrix_dump
    print "XYZ to {0} matrix ({1}, {2} output):\n".format(colorspace, matrix_type, matrix_format)
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
    # Get primarie matrix only
    parser.add_argument("-po", "--primaries-only",
                        help="Primaries matrix only, doesn't include white point.",
                        action="store_true")
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
    display_matrix(ARGS.colorspace, ARGS.format, ARGS.primaries_only)
