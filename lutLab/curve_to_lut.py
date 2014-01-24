#!/usr/bin/python
"""Convert colorspace gradation curve into 1D LUT

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
from utils.colorspaces import COLORSPACES
from utils.private_colorspaces import PRIVATE_COLORSPACES
import argparse
from utils.csp_helper import write_1d_csp_lut
from utils.cube_helper import write_1d_cube_lut
from utils.spi_helper import write_1d_spi_lut
from utils import debug_helper
from utils.lut_utils import check_extension, LUTException
import sys
from numpy import linspace
import os


class CurveToLUTException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


class Direction(object):
    """Curve direction enum

    """
    ENCODE = "encode"
    DECODE = "decode"


def curve_to_lut(colorspace, outlutpath, lut_type='1D_CUBE',
                 lut_range=None, lutsize=16, direction=Direction.ENCODE):
    """Export a LUT from a colorspace gradation function

    Args:
        colorspace (str): input colorspace

        lut_type (str): 1D_CUBE, 1D_CSP, 1D_SPI

        lut_range ([float, float]): LUT range boundaries

        lutsize (int): out LUT bit precision for 1D. Ex : 16 (bits)

        direction (Direction): encode or decode

    """
    # init
    if not lut_range:
        lut_range = [0, 1]
    samples_count = pow(2, lutsize)
    if lut_type == '1D_CUBE':
        ext = ".cube"
        write_function = write_1d_cube_lut
    elif lut_type == '1D_CSP':
        ext = ".csp"
        write_function = write_1d_csp_lut
    elif lut_type == '1D_SPI':
        ext = ".spi1d"
        write_function = lambda lutfile, values: write_1d_spi_lut(lutfile,
                                                                  values,
                                                                  lut_range)
    else:
        raise CurveToLUTException(("Unsupported export "
                                   "format: {0}").format(lut_type))
    # process file output
    if os.path.isdir(outlutpath):
        filename = "{0}_{1}{2}".format(direction, colorspace, ext)
        outlutfile = os.path.join(outlutpath, filename)
    else:
        try:
            check_extension(outlutpath, ext)
            outlutfile = outlutpath
        except LUTException as error:
            raise CurveToLUTException(("Directory doesn't exist "
                                       "or {0}").format(error))
    # get colorspace function
    try:
        colorspace_obj = (COLORSPACES.items() +
                          PRIVATE_COLORSPACES.items())[colorspace]
    except KeyError:
        raise CurveToLUTException(("Unsupported {0} "
                                   "Colorspace!").format(colorspace))
    if direction == Direction.DECODE:
        gradation = colorspace_obj.decode_gradation
    else:
        gradation = colorspace_obj.encode_gradation
    # create range
    input_range = linspace(lut_range[0], lut_range[1], samples_count)
    output_range = []
    for x in input_range:
        y = gradation(x)
        output_range.append(y)
    write_function(outlutfile, output_range)
    print "{0} was converted into {1}.".format(colorspace, outlutfile)


def __get_options():
    """Return curve_to_lut option parser

    Returns:
        .argparse.ArgumentParser.args

    """
    ## Define parser
    description = 'Create lut file corresponding to a colorspace gradation'
    parser = argparse.ArgumentParser(description=description)
    # RGB colorspace
    parser.add_argument("colorspace",
                        help=("Input RGB Colorspace."),
                        type=str,
                        choices=sorted(COLORSPACES.keys() +
                                        PRIVATE_COLORSPACES.keys()))
    # output lut
    parser.add_argument("outlutpath", help=("path to the output LUT."
                                                      " Can be a file or a "
                                                      "directory."
                                                      ), type=str)
    # type
    parser.add_argument("-t", "--out-type", help=("Output LUT type."),
                        type=str, choices=['1D_CSP', '1D_CUBE', '1D_SPI'],
                        default='1D_CUBE')
    # in range
    parser.add_argument("-ir", "--in-range", help=("In range value."),
                        type=float, default=0.0)
    # out range
    parser.add_argument("-or", "--out-range", help=("Out range value."),
                        type=float, default=1.0)
    # out lut size
    parser.add_argument("-os", "--out-lut-size", help=(
        "Output lut bit precision. Ex : 10, 16, 32."
    ), default=16, type=int)
    # direction
    parser.add_argument("-d", "--direction", help=("Direction : "
                                                   "encode or decode."),
                        type=str, choices=[Direction.ENCODE, Direction.DECODE],
                        default=Direction.ENCODE)
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
    try:
        curve_to_lut(ARGS.colorspace, ARGS.outlutpath, ARGS.out_type,
                     [ARGS.in_range, ARGS.out_range], ARGS.out_lut_size,
                     ARGS.direction)
    except (CurveToLUTException, LUTException) as error:
        print "Curve to LUT: {0}".format(error)
