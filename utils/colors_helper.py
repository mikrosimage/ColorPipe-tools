""" Colors helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.3"
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


def XYZ_to_xy(XYZ):
    """Convert XYZ to xy

    Args:
        XYZ ([float, float, float]: X, Y, Z input values

    Returns:
        .[float, float]

    """
    X, Y, Z = XYZ
    divider = (X + Y + Z)
    x = X / divider
    y = Y / divider
    return [x, y]


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


def xy_to_RGB(xy, colorspace, clamp=False):
    """Convert xy to RGB values

    Args:
        xy ([float, float]): x, y input values

        colorspace (utils.colorspaces): reference RGB colorspace

    kwargs:
        clamp (bool): clamp resulting values between 0 and 1

    Returns:
        .[float, float, float]

    """
    XYZ = xy_to_XYZ(xy)
    return XYZ_to_RGB(XYZ, colorspace, clamp)


def XYZ_to_RGB(XYZ, colorspace, clamp=False):
    """Convert XYZ to RGB values

    Args:
        XYZ ([float, float, float]): X, Y, Z input values

        colorspace (utils.colorspaces): reference RGB colorspace

    kwargs:
        clamp (bool): clamp resulting values between 0 and 1

    Returns:
        .[float, float, float]

    """
    matrix = get_XYZ_to_RGB_matrix(colorspace.get_red_primaries(),
                                   colorspace.get_green_primaries(),
                                   colorspace.get_blue_primaries(),
                                   colorspace.get_white_point()
                                   )
    # apply matrix
    RGB = apply_matrix(matrix, XYZ)
    # apply gradation
    RGB = [colorspace.encode_gradation(value) for value in RGB]
    # clamp
    if clamp:
        RGB = [clamp_value(value) for value in RGB]
    return RGB


def apply_matrix(matrix, triplet):
    """Apply a matrix on a value triplet

    Args:
        matrix (3x3 numpy.matrix): matrix to apply (ex : RGB to XYZ matrix)

        triplet ([float, float, float]: ex. RGB or XYZ values

    Returns:
        .[float, float, float]

    """
    a, b, c = triplet
    ap = matrix.item(0, 0) * a + matrix.item(0, 1) * b + matrix.item(0, 2) * c
    bp = matrix.item(1, 0) * a + matrix.item(1, 1) * b + matrix.item(1, 2) * c
    cp = matrix.item(2, 0) * a + matrix.item(2, 1) * b + matrix.item(2, 2) * c
    return [ap, bp, cp]


def clamp_value(value, max_value=1.0, min_value=0.0):
    """Clamp a value between max and min

    Args:
        value (float): value to clamp

    Kwargs:
        max (float): max value

        min (float): min value

    Returns:
        .float

    """
    return max(min(value, max_value), min_value)


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


def get_XYZ_to_RGB_matrix(xy_red, xy_green, xy_blue, xy_white):
    """Compute XYZ to RGB matrix
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
    return get_RGB_to_XYZ_matrix(xy_red, xy_green, xy_blue, xy_white).I
