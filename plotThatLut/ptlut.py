#!/usr/bin/python

"""A command line tool for plot_that_lut.

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
import sys
import plot_that_lut


def help():
    """Return help

    Returns:
        str.

    """
    return (
        "----\n"
        "plot_that_lut.py <path to a LUT>\n"
        "       dispay a cube ({0} segments) for 3D LUTs and matrixes\n"
        "       or a curve ({1} points) for 1D/2D LUTs.\n"

        "plot_that_lut.py <path to a LUT> curve [points count]\n"
        "       display a curve with x points (default value : {2}).\n"
        "       plot_that_lut.py <path to a LUT> cube [cube size]\n"
        "       display a cube with x segments (default value : {3}).\n"
        "\n{4}"
    ).format(plot_that_lut.DEFAULT_CUBE_SIZE, plot_that_lut.DEFAULT_SAMPLE,
             plot_that_lut.DEFAULT_SAMPLE, plot_that_lut.DEFAULT_CUBE_SIZE,
             plot_that_lut.supported_formats())

if __name__ == '__main__':
    """ Command line interface for plot_that_lut

    .. todo:: use optparse (or argparse)

    """
    plot_that_lut.web_mode = False
    params_count = len(sys.argv)
    lutfile = ""
    plot_type = None
    count = None
    if params_count < 2:
        print "Syntax error !"
        print help()
        sys.exit(1)
    elif params_count == 2:
        lutfile = sys.argv[1]
    elif params_count == 3:
        lutfile = sys.argv[1]
        plot_type = sys.argv[2]
    elif params_count == 4:
        lutfile = sys.argv[1]
        plot_type = sys.argv[2]
        count = int(sys.argv[3])
    else:
        print "Syntax error !"
        print help()
        sys.exit(1)
    try:
        plot_that_lut.plot_that_lut(lutfile, plot_type, count,
                                    helpMessage=help())
    except Exception, e:
        print "Watch out !\n%s" % e
