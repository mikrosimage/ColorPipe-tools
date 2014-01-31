""" Colors helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.2"
import math
import numpy


def xy_to_XYZ(xy, Y=1):
    """Convert xyY into XYZ

    Args:
        xy ([float, float]): x, y input values

    Kwargs:
        Y (float): Y input value

    Returns:
        .[float, float, float]

    """
    x, y = xy
    X = (x * Y) / y
    Z = ((1 - x - y) * Y) / y
    return [X, Y, Z]


def xy_to_upvp(xy):
    """Convert xy to u'v'

    Args:
        xy ([float, float]): x, y input values

    Returns:
        .[float, float]
    """
    x, y = xy
    up = 4 * x / (-2 * x + 12 * y + 3)
    vp = 9 * y / (-2 * x + 12 * y + 3)
    return [up, vp]


def lin_to_gamma(value, gamma):
    """Simple lin to Gamma function

    Args:
        value (float): input value

        gamma (float): gamma value

    Returns:
        .float

    """
    return math.pow(value, 1 / gamma)


def gamma_to_lin(value, gamma):
    """Simple gamma to lin function

    Args:
        value (float): input value

        gamma (float): gamma value

    Returns:
        .float

    """
    return math.pow(value, gamma)


def get_primaries_matrix(xy_red, xy_green, xy_blue):
    """Return primaries XYZ matrix form xy coords

    Args:
        xy_red (float, float): red primary coords

        xy_green (float, float): green primary coords

        xy_blue (float, float): blue primary coords

    Returns:
        .numpy.matrix (3x3)

    """
    XYZ_red = xy_to_XYZ(xy_red)
    XYZ_green = xy_to_XYZ(xy_green)
    XYZ_blue = xy_to_XYZ(xy_blue)
    primaries_matrix = numpy.matrix(
        [
            [XYZ_red[0], XYZ_green[0], XYZ_blue[0]],
            [XYZ_red[1], XYZ_green[1], XYZ_blue[1]],
            [XYZ_red[2], XYZ_green[2], XYZ_blue[2]],
        ])
    return primaries_matrix


def get_white_matrix(xy_white):
    """Return white point XYZ matrix form xy coords

    Args:
        xy_white (float, float): white point coords

    Returns:
        .numpy.matrix (3x1)

    """
    XYZ_white = xy_to_XYZ(xy_white)
    white_matrix = numpy.matrix(
        [
            [XYZ_white[0]],
            [XYZ_white[1]],
            [XYZ_white[2]],
        ])
    return white_matrix


def get_RGB_to_XYZ_matrix(xy_red, xy_green, xy_blue, xy_white):
    """Compute RGB to XYZ matrix
    See Bruce Lindbloom page :
    http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html

    Args:
        xy_red (float, float): red primary coords

        xy_green (float, float): green primary coords

        xy_blue (float, float): blue primary coords

        xy_white (float, float): white point coords

    Returns:
        .numpy.matrix (3x3)

    """
    primaries_matrix = get_primaries_matrix(xy_red, xy_green, xy_blue)
    white_matrix = get_white_matrix(xy_white)
    s = primaries_matrix ** -1 * white_matrix
    s_r, s_g, s_b = s.item(0, 0), s.item(1, 0), s.item(2, 0)
    RGB_to_XYZ = numpy.matrix([
        [s_r * primaries_matrix.item(0, 0), s_g * primaries_matrix.item(0, 1),
         s_b * primaries_matrix.item(0, 2)],
        [s_r * primaries_matrix.item(1, 0), s_g * primaries_matrix.item(1, 1),
         s_b * primaries_matrix.item(1, 2)],
        [s_r * primaries_matrix.item(2, 0), s_g * primaries_matrix.item(2, 1),
         s_b * primaries_matrix.item(2, 2)]])
    return RGB_to_XYZ
