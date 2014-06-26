""" OpenColorIO helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import os
# import OpenColorIO
from PyOpenColorIO import (
    Config, ColorSpace, FileTransform, GroupTransform,
)
from PyOpenColorIO.Constants import (
    INTERP_LINEAR,
    COLORSPACE_DIR_TO_REFERENCE,
    TRANSFORM_DIR_FORWARD, TRANSFORM_DIR_INVERSE,
)

OCIO_1D_LUTS_FORMATS = ['.csp', '.cub', '.cube', '.hdl', '.spi1d']

OCIO_3D_LUTS_FORMATS = ['.3dl', '.csp', '.cub', '.cube', '.hdl', '.look',
                        '.mga/m3d', '.spi3d', '.spimtx', '.vf']

OCIO_LUTS_FORMATS = sorted(OCIO_1D_LUTS_FORMATS +
                           list(set(OCIO_3D_LUTS_FORMATS) -
                                set(OCIO_1D_LUTS_FORMATS)))


def create_ocio_processor(lutfiles, interpolation=INTERP_LINEAR, inverse=False,
                          prelutfile=None, postlutfile=None):
    """Create an OpenColorIO processor for lutfile

    Args:
        lutfiles (str or [str]): path to a LUT or list of LUT paths

        interpolation (int): can be INTERP_NEAREST, INTERP_LINEAR or
        INTERP_TETRAHEDRAL (only for 3D LUT)

        inverse (bool): get an inverse direction processor

    Kwargs:
        prelutfile (str): path to a pre LUT

        postlutfile (str): path to a post LUT

    Returns:
        PyOpenColorIO.config.Processor.

    """
    if inverse:
        direction = TRANSFORM_DIR_INVERSE
    else:
        direction = TRANSFORM_DIR_FORWARD
    config = Config()
    # In colorspace (LUT)
    colorspace = ColorSpace(name='RawInput')
    group = GroupTransform()
    # Prelut
    if prelutfile:
        prelut = FileTransform(prelutfile, interpolation=interpolation)
        group.push_back(prelut)
    # Mainlut
    if not isinstance(lutfiles, (list, tuple)):
        lutfiles = [lutfiles]
    for lutfile in lutfiles:
        main_lut = FileTransform(lutfile, interpolation=interpolation,
                                 direction=direction)
        group.push_back(main_lut)
    # Postlut
    if postlutfile:
        postlut = FileTransform(postlutfile, interpolation=interpolation)
        group.push_back(postlut)
    colorspace.setTransform(group, COLORSPACE_DIR_TO_REFERENCE)
    config.addColorSpace(colorspace)
    # Out colorspace
    colorspace = ColorSpace(name='ProcessedOutput')
    config.addColorSpace(colorspace)
    # Create a processor corresponding to the LUT transformation
    try:
        return config.getProcessor('RawInput', 'ProcessedOutput')
    except Exception, e:
        # tetrahedral interpolation is only allowed with 3D LUT
        # TODO set interpo mode by LUT
        if "tetrahedral interpolation is not allowed" in str(e):
            return create_ocio_processor(lutfiles, interpolation=INTERP_LINEAR,
                                         inverse=inverse,
                                         prelutfile=prelutfile,
                                         postlutfile=postlutfile)
        raise


def is_3d_lut(processor, lutfile):
    """Use hasChannelCrosstalk function to deduce if lutfile is a 3D LUT

    Args:
        processor (PyOpenColorIO.config.Processor): OpenColorIO processor

        lutfile (str): path to a LUT

    Returns:
        .bool

    """
    fileext = os.path.splitext(lutfile)[1]
    return processor.hasChannelCrosstalk() or fileext == '.spimtx'
