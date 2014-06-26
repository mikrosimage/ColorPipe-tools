""" A chroma plotting tool based on matplotlib.

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.2"
import argparse
import matplotlib.pyplot as plt
from utils import matplotlib_helper as mplh
from utils.colorspaces import COLORSPACES
from utils.private_colorspaces import PRIVATE_COLORSPACES
import itertools
import sys


class PlotThatChromaException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


def plot_that_chroma(colorspaces, points, display_spectrum=False):
    """Plot chromaticities

    Args:
        colorspaces [colorspace]: a list of standard colorspaces

    """
    # Init diagram
    plt.xlabel('chromaticity x')
    plt.ylabel('chromaticity y')
    plt.title("Standard Gamut")
    plt.grid(True)
    if colorspaces:
        # Init option
        colors_it = itertools.cycle(mplh.COLORS)
        for colorspace in colorspaces:
            try:
                merged_dict = dict(COLORSPACES, **PRIVATE_COLORSPACES)
                colorspace_obj = merged_dict[colorspace]
            except KeyError:
                raise PlotThatChromaException(("Unsupported {0} Colorspace !").
                                              format(colorspace))
            mplh.plot_colorspace_gamut(colorspace_obj,
                                       lines_color=colors_it.next())
    if points:
        for point in points:
            mplh.plot_points(point[0], point[1])
    if display_spectrum:
        mplh.plot_spectrum_locus_31()
    plt.legend(loc=4)
    plt.show()


def __get_options():
    """Return plot that chroma option parser

    Returns:
        .argparse.ArgumentParser.args

    """
    # Define parser
    description = 'Plot chromaticities in a xy or u\'v\' diagram'
    parser = argparse.ArgumentParser(description=description)
    # RGB colorspace
    parser.add_argument("-space", "--colorspace",
                        help=("RGB Colorspace."),
                        type=str, action='append', dest='colorspaces',
                        choices=sorted(COLORSPACES.keys() +
                                       PRIVATE_COLORSPACES.keys()))
    # Points
    parser.add_argument("-p", "--point", type=float, nargs=2,
                        metavar=('x', 'y'), action='append',
                        dest='points', help='Display an xy point')
    # Spectrum locus
    parser.add_argument("-spectrum", "--spectrum-locus", action="store_true",
                        help="Display spectrum locus")
    return parser

if __name__ == '__main__':
    PARSER = __get_options()
    ARGS = PARSER.parse_args()
    if len(sys.argv) < 2:
        print "No option found !"
        PARSER.print_help()
    else:
        plot_that_chroma(ARGS.colorspaces, ARGS.points, ARGS.spectrum_locus)
