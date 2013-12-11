""" Display RGB colorspaces to XYZ conversion matrixes

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
from utils.colors_helper import xy_to_XYZ
from utils.colorspaces import COLORSPACES
from utils.private_colorspaces import PRIVATE_COLORSPACES
import numpy
import argparse


class RGBToXYZMatrixException(Exception):
    pass


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


def display_matrix(colorspace, format):
    """Display RGB to XYZ matrix corresponding to colorspace and formatting
    as format

    Args:
        colorspace (str): input colorspace. For now, REC709 is the only option.

        format (str): output format. simple, matrix, spimtx.

    """
    print "{0} to XYZ matrix ({1} output):\n".format(colorspace, format)
    try:
        colorspace = COLORSPACES[colorspace]
    except KeyError:
        colorspace = PRIVATE_COLORSPACES[colorspace]
    matrix = get_RGB_to_XYZ_matrix(colorspace.get_red_primaries(),
                                   colorspace.get_green_primaries(),
                                   colorspace.get_blue_primaries(),
                                   colorspace.get_white_point())
    if format == 'simple':
        print ("{0:.10f} {1:.10f} {2:.10f}\n"
               "{3:.10f} {4:.10f} {5:.10f}\n"
               "{6:.10f} {7:.10f} {8:.10f}\n").format(matrix.item(0, 0),
                                                      matrix.item(0, 1),
                                                      matrix.item(0, 2),
                                                      matrix.item(1, 0),
                                                      matrix.item(1, 1),
                                                      matrix.item(1, 2),
                                                      matrix.item(2, 0),
                                                      matrix.item(2, 1),
                                                      matrix.item(2, 2))
    elif format == 'spimtx':
        print ("{0:.10f} {1:.10f} {2:.10f} 0\n"
               "{3:.10f} {4:.10f} {5:.10f} 0\n"
               "{6:.10f} {7:.10f} {8:.10f} 0\n").format(matrix.item(0, 0),
                                                        matrix.item(0, 1),
                                                        matrix.item(0, 2),
                                                        matrix.item(1, 0),
                                                        matrix.item(1, 1),
                                                        matrix.item(1, 2),
                                                        matrix.item(2, 0),
                                                        matrix.item(2, 1),
                                                        matrix.item(2, 2))
    else:
        print matrix


def __get_options():
    """ Return rgb_to_xyz option parser

    Returns:
        .argparse.ArgumentParser.args

    """
    ## Define parser
    description = 'Print RGB -> XYZ matrix'
    parser = argparse.ArgumentParser(description=description)
    # RGB colorspace
    parser.add_argument("-c", "--colorspace",
                        help=("Input RGB Colorspace."),
                        type=str,
                        choices= sorted(COLORSPACES.keys() +
                                        PRIVATE_COLORSPACES.keys()),
                        default='REC709')
    # Output format
    parser.add_argument("-f", "--format",
                        help=("Output formatting."),
                        type=str,
                        choices=['matrix', 'spimtx', 'simple'],
                        default='matrix')
    return parser.parse_args()


if __name__ == '__main__':
    """ Command line interface
    """
    args = __get_options()
    display_matrix(args.colorspace, args.format)
