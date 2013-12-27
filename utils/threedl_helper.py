""" 3dl (3D LUT) helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
import math


class ThreeDLHelperException(Exception):
    pass


def get_shaper_lut(cube_size, bit_depth):
    """ Return shaper lut as a list

    Args:
        cube_size (int): cube size. Ex: 17, 32...

        bit_depth (int): bit depth of shaper lut values. Ex: 10, 12, 16...

    Returns:
        .int list

    """
    max_value = float(math.pow(2, bit_depth) - 1)
    step = max_value / (cube_size - 1)
    shaper_lut = []
    for i in range(0, cube_size):
        shaper_lut.append(int(i*step))
    return shaper_lut


def get_string_shaper_lut(cube_size, bit_depth):
    """ Return shaper lut as a string

    Args:
        cube_size (int): cube size. Ex: 17, 32...

        bit_depth (int): bit depth of the value of the shaper lut. Ex: 10, 12,
        16...

    Returns:
        .string list

    """
    shaper_lut = get_shaper_lut(cube_size, bit_depth)
    return "{0}".format(" ".join(map(str, shaper_lut)))
