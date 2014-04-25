""" Export tool helper

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import utils.lut_presets as presets
from utils.ocio_helper import OCIO_LUTS_FORMATS
from utils.debug_helper import make_full_version_action
from utils.threedl_helper import THREEDL_HELPER
from utils.csp_helper import CSP_HELPER
from utils.cube_helper import CUBE_HELPER
from utils.ascii_helper import ASCII_HELPER
from utils.clcc_helper import CLCC_HELPER
from utils.spi_helper import SPI_HELPER
from utils.json_helper import JSON_HELPER

import warnings
warnings.filterwarnings(
    'ignore',
    message='BaseException.message has been deprecated as of Python 2.6',
    category=DeprecationWarning,
    module='argparse')


class ExportLutException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


# Argparse options


def add_inlutfile_option(parser):
    """ Add inlutfile argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument("inlutfile",
                        help=("path to a LUT.\n Available input formats : {0}"
                              ).format(str(OCIO_LUTS_FORMATS)),
                        type=str)


def add_outlutfile_option(parser, required=False):
    """ Add outlutfile argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    Kwargs:
        required (bool): true if the option is required

    """
    help_msg = "path to the output LUT or to the output directory"
    if required:
        parser.add_argument("outlutfile",
                            help=help_msg,
                            type=str,
                            default=None)
    else:
        parser.add_argument("-out",
                            "--outlutfile",
                            help=help_msg,
                            type=str,
                            default=None)


def add_out_type_option(parser):
    """ Add out type argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument("out_type",
                        help=("Output LUT type.\nBeware: every format doesn't "
                              "support each type. See format help."),
                        type=str,
                        choices=presets.EXPORT_CHOICE,
                        default='3D')


def add_out_format_option(parser):
    """ Add out format argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument("out_format",
                        help=("Output LUT format.\nBeware: 3dl, clcc, json are"
                              " 3D only and lut is 1D/2D only."),
                        type=str,
                        choices=['3dl', 'csp', 'cube', 'lut', 'spi', 'clcc',
                                 'json'],
                        default='cube')


def add_range_option(parser):
    """ Add ranges argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument("-ir",
                        "--input-range",
                        help="Input range. Ex: 0.0 1.0 or 0 4095",
                          nargs='+')
    parser.add_argument("-or",
                        "--output-range",
                        help="Output range. Ex: 0.0 1.0 or 0 4095",
                        nargs='+')


def add_out_bitdepth_option(parser):
    """ Add out bit depth argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument("-os",
                        "--out-bit-depth",
                        help=("Output lut bit precision (1D only). "
                              "Ex : 10, 16, 32."),
                        default=16,
                        type=int)


def add_inverse_option(parser):
    """ Add inverse argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument("-inv",
                        "--inverse",
                        help="Inverse input LUT (1D only)",
                        action="store_true")


def add_out_cube_size_option(parser):
    """ Add inverse argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    # # 3D arg
    # out cube size
    parser.add_argument("-ocs",
                        "--out-cube-size",
                        help="Output cube size (3D only). Ex : 17, 32.",
                        default=17,
                        type=int)


def add_version_option(parser, description, version, full_version):
    """ Add version argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

        description (str): tool description

        version (str): version of the module

        full_version (str): versions of dependencies.
        See debug_helper.get_imported_modules_versions

    """
        # version
    parser.add_argument('-v',
                        "--version",
                        action='version',
                        version='{0} - version {1}'.format(description,
                                                           version))
    # full version
    versions = '{0} - version {1}\n\n{2}'.format(description,
                                                 version,
                                                 full_version)
    parser.add_argument('-V',
                        "--full-versions",
                        action=make_full_version_action(versions))


def add_verbose_option(parser):
    """ Add verbose argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument('--verbose',
                        action='store_true',
                        help='Print log')


def add_trace_option(parser):
    """ Add trace argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument('--trace',
                        action='store_true',
                        help='In case of error, print stack trace')


def add_export_lut_options(parser):
    """ Add export LUT arguments : out lut file, type, format, ranges,
    out bit depth and out cube size.

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    add_out_type_option(parser)
    add_out_format_option(parser)
    add_range_option(parser)
    # 1D arg
    add_out_bitdepth_option(parser)
    # 3D arg
    add_out_cube_size_option(parser)


def get_preset_and_write_function(out_type, out_format,
                          input_range=None, output_range=None,
                          out_bit_depth=None, out_cube_size=None):
    """ Get preset and write function considering args

    Args:
        out_type (str): 1D, 2D or 3D

        out_format (str): '3dl', 'csp', 'cube', 'lut', 'spi', 'clcc', 'json'...

    Kwargs:
        input_range ([int/float, int/float]): input range.
        Ex: [0.0, 1.0] or [0, 4095]

        output_range ([int/float, int/float]): output range.
        Ex: [0.0, 1.0] or [0, 4095]

        out_bit_depth (int): output lut bit precision (1D only).
        Ex : 10, 16, 32.

        out_cube_size (int): output cube size (3D only). Ex : 17, 32.

    Returns:
        (preset, write function)

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
        raise ExportLutException(("Unsupported export "
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
    # get write function
    if out_type == '3D':
        write_function = helper.write_3d_lut
    elif out_type == '1D':
        write_function = helper.write_1d_lut
    elif out_type == '2D':
        write_function = helper.write_2d_lut
    return preset, write_function
