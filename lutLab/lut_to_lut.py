#!/usr/bin/python

""" Convert a LUT into another format

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.2"
import argparse
from utils.threedl_helper import THREEDL_HELPER
from utils.csp_helper import CSP_HELPER
from utils.cube_helper import CUBE_HELPER
from utils.ascii_helper import ASCII_HELPER
from utils.clcc_helper import CLCC_HELPER
from utils.spi_helper import SPI_HELPER
from utils.json_helper import JSON_HELPER
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
                                      add_inlutfile_option)


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

    """
    preset = {}
    # out type (1D, 2D, 3D)
    preset[presets.TYPE] = out_type
    # out format (csp, 3dl...)
    if out_format == '3dl':
        preset[presets.EXT] = '.3dl'
        helper = THREEDL_HELPER
    elif out_format == 'cube':
        preset[presets.EXT] = '.cube'
        helper = CUBE_HELPER
    elif out_format == 'csp':
        preset[presets.EXT] = '.csp'
        helper = CSP_HELPER
    elif out_format == 'lut':
        preset[presets.EXT] = '.lut'
        helper = ASCII_HELPER
    elif out_format == 'spi':
        if out_type == '3D':
            preset[presets.EXT] = '.spi3d'
        else:
            preset[presets.EXT] = '.spi1d'
        helper = SPI_HELPER
    elif out_format == 'clcc':
        preset[presets.EXT] = '.cc'
        helper = CLCC_HELPER
    elif out_format == 'json':
        preset[presets.EXT] = '.json'
        helper = JSON_HELPER
    else:
        raise LutToLutException(("Unsupported export "
                                 "format : {0}").format(out_format))
    # check args
    if not input_range is None:
        preset[presets.IN_RANGE] = input_range
    if not output_range is None:
        preset[presets.OUT_RANGE] = output_range
    if not out_bit_depth is None:
        preset[presets.OUT_BITDEPTH] = out_bit_depth
    if not out_cube_size is None:
        preset[presets.CUBE_SIZE] = out_cube_size

    # fill missing args if necessary
    preset = helper.complete_preset(preset)
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
        helper.write_3d_lut(processor.applyRGB, outlutfile, preset)
    elif out_type == '1D':
        helper.write_1d_lut(processor.applyRGB, outlutfile, preset)
    elif out_type == '2D':
        helper.write_2d_lut(processor.applyRGB, outlutfile, preset)


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
