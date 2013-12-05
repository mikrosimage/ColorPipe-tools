#!/usr/bin/python

"""A command line tool for plot_that_lut.

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
import plot_that_lut
import argparse


def __get_options():
    """ Return ptlut option parser

    Returns:
        .argparse.ArgumentParser.args

    """
    ## Define parser
    description = 'PlotThatLUT command line tool'
    parser = argparse.ArgumentParser(description=description)
    # main lut
    parser.add_argument("lutfiles", help=(
        "path to the main LUT to plot.\n{0}"
    ).format(plot_that_lut.supported_formats()), type=str, nargs='+')
    # inverse
    parser.add_argument("-i", "--inverse", help="inverse main lut",
                        action="store_true")
    # display markers
    parser.add_argument("-m", "--markers",
                        help="display markers on curves (useless on cubes)",
                        action="store_true")
    # pre lut
    parser.add_argument("-pre", "--prelutfile", help=(
        "path to a pre LUT.{0}"
    ).format(plot_that_lut.supported_formats()), type=str, default=None)
    # post lut
    parser.add_argument("-post", "--postlutfile", help=(
        "path to a post LUT.\n{0}"
    ).format(plot_that_lut.supported_formats()), type=str, default=None)
    # type
    parser.add_argument("-t", "--plot-type",
                        help=("Plot type. By default, a curve for a 1D/2D LUT "
                        "and a cube for a 3D LUT."),
                        type=str,
                        choices=['auto', 'curve', 'red_curve', 'blue_curve',
                                 'green_curve', 'cube'],
                        default='auto')
    # samples count
    parser.add_argument("-s", "--samples-count", help=(
        "Samples count. Ex : {0} for a curve or {1} for a cube."
    ).format(plot_that_lut.DEFAULT_SAMPLE, plot_that_lut.DEFAULT_CUBE_SIZE),
default=None, type=int)
    ## return args
    return parser.parse_args()


if __name__ == '__main__':
    """ Command line interface for plot_that_lut

    """
    args = __get_options()
    try:
        plot_that_lut.plot_that_lut(args.lutfiles,
                                    args.plot_type,
                                    args.samples_count,
                                    args.inverse,
                                    args.prelutfile,
                                    args.postlutfile,
                                    args.markers)
    except Exception, e:
        print "Watch out !\n%s" % e
