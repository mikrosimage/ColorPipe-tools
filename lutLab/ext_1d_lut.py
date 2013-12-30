#!/usr/bin/python

""" Extract 1D composante of a 3D LUT

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import argparse
from utils.ocio_helper import (
    OCIO_3D_LUTS_FORMATS, create_ocio_processor, is_3d_lut
)
from utils.csp_helper import write_2d_csp_lut
from utils.lut_utils import get_default_out_path

from scipy.interpolate import PchipInterpolator
import numpy


class Ext1DLutException(Exception):
    pass


def extract_1d_lut(inlutfile, lutsize, outlutfile=None, smooth=False,
                   smooth_size=17, display=False):
    """Extract the tone mapping curve of a 3D LUT

    Args:
        inlutfile (str): an input 3D LUT

        lutsize (int): out 1D LUT bit precision. Ex : 16 (bits)

    Kwargs:
        outlutfile (str): the output 1D lut. If not define, LUT is written in
        the input LUT directory and post-fixed with "_export"

        smooth (bool): smooth the resulting curve with a bicubic monotonic
        interpolation. See also smooth_size.

        smooth_size (int): only used when smooth is true. Specify how many
        points are sampled using OpenColorIO processor. The result curve is then
        smoothed and resample to fit input lutsize.
        So the smaller this value is, the smoother the curve will be.

    """
    if not outlutfile:
        outlutfile = get_default_out_path(inlutfile, ".csp")
    # create OCIO processor
    processor = create_ocio_processor(inlutfile)
    if not is_3d_lut(processor, inlutfile):
        raise Ext1DLutException("Input lut must be a 3D LUT !")
    # init vars
    if smooth:
        # subsample OCIO processed curve
        count = smooth_size
    else:
        count = pow(2, lutsize)
    max_value = count - 1.0
    red_values = []
    green_values = []
    blue_values = []
    for n in range(0, count):
        x = n/max_value
        res = processor.applyRGB([x, x, x])
        red_values.append(res[0])
        green_values.append(res[1])
        blue_values.append(res[2])
    if smooth:
        # get full range
        xnew = numpy.arange(0, max_value, float(count-1)/(pow(2, lutsize)))
        # get a monotonic cubic function from subsampled curve
        red_cubic_monotonic_func = PchipInterpolator(numpy.arange(0, count),
                                                     red_values)
        green_cubic_monotonic_func = PchipInterpolator(numpy.arange(0, count),
                                                       green_values)
        blue_cubic_monotonic_func = PchipInterpolator(numpy.arange(0, count),
                                                      blue_values)
        # sample on the full range
        reds = red_cubic_monotonic_func(xnew)
        greens = green_cubic_monotonic_func(xnew)
        blues = blue_cubic_monotonic_func(xnew)
    else:
        reds = red_values
        greens = green_values
        blues = blue_values
    write_2d_csp_lut(outlutfile, reds, greens, blues)
    if display:
        try:
        # init plot
            from matplotlib.pyplot import (title, plot, grid,
                                           figure, show)
        except:
            raise Ext1DLutException("Install matplotlib to use display option")

        fig = figure()
        fig.canvas.set_window_title('Plot That 1D LUT')

        title("Compare")
        grid(True)
        # plot curves
        plot(reds, 'r-', label='numpy', linewidth=1)
        plot(greens, 'g-', label='numpy', linewidth=1)
        plot(blues, 'b-', label='numpy', linewidth=1)
        show()


def __get_options():
    """ Return ext_1d_lut option parser

    Returns:
        .argparse.ArgumentParser.args

    """
    ## Define parser
    description = 'Extract 1D composante of a 3D LUT'
    parser = argparse.ArgumentParser(description=description)
    # input 3D lut file
    parser.add_argument("inlutfile", help=(
        "path to a 3D LUT.\n{0}"
    ).format(str(OCIO_3D_LUTS_FORMATS)), type=str)
    # output lut
    parser.add_argument("-out", "--outlutfile", help=(
        "export path of the extracted (.csp) 1D LUT."
    ), type=str, default=None)
    # out lut size
    parser.add_argument("-os", "--outlut-size", help=(
        "Output lut bit precision. Ex : 10, 16, 32."
    ), default=16, type=int)
    # Smooth
    parser.add_argument("-sm", "--smooth", help="Smooth resulting LUT",
                        action="store_true")
    # out lut size
    parser.add_argument("-sms", "--smooth-size", help=(
        "Smooth sub-sampling size. Ex : 17"
    ), default=17, type=int)
    # Display curves
    parser.add_argument("-d", "--display",
                        help="Display result using matplotlib",
                        action="store_true")
    return parser.parse_args()

if __name__ == '__main__':
    """ Command line interface
    """
    args = __get_options()
    extract_1d_lut(args.inlutfile, args.outlut_size, args.outlutfile,
                   args.smooth, args.smooth_size, args.display)
