#!/usr/bin/python

""" Convert a LUT into another format

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
import argparse
from utils.ocio_helper import OCIO_LUTS_FORMATS, create_ocio_processor
from utils.csp_helper import write_2d_csp_lut
from utils.cube_helper import write_2d_cube_lut, write_3d_cube_lut
from utils.lut_utils import get_default_out_path
from PyOpenColorIO.Constants import (
    INTERP_LINEAR, INTERP_TETRAHEDRAL
)


class LutToLutException(Exception):
    pass


def lut_to_lut(inlutfile, outlutfile=None, type='1D_CUBE',
               lutsize=16, cubesize=17):
    """Extract the tone mapping curve of a 3D LUT

    Args:
        inlutfile (str): an input 3D LUT

    Kwargs:
        outlutfile (str): the output 1D LUT. If not define, LUT is written in
        the input LUT directory and post-fixed with "_export"

        type (str): specify output LUT format. For now only 2D csp and 2D cube
        are available.

        lutsize (int): out LUT bit precision for 1D. Ex : 16 (bits)

    """
    samples_count = pow(2, lutsize)
    if type == '1D_CUBE':
        ext = ".cube"
        write_function = write_2d_cube_lut
        interp = INTERP_LINEAR
    elif type == '3D_CUBE':
        ext = ".cube"
        write_function = write_3d_cube_lut
        interp = INTERP_TETRAHEDRAL
    elif type == '1D_CSP':
        ext = ".csp"
        write_function = write_2d_csp_lut
        interp = INTERP_LINEAR
    else:
        raise LutToLutException("Unsupported export format!")
    if not outlutfile:
        outlutfile = get_default_out_path(inlutfile, ext)
    processor = create_ocio_processor(inlutfile, interpolation=interp)
    # init vars
    max_value = samples_count - 1.0
    red_values = []
    green_values = []
    blue_values = []
    if "1D" in type:
        # process color values
        for n in range(0, samples_count):
            x = n/max_value
            res = processor.applyRGB([x, x, x])
            red_values.append(res[0])
            green_values.append(res[1])
            blue_values.append(res[2])
        # write
        write_function(outlutfile, red_values, green_values, blue_values)
    elif "3D" in type:
        # write
        write_function(outlutfile, cubesize, processor)


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
                        choices=['1D_CSP', '1D_CUBE', '3D_CUBE'],
                        default='1D_CUBE')
    # out lut size
    parser.add_argument("-os", "--out-lut-size", help=(
        "Output lut bit precision. Ex : 10, 16, 32."
    ), default=16, type=int)
    # out cube size
    parser.add_argument("-ocs", "--out-cube-size", help=(
        "Output cube size (3D only). Ex : 17, 32."
    ), default=17, type=int)
    return parser.parse_args()

if __name__ == '__main__':
    """ Command line interface
    """
    args = __get_options()
    lut_to_lut(args.inlutfile, args.outlutfile, args.out_type,
               args.out_lut_size, args.out_cube_size)
