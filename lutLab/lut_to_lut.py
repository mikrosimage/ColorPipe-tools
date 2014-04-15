#!/usr/bin/python

""" Convert a LUT into another format

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import argparse
from utils.ocio_helper import OCIO_LUTS_FORMATS, create_ocio_processor
from utils.csp_helper import write_2d_csp_lut
# from utils.cube_helper import CUBE_HELPER
from utils.lut_utils import get_default_out_path, write_3d_json_file
from utils.clcc_helper import write_3d_clcc_lut
from PyOpenColorIO.Constants import (
    INTERP_LINEAR, INTERP_TETRAHEDRAL
)
from utils import debug_helper
import sys


class LutToLutException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


def lut_to_lut(inlutfile, outlutfile=None, lut_type='1D_CUBE',
               lutsize=16, cubesize=17, inverse=False):
    """Extract the tone mapping curve of a 3D LUT

    Args:
        inlutfile (str): an input 3D LUT

    Kwargs:
        outlutfile (str): the output 1D LUT. If not define, LUT is written in
        the input LUT directory and post-fixed with "_export"

        lut_type (str): specify output LUT format. For now only 2D/3D csp and
        2D cube are available.

        lutsize (int): out LUT bit precision for 1D. Ex : 16 (bits)

    """
    samples_count = pow(2, lutsize)
# WIP
#     if lut_type == '1D_CUBE':
#         ext = ".cube"
#         write_function = write_2d_cube_lut
#         interp = INTERP_LINEAR
#     elif lut_type == '3D_CUBE':
#         ext = ".cube"
#         write_function = write_3d_cube_lut
#         interp = INTERP_TETRAHEDRAL
    if lut_type == '1D_CSP':
        ext = ".csp"
        write_function = write_2d_csp_lut
        interp = INTERP_LINEAR
    elif lut_type == '3D_JSON':
        ext = ".json"
        write_function = write_3d_json_file
        interp = INTERP_TETRAHEDRAL
    elif lut_type == '3D_CLCC':
        ext = ".cc"
        write_function = write_3d_clcc_lut
        interp = INTERP_TETRAHEDRAL
    else:
        raise LutToLutException("Unsupported export format!")
    if not outlutfile:
        outlutfile = get_default_out_path(inlutfile, ext)
    processor = create_ocio_processor(inlutfile, interpolation=interp,
                                      inverse=inverse)
    # init vars
    max_value = samples_count - 1.0
    red_values = []
    green_values = []
    blue_values = []
    if "1D" in lut_type:
        # process color values
        for code_value in range(0, samples_count):
            norm_value = code_value / max_value
            res = processor.applyRGB([norm_value, norm_value, norm_value])
            red_values.append(res[0])
            green_values.append(res[1])
            blue_values.append(res[2])
        # write
        write_function(outlutfile, red_values, green_values, blue_values)
    elif "3D" in lut_type:
        # write
        write_function(outlutfile, cubesize, processor)
    print "{0} was converted into {1}.".format(inlutfile, outlutfile)


def __get_options():
    """ Return lut_to_lut option parser

    Returns:
        .argparse.ArgumentParser.args

    """
    ## Define parser
    description = 'Convert a LUT into another format'
    parser = argparse.ArgumentParser(description=description)
    # input lut
    parser.add_argument("inlutfile", help=(
        "path to a LUT.\n{0}"
    ).format(str(OCIO_LUTS_FORMATS)), type=str)
    # output lut
    parser.add_argument("-out", "--outlutfile", help=(
        "path to the output LUT"
    ), type=str, default=None)
    # type
    parser.add_argument("-t", "--out-type",
                        help=("Output LUT type."),
                        type=str,
                        choices=['1D_CSP', '1D_CUBE', '3D_CUBE', '3D_CLCC',
                                 '3D_JSON'],
                        default='1D_CUBE')
    # out lut size
    parser.add_argument("-os", "--out-lut-size", help=(
        "Output lut bit precision. Ex : 10, 16, 32."
    ), default=16, type=int)
    # out cube size
    parser.add_argument("-ocs", "--out-cube-size", help=(
        "Output cube size (3D only). Ex : 17, 32."
    ), default=17, type=int)
    # inverse
    parser.add_argument("-inv", "--inverse", help="Inverse input LUT",
                        action="store_true")
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
    """ Command line interface
    """
    ARGS = __get_options()
    lut_to_lut(ARGS.inlutfile, ARGS.outlutfile, ARGS.out_type,
               ARGS.out_lut_size, ARGS.out_cube_size, ARGS.inverse)
