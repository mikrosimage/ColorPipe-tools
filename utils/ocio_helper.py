""" OpenColorIO helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
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

OCIO_LUTS_FORMATS = sorted(OCIO_1D_LUTS_FORMATS + list(set(OCIO_3D_LUTS_FORMATS)
                           - set(OCIO_1D_LUTS_FORMATS)))


def create_ocio_processor(lutfile, interpolation=INTERP_LINEAR, inverse=False,
                          prelutfile=None, postlutfile=None):
    """Create an OpenColorIO processor for lutfile

    Args:
        lutfile (str): path to a LUT

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
    mainLut = FileTransform(lutfile, interpolation=interpolation,
                            direction=direction)
    group = GroupTransform()
    # Prelut
    if prelutfile:
        prelut = FileTransform(prelutfile, interpolation=interpolation)
        group.push_back(prelut)
    # Mainlut
    group.push_back(mainLut)
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
    return config.getProcessor('RawInput', 'ProcessedOutput')


def is_3d_lut(processor, filepath):
    fileext = os.path.splitext(filepath)[1]
    return processor.hasChannelCrosstalk() or fileext == '.spimtx'
