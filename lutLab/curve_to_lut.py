#!/usr/bin/python
"""Convert colorspace or gamma gradation curve into 1D LUT

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.5"
import os
import sys

import argparse

from utils import debug_helper
from utils.colors_helper import lin_to_gamma, gamma_to_lin
from utils.colorspaces import COLORSPACES
# To prevent a warning in argparse
from utils.export_tool_helper import (add_export_lut_options,
                                      add_version_option,
                                      add_silent_option,
                                      get_preset_and_write_function,
                                      add_outlutfile_option,
                                      add_trace_option,
                                      get_write_function)
import utils.lut_presets as presets
from utils.lut_utils import check_extension, LUTException, get_input_range
from utils.private_colorspaces import PRIVATE_COLORSPACES
from utils.color_log_helper import (print_warning_message,
                                    print_error_message,
                                    print_success_message)


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


def curve_to_lut(colorspace, gamma, outlutfile, out_type=None, out_format=None,
                 input_range=None, output_range=None, out_bit_depth=None,
                 out_cube_size=None, verbose=False, direction=Direction.ENCODE,
                 preset=None, overwrite_preset=False,
                 process_input_range=False):
    """Export a LUT from a colorspace gradation function

    Args:
        colorspace (str): input colorspace. Mutually exclusive with gamma.
        See list of colorspaces in utils.colorspaces

        gamma (float): input gamma. Mutually exclusive with colorspace.

        out_type (str): 1D, 2D or 3D

        out_format (str): '3dl', 'csp', 'cube', 'lut', 'spi', 'clcc', 'json'...

        outlutfile (str): path to output LUT

    Kwargs:

        input_range ([int/float, int/float]): input range.
        Ex: [0.0, 1.0] or [0, 4095]

        output_range ([int/float, int/float]): output range.
        Ex: [0.0, 1.0] or [0, 4095]

        out_bit_depth (int): output lut bit precision (1D only).
        Ex : 10, 16, 32.

        out_cube_size (int): output cube size (3D only). Ex : 17, 32.

        verbose (bool): print log if true

        direction (Direction): encode or decode

        preset (dict): lut generic and sampling informations

        process_input_range (bool): If true, input range will be computed from
        colorspace gradation functions. Colorspace only"

    """
    # get colorspace function
    if colorspace is None and gamma is None:
        raise AttributeError("A colorspace or a gamma should be specified")
    if colorspace is not None and gamma is not None:
        raise AttributeError("Choose between a colorspace or a gamma")
    elif gamma is not None:
        # gamma mode
        if direction == Direction.DECODE:
            gradation = lambda value: gamma_to_lin(value, gamma)
            title = "Gamma{0}_to_lin".format(gamma)
        else:
            gradation = lambda value: lin_to_gamma(value, gamma)
            title = "Lin_to_gamma{0}".format(gamma)
    else:
        # colorspace mode
        try:
            colorspace_obj = dict(COLORSPACES.items() +
                                  PRIVATE_COLORSPACES.items())[colorspace]
        except KeyError:
            raise CurveToLUTException(("Unsupported {0} "
                                       "Colorspace!").format(colorspace))
        if direction == Direction.DECODE:
            gradation = colorspace_obj.decode_gradation
            title = "{0}_to_lin".format(colorspace)
        else:
            gradation = colorspace_obj.encode_gradation
            title = "Lin_to_{0}".format(colorspace)
    # get preset and write function
    if preset:
        write_function = get_write_function(preset, overwrite_preset,
                                            out_type, out_format,
                                            input_range,
                                            output_range,
                                            out_bit_depth,
                                            out_cube_size,
                                            verbose)
    elif out_type is None or out_format is None:
        raise CurveToLUTException("Specify out_type/out_format or a preset.")
    else:
        preset, write_function = get_preset_and_write_function(out_type,
                                                               out_format,
                                                               input_range,
                                                               output_range,
                                                               out_bit_depth,
                                                               out_cube_size)
    if preset[presets.TYPE] == '3D':
        print_warning_message(("Gradations and gamma functions are 1D / 2D"
                               " transformations. Baking them in a 3D LUT "
                               "may not be efficient. Are you sure ?"))
    # process file output
    if os.path.isdir(outlutfile):
        filename = "{0}{1}".format(title,
                                   preset[presets.EXT])
        outlutfile = os.path.join(outlutfile, filename)
    else:
        try:
            check_extension(outlutfile, preset[presets.EXT])
            outlutfile = outlutfile
        except LUTException as error:
            raise CurveToLUTException(("Directory doesn't exist "
                                       "or {0}").format(error))
    preset[presets.TITLE] = title
    if process_input_range:
        if colorspace:
            preset[presets.IN_RANGE] = get_input_range(colorspace_obj,
                                                       direction,
                                                       8)
        else:
            raise CurveToLUTException(("--process-input-range must be used"
                                       " with --colorspace."))
    if verbose:
        print "{0} will be written in {1}.".format(title, outlutfile)
        print "Final setting:\n{0}".format(presets.string_preset(preset))
    # write
    message = write_function(gradation, outlutfile, preset)
    if verbose:
        print_success_message(message)


def __get_options():
    """Return curve_to_lut option parser

    Returns:
        .argparse.ArgumentParser.args

    """
    # Define parser
    description = ('Create lut file corresponding to a colorspace or gamma '
                   'gradation')
    parser = argparse.ArgumentParser(description=description)
    # RGB colorspace
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--colorspace",
                        help=("Input RGB Colorspace."),
                        type=str,
                        choices=sorted(COLORSPACES.keys() +
                                       PRIVATE_COLORSPACES.keys()))
    action.add_argument("--gamma",
                        help="Input pure gamma gradation",
                        type=float)
    # direction
    parser.add_argument("-d", "--direction", help=("Direction : "
                                                   "encode or decode."),
                        type=str, choices=[Direction.ENCODE, Direction.DECODE],
                        default=Direction.ENCODE)
    # out lut file, type, format, ranges,  out bit depth, out cube size
    add_outlutfile_option(parser, required=True)
    add_export_lut_options(parser)
    parser.add_argument("--process-input-range", action="store_true",
                        help=("If true, input range will be computed from "
                              " colorspace gradation functions."
                              "(Colorspace only))"))
    # version
    full_version = debug_helper.get_imported_modules_versions(sys.modules,
                                                              globals())
    add_version_option(parser, description, __version__, full_version)
    # verbose
    add_silent_option(parser)
    # trace
    add_trace_option(parser)
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = __get_options()
    try:
        if ARGS.input_range is not None:
            ARGS.input_range = presets.convert_string_range(ARGS.input_range)
        if ARGS.output_range is not None:
            ARGS.output_range = presets.convert_string_range(ARGS.output_range)
        if ARGS.preset is not None:
            ARGS.preset = presets.get_presets_from_env()[ARGS.preset]
        curve_to_lut(ARGS.colorspace,
                     ARGS.gamma,
                     ARGS.outlutfile,
                     ARGS.out_type,
                     ARGS.out_format,
                     ARGS.input_range,
                     ARGS.output_range,
                     ARGS.out_bit_depth,
                     ARGS.out_cube_size,
                     not ARGS.silent,
                     ARGS.direction,
                     ARGS.preset,
                     ARGS.overwrite_preset,
                     ARGS.process_input_range
                     )
    except Exception as error:
        if ARGS.trace:
            print_error_message(error)
            raise
        MSG = "{0}.\nUse --trace option to get details".format(error)
        print_error_message(MSG)
