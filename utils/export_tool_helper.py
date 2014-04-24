""" Export tool helper

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import utils.lut_presets as presets
from utils.ocio_helper import OCIO_LUTS_FORMATS
from utils.debug_helper import make_full_version_action


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


def add_outlutfile_option(parser):
    """ Add outlutfile argument

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    parser.add_argument("-out",
                        "--outlutfile",
                        help="path to the output LUT",
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


def add_export_lut_options(parser):
    """ Add export LUT arguments : out lut file, type, format, ranges,
    out bit depth and out cube size.

    Args:
        parser (argparse.ArgumentParser): parser on which option will be add

    """
    add_outlutfile_option(parser)
    add_out_type_option(parser)
    add_out_format_option(parser)
    add_range_option(parser)
    # 1D arg
    add_out_bitdepth_option(parser)
    # 3D arg
    add_out_cube_size_option(parser)
