#!/usr/bin/python

""" Display RGB colorspaces to XYZ conversion matrices and their inverses

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.5"
from utils.colors_helper import get_RGB_to_RGB_matrix, get_colorspace_matrix
from utils.colorspaces import COLORSPACES
from utils.private_colorspaces import PRIVATE_COLORSPACES
from utils.matrix_helper import matrix_to_string, matrix_to_spimtx_string
import argparse
import sys
from utils import debug_helper

XYZ_colorspace = 'XYZ'


class RGBToXYZMatrixException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


def display_matrix(in_colorspace, out_colorspace, matrix_format, primaries_only=False):
    """Display RGB to XYZ matrix corresponding to colorspace and formatting
    as format

    Args:
        colorspace (str): input colorspace.

        matrix_format (str): output format. simple, matrix, spimtx.

    """
    if in_colorspace == XYZ_colorspace:
        if out_colorspace == XYZ_colorspace:
            raise AttributeError("In and out colorspaces can't be both XYZ !")
        matrix = get_colorspace_matrix(out_colorspace, primaries_only, inv=True)
    elif out_colorspace == XYZ_colorspace:
        matrix = get_colorspace_matrix(in_colorspace, primaries_only, inv=False)
    else:
        matrix = get_RGB_to_RGB_matrix(in_colorspace, out_colorspace, primaries_only)

    if matrix_format == 'simple':
        matrix_dump = matrix_to_string(matrix)
    elif matrix_format == 'spimtx':
        matrix_dump = matrix_to_spimtx_string(matrix)
    else:
        matrix_dump = "{0}".format(matrix)

    print "{0} to {1} matrix ({2} {3} output):\n".format(in_colorspace,
                                                         out_colorspace,
                                                         primaries_only and "primaries"
                                                         or "primaries + white point",
                                                         matrix_format)
    print matrix_dump


def __get_options():
    """ Return rgb_to_xyz option parser

    Returns:
        .argparse.ArgumentParser.args

    """
    # Define parser
    description = 'Print RGB -> RGB matrix'
    parser = argparse.ArgumentParser(description=description)
    # RGB colorspace
    colorspaces = sorted(COLORSPACES.keys() + PRIVATE_COLORSPACES.keys() + [XYZ_colorspace])
    parser.add_argument("-in", "--in-colorspace",
                        help=("Input RGB Colorspace."),
                        type=str,
                        choices=colorspaces,
                        required=True)
    parser.add_argument("-out", "--out-colorspace",
                        help=("Output RGB Colorspace."),
                        type=str,
                        choices=colorspaces,
                        required=True)
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
    display_matrix(ARGS.in_colorspace, ARGS.out_colorspace, ARGS.format, ARGS.primaries_only)
