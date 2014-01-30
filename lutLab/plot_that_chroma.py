""" A chroma plotting tool based on matplotlib.

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import argparse
import matplotlib.pyplot as plt
from utils import matplotlib_helper as mplh
from utils.colorspaces import COLORSPACES
from utils.private_colorspaces import PRIVATE_COLORSPACES
import itertools


class PlotThatChromaException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


def plot_that_chroma(colorspaces):
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
            print colorspace
            try:
                merged_dict = dict(COLORSPACES, **PRIVATE_COLORSPACES)
                colorspace_obj = merged_dict[colorspace]
            except KeyError:
                raise PlotThatChromaException(("Unsupported {0} Colorspace !").
                                              format(colorspace))
            mplh.plot_colorspace_gamut(colorspace_obj,
                                       lines_color=colors_it.next())
    plt.legend(loc=4)
    plt.show()


def __get_options():
    """Return plot that chroma option parser

    Returns:
        .argparse.ArgumentParser.args

    """
    ## Define parser
    description = 'Create lut file corresponding to a colorspace gradation'
    parser = argparse.ArgumentParser(description=description)
    # RGB colorspace
    parser.add_argument("-space", "--colorspace",
                        help=("RGB Colorspace."),
                        type=str, action='append', dest='colorspaces',
                        choices=sorted(COLORSPACES.keys() +
                                        PRIVATE_COLORSPACES.keys()))
    return parser.parse_args()

if __name__ == '__main__':
    ARGS = __get_options()
    plot_that_chroma(ARGS.colorspaces)
