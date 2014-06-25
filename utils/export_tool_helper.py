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
from utils.color_log_helper import print_warning_message

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


def add_inlutfile_option(parser, is_list=False):
    """ Add inlutfile argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    help_message = (" to LUTs.\n Available input formats : {0}"
                    ).format(str(OCIO_LUTS_FORMATS))
    if is_list:
        parser.add_argument("inlutfiles",
                            help="paths{0}".format(help_message),
                            type=str,
                            nargs='+')
    else:
        parser.add_argument("inlutfile",
                            help="path{0}".format(help_message),
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
        parser.add_argument("-outfile",
                            "--outlutfile",
                            help=help_msg,
                            type=str,
                            default=None)


def add_out_type_option(parser):
    """ Add out type argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument("--out_type",
                        help=("Output LUT type.\nBeware: every format doesn't "
                              "support each type. See format help."),
                        type=str,
                        choices=presets.EXPORT_CHOICE,
                        default=None)


def add_out_format_option(parser):
    """ Add out format argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument("--out_format",
                        help=("Output LUT format.\nBeware: 3dl, clcc, json are"
                              " 3D only and lut is 1D/2D only."),
                        type=str,
                        choices=['3dl', 'csp', 'cube', 'lut', 'spi', 'clcc',
                                 'json'],
                        default=None)


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
                        default=None,
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
                        default=None,
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


def add_silent_option(parser):
    """ Add verbose argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument('--silent',
                        action='store_true',
                        help='Hide log')


def add_trace_option(parser):
    """ Add trace argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument('--trace',
                        action='store_true',
                        help='In case of error, print stack trace')


def add_preset_option(parser):
    """ Add preset argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    loaded_presets = presets.get_presets_from_env()
    if len(loaded_presets) > 0:
        parser.add_argument('--preset',
                            type=str,
                            choices=loaded_presets.keys(),
                            help=('Use a LUT export preset to set output LUT '
                                  'arguments'),
                            default=None)
        parser.add_argument('--overwrite-preset',
                            action='store_true',
                            help=("If a preset + other options are "
                                  "specified, it will overwrite preset values"
                                  " with the option values."
                                  "Ex: --preset lustre --output-range [0, 255]"
                                  ", will use range defined by --output-range"
                                  ))


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
    # presets
    add_preset_option(parser)


def _get_ext_and_helper(key, typ):
    """ Guess the helper and extension thanks to key.
    Key can be an extension or an option. If its an option, extension is deduce
    from the option name

    Args:
        key (str): option (spi, clcc, 3dl...) or extension (.spi1d, .cc, .3dl)

        typ (str): LUT type. Values: '1D', '2D' or '3D'

    Returns:
        .helper, ext

    """
    if not key.startswith('.'):
        ext = ".{0}".format(key)
    else:
        ext = key
    if key.endswith('3dl'):
        helper = THREEDL_HELPER
    elif key.endswith('cube'):
        helper = CUBE_HELPER
    elif key.endswith('csp'):
        helper = CSP_HELPER
    elif key.endswith('lut'):
        helper = ASCII_HELPER
    elif key.endswith('spi') or key.endswith('spi1d') or key.endswith('spi3d'):
        if typ == '3D':
            ext = '.spi3d'
        else:
            ext = '.spi1d'
        helper = SPI_HELPER
    elif key.endswith('clcc') or key.endswith('.cc'):
        ext = ".cc"
        helper = CLCC_HELPER
    elif key.endswith('json'):
        helper = JSON_HELPER
    else:
        raise ExportLutException("Unsupported export format: {0}".format(key))
    return ext, helper


def _get_write_function(helper, typ):
    """ Return write function

    Args:
        typ (str): LUT type. Values: '1D', '2D' or '3D'

    Returns:
        .write function

    """
    # get write function
    if typ == '3D':
        return helper.write_3d_lut
    elif typ == '1D':
        return helper.write_1d_lut
    elif typ == '2D':
        return helper.write_2d_lut


def get_write_function(preset, overwrite_preset=False, out_type=None,
                       out_format=None, input_range=None, output_range=None,
                        out_bit_depth=None, out_cube_size=None, verbose=False):
    """ Get write function from a preset

    Args:
        preset (dict): lut generic and sampling informations

    Returns:
        .write function

    """
    if overwrite_preset:
        if not out_type is None:
            preset[presets.TYPE] = out_type
        if not out_format is None:
            preset[presets.EXT] = out_format
        if not input_range is None:
            preset[presets.IN_RANGE] = input_range
        if not output_range is None:
            preset[presets.OUT_RANGE] = output_range
        if not out_bit_depth is None:
            preset[presets.OUT_BITDEPTH] = out_bit_depth
        if not out_cube_size is None:
            preset[presets.CUBE_SIZE] = out_cube_size

    if (not overwrite_preset
    and (not out_type is None
         or not out_format is None
         or not input_range is None
         or not output_range is None
         or not out_bit_depth is None
         or not out_cube_size is None
         )):
        if verbose:
            print_warning_message(("A preset was specified."
                                   " Default behaviour is to ignore other"
                                   " export options. Use "
                                   "--overwrite-preset, if you want to "
                                   "overwrite preset values that are"
                                   " redefined by other options"))

    typ = preset[presets.TYPE]
    ext, helper = _get_ext_and_helper(preset[presets.EXT], typ)
    # necessary if presets.TYPE was overwrite by overwrite_preset option
    preset[presets.EXT] = ext
    # check
    helper.check_preset(preset)
    return _get_write_function(helper, typ)


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
    ext, helper = _get_ext_and_helper(out_format, out_type)
    preset[presets.EXT] = ext
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
    return preset, _get_write_function(helper, out_type)
