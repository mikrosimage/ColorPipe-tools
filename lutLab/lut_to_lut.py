#!/usr/bin/python

""" Convert a LUT into another format

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.2"
import argparse
from PyOpenColorIO.Constants import INTERP_LINEAR, INTERP_TETRAHEDRAL
from utils import debug_helper
import sys
import utils.lut_presets as presets
from utils.lut_utils import get_default_out_path, check_extension
from utils.ocio_helper import (create_ocio_processor,
                               is_3d_lut)
from utils.export_tool_helper import (add_export_lut_options,
                                      add_version_option,
                                      add_inverse_option,
                                      add_verbose_option,
                                      add_inlutfile_option,
                                      get_preset_and_write_function)


class LutToLutException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


def lut_to_lut(inlutfile, out_type, out_format, outlutfile=None,
               input_range=None, output_range=None, out_bit_depth=None,
               inverse=False, out_cube_size=None, verbose=False):
    """ Concert a LUT in another LUT
    Arguments testing are delegated to LUT helpers

    Args:
        inlutfile (str): path to input LUT

        out_type (str): 1D, 2D or 3D

        out_format (str): '3dl', 'csp', 'cube', 'lut', 'spi', 'clcc', 'json'...

    Kwargs:
        outlutfile (str): path to output LUT

        input_range ([int/float, int/float]): input range.
        Ex: [0.0, 1.0] or [0, 4095]

        output_range ([int/float, int/float]): output range.
        Ex: [0.0, 1.0] or [0, 4095]

        out_bit_depth (int): output lut bit precision (1D only).
        Ex : 10, 16, 32.

        inverse (bool): inverse input LUT (1D only)

        out_cube_size (int): output cube size (3D only). Ex : 17, 32.

        verbose (bool): print log if true

    """
    preset, write_function = get_preset_and_write_function(out_type,
                                                           out_format,
                                                           input_range,
                                                           output_range,
                                                           out_bit_depth,
                                                           out_cube_size)
    if not outlutfile:
        outlutfile = get_default_out_path(inlutfile, preset[presets.EXT])
    else:
        check_extension(outlutfile, preset[presets.EXT])
    if verbose:
        print "{0} will be converted into {1}.".format(inlutfile, outlutfile)
        print "Final setting:\n{0}".format(presets.string_preset(preset))
    processor = create_ocio_processor(inlutfile,
                                      interpolation=INTERP_LINEAR,
                                      inverse=inverse)
    # change interpolation if 3D LUT
    if is_3d_lut(processor, inlutfile):
        processor = create_ocio_processor(inlutfile,
                                          interpolation=INTERP_TETRAHEDRAL,
                                          inverse=inverse)
    # write LUT
    if out_type == '3D':
        write_function(processor.applyRGB, outlutfile, preset)
    elif out_type == '1D':
        write_function(processor.applyRGB, outlutfile, preset)
    elif out_type == '2D':
        write_function(processor.applyRGB, outlutfile, preset)


def __get_options():
    """ Return lut_to_lut option parser

    Returns:
        .argparse.ArgumentParser.args

    """
    ## Define parser
    description = 'Convert a LUT into another format'
    parser = argparse.ArgumentParser(description=description)
    # input lut
    add_inlutfile_option(parser)
    # out lut file, type, format, ranges,  out bit depth, out cube size
    add_export_lut_options(parser)
    # inverse (1d arg)
    add_inverse_option(parser)
    # version
    full_version = debug_helper.get_imported_modules_versions(sys.modules,
                                                              globals())
    add_version_option(parser, description, __version__, full_version)
    # verbose
    add_verbose_option(parser)
    return parser.parse_args()


if __name__ == '__main__':
    """ Command line interface
    """
    ARGS = __get_options()
    if not ARGS.input_range is None:
        ARGS.input_range = presets.convert_string_range(ARGS.input_range)
    if not ARGS.output_range is None:
        ARGS.output_range = presets.convert_string_range(ARGS.output_range)
    lut_to_lut(ARGS.inlutfile,
               ARGS.out_type,
               ARGS.out_format,
               ARGS.outlutfile,
               ARGS.input_range,
               ARGS.output_range,
               ARGS.out_bit_depth,
               ARGS.inverse,
               ARGS.out_cube_size,
               ARGS.verbose
               )
