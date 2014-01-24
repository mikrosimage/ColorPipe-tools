""" Matplotlib helpers

.. moduleauthor:: `Jeremie Gerhardt <github.com/mrbonsoir>`_ \and
                  `Marie FETIVEAU <github.com/mfe>`_

"""
import matplotlib.pyplot as plt
import numpy as np
import os


def plot_points(x, y, point_type='o', color='gray'):
    """Plot an xy points

    Args:
        x,y (float or [floats]): coords

    kwargs:
        type (str): matplotlib type. Ex: 'o', 'r+'

        color (str): matplotlib color. Ex: green, cyan

    """
    plt.plot(x, y, point_type, color=color)


def plot_triangle(x, y, color=None, draw_lines=True, fill=False):
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
        plt.plot(x[index_val], y[index_val], '-k')

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


def plot_spectrum_locus(data_path):
    """Plot standard spectrum locus

    Args:
        data_path (str): path to a file containing xyz data

    """
    data = np.loadtxt(data_path)
    x = data[:, 1] / (data[:, 1] + data[:, 2] + data[:, 3])
    y = data[:, 2] / (data[:, 1] + data[:, 2] + data[:, 3])
    plt.plot(x, y, 'k-')
    plt.plot(x[[0, x.size - 1]], y[[0, y.size - 1]], 'k:')


def plot_spectrum_locus_31():
    """Plot CIE1931 spectrum locus

    """
    plot_spectrum_locus(SPECTRUM_LOCUS_31)


def plot_spectrum_locus_64():
    """Plot CIE1964 spectrum locus

    """
    plot_spectrum_locus(SPECTRUM_LOCUS_64)


def plot_colorspace_gamut(colorspace, color=None, draw_lines=True, fill=False):
    """Plot colorspace primaries triangle

    Args:
        colorspace (utils.colorspace)

    kwargs:
        color (str): if none, 1st point--> red, 2nd --> green, 3rd -> blue

        drawLines (bool): draw outline

        fill (bool): fill triangle

    """
    red_x, red_y = colorspace.get_red_primaries()
    green_x, green_y = colorspace.get_green_primaries()
    blue_x, blue_y = colorspace.get_blue_primaries()
    plot_triangle(np.array([red_x, green_x, blue_x]),
                  np.array([red_y, green_y, blue_y]),
                  color, draw_lines, fill)
