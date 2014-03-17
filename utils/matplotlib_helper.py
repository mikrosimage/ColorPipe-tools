""" Matplotlib helpers

.. moduleauthor:: `Jeremie Gerhardt <github.com/mrbonsoir>`_ \and
                  `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.2"
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from utils import colors_helper as coh
from utils.colorspaces import sRGB
import os

WEB_MODE = False
MARKERS = ['o', '*', 'H', 'D', '8', 's', 'p', 'h', 'd']
REDS = ['r', 'c', '#990000', '#660000']
GREENS = ['g', 'm', '#009900', '#006600']
BLUES = ['b', 'y', '#000099', '#000066']
COLORS = ['c', 'm', 'y', '#FF8200', '#8C00FF', '#EF8AF2', '#71B3F5']


def set_matplotlib_backend():
    """Select display backend

    .. todo:: Externalize this and remove WEB_MODE global var

    """
    if WEB_MODE:
        matplotlib.use('Agg')
    else:
        matplotlib.use('Qt4Agg')


def get_matplotlib_color(x, y):
    R, G, B = coh.xy_to_RGB([x, y], sRGB, clamp=True)
    return (R, G, B)


def plot_points(x, y, point_type='o', color='auto'):
    """Plot an xy points

    Args:
        x,y (float or [floats]): coords

    kwargs:
        type (str): matplotlib type. Ex: 'o', 'r+'

        color (str): matplotlib color. Ex: green, cyan. If 'auto', color is
        computed from x,y coords

    """
    if color == 'auto':
        if isinstance(x, list):
            color = 'gray'
        else:
            color = get_matplotlib_color(x, y)
    plt.plot(x, y, point_type, color=color)


def plot_triangle(x, y, color=None, draw_lines=True, lines_color='black',
                  fill=False, label=""):
    """Plot an rgb triangle in xy

    Args:
        x,y (numpy.array): [r, g, b] coords

    kwargs:
        color (str): if none, 1st point--> red, 2nd --> green, 3rd -> blue

        drawLines (bool): draw outline

        fill (bool): fill triangle

    """
    if fill:
        plt.fill(x, y, color='grey', alpha='0.5')
    if draw_lines:
        index_val = np.hstack([np.arange(x.size), 0])
        plt.plot(x[index_val], y[index_val], color=lines_color, label=label)

    if color:
        plt.plot(x[0], y[0], 'o', x[1], y[1], 'o', x[2], y[2], 'o',
                 color=color)
    else:
        plt.plot(x[0], y[0], 'or', x[1], y[1], 'og', x[2], y[2], 'ob')


SPECTRUM_DATA_PATH = os.path.join(os.path.dirname(__file__), 'rsrc')
SPECTRUM_LOCUS_31 = os.path.join(SPECTRUM_DATA_PATH,
                                 'spectrum_locus_xyz1931.txt')
SPECTRUM_LOCUS_64 = os.path.join(SPECTRUM_DATA_PATH,
                                 'spectrum_locus_xyz1964.txt')


def load_xy_from_file(data_path):
    """Use numpy to load coordinates from file

    Args:
        data_path (str): path to a file containing xy data

    Returns:
        .[float, float]

    """
    data = np.loadtxt(data_path)
    x = data[:, 4]
    y = data[:, 5]
    return [x, y]


def plot_spectrum_locus(x, y, label):
    """Plot standard spectrum locus

    Args:
        data_path (str): path to a file containing xyz data

    """
    plt.plot(x, y, 'k-', label=label)
    plt.plot(x[[0, x.size - 1]], y[[0, y.size - 1]], 'k-')


def plot_spectrum_locus_31():
    """Plot CIE1931 spectrum locus

    """
    x, y = load_xy_from_file(SPECTRUM_LOCUS_31)
    plot_spectrum_locus(x, y, "spectrum locus CIE1931")


def plot_spectrum_locus_64():
    """Plot CIE1964 spectrum locus

    """
    x, y = load_xy_from_file(SPECTRUM_LOCUS_64)
    plot_spectrum_locus(x, y, "spectrum locus CIE1964")


def plot_spectrum_locus_76():
    """Plot CIE1976 spectrum locus

    """
    # Load CIE 1931 data
    x_list, y_list = load_xy_from_file(SPECTRUM_LOCUS_31)
    up_list = []
    vp_list = []
    # Convert data from xy to u'v"
    for x, y in zip(x_list, y_list):
        up, vp = coh.xy_to_upvp([x, y])
        up_list.append(up)
        vp_list.append(vp)
    up_list = np.array(up_list)
    vp_list = np.array(vp_list)
    # Plot resulting data
    plot_spectrum_locus(up_list, vp_list, "spectrum locus CIE1976")


def plot_colorspace_gamut(colorspace, color=None, draw_lines=True,
                          lines_color='black', fill=False,
                          upvp_conversion=False):
    """Plot colorspace primaries triangle

    Args:
        colorspace (utils.colorspace)

    kwargs:
        color (str): if none, 1st point--> red, 2nd --> green, 3rd -> blue

        drawLines (bool): draw outline

        fill (bool): fill triangle

        upvp_coords (bool): if true, convert x,y values into u'v' values

    """
    red_x, red_y = colorspace.get_red_primaries()
    green_x, green_y = colorspace.get_green_primaries()
    blue_x, blue_y = colorspace.get_blue_primaries()
    if upvp_conversion:
        red_x, red_y = coh.xy_to_upvp([red_x, red_y])
        green_x, green_y = coh.xy_to_upvp([green_x, green_y])
        blue_x, blue_y = coh.xy_to_upvp([blue_x, blue_y])
    plot_triangle(np.array([red_x, green_x, blue_x]),
                  np.array([red_y, green_y, blue_y]),
                  color, draw_lines, lines_color, fill,
                  colorspace.__class__.__name__)
