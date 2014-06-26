#!/usr/bin/python

""" A Look Up Table plotting tool based on OpenColorIO and matplotlib.

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import os
# OpenColorIO
from PyOpenColorIO.Constants import INTERP_LINEAR
from utils.ocio_helper import (
    OCIO_LUTS_FORMATS, create_ocio_processor, is_3d_lut
)
from utils.lut_utils import get_3d_list_values
# matplotlib
import matplotlib
import itertools
from utils import matplotlib_helper as mplh
import ntpath


class PlotThatLutException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


DEFAULT_SAMPLE = 256
DEFAULT_CUBE_SIZE = 17


def show_plot(fig, filename):
    """Plot the figure depending on the backend

    Args:
        fig (matplotlib.pyplot.figure): figure to plot

        filename (str): associated lut filename

    Returns:
        str.
            if in web mode, an html string,
            else a void string.

    """
    if mplh.WEB_MODE:
        split_filename = os.path.splitext(filename)
        filename = '{0}{1}'.format(split_filename[0],
                                   split_filename[1].replace(".", "_"))
        # TODO parametrize current_dir
        current_dir = os.path.dirname(os.path.abspath(__file__))
        current_dir = os.path.join(os.path.dirname(current_dir), 'web_app')
        export_path = 'img/export_{0}.png'.format(filename)
        abs_export_path = '{0}/img/export_{1}.png'.format(current_dir,
                                                          filename)
        print abs_export_path
        fig.savefig(abs_export_path)
        return export_path
    else:
        matplotlib.pyplot.show()
        return ""


def plot_curve(lutfiles, samples_count, processors, draw_red_curve=True,
               draw_green_curve=True, draw_blue_curve=True,
               display_markers=False):
    """Plot a lutfile as a curve

    Args:
        lutfiles ([str]): pathes to color transformation files (lut, matrix...)

        samples_count (int): number of points for the displayed curve

        processors ([PyOpenColorIO.config.Processor]): OpenColorIO processors
        for lutfiles

        draw_red_curve (bool): plot red curve only

        draw_green_curve (bool): plot green curve only

        draw_blue_curve (bool): plot blue curve only

        display_markers (bool): should display markers on curve

    Returns:
            str.

    """
    # matplotlib : general plot
    from matplotlib.pyplot import (title, plot, xlabel, ylabel, grid,
                                   figure)

    # init plot
    fig = figure()
    fig.canvas.set_window_title('Plot That 1D LUT')
    figure_title = ""
    for lutfile in lutfiles:
        filename = os.path.basename(lutfile)
        figure_title = "{0}\n{1}".format(figure_title, filename)
    title(figure_title)
    xlabel("Input")
    ylabel("Output")
    grid(True)
    markers_it = itertools.cycle(mplh.MARKERS)
    reds_it = itertools.cycle(mplh.REDS)
    greens_it = itertools.cycle(mplh.GREENS)
    blues_it = itertools.cycle(mplh.BLUES)
    for lutfile, processor in itertools.izip(lutfiles, processors):
        # init vars
        max_value = samples_count - 1.0
        red_values = []
        green_values = []
        blue_values = []
        input_range = []
        # process color values
        for code_value in range(0, samples_count):
            norm_value = code_value / max_value
            res = processor.applyRGB([norm_value, norm_value, norm_value])
            red_values.append(res[0])
            green_values.append(res[1])
            blue_values.append(res[2])
            input_range.append(norm_value)
        # markers
        marker = markers_it.next()
        markersize = 0
        if display_markers:
            markersize = 4
        # plot curves
        labelbase = os.path.splitext(ntpath.basename(lutfile))[0]
        if draw_red_curve:
            if not draw_blue_curve and not draw_green_curve:
                label = labelbase
            else:
                label = "{0} (R)".format(labelbase)
            plot(input_range, red_values, color=reds_it.next(), marker=marker,
                 label=label, linewidth=1, markersize=markersize)
        if draw_green_curve:
            if not draw_blue_curve and not draw_red_curve:
                label = labelbase
            else:
                label = "{0} (G)".format(labelbase)
            plot(input_range, green_values, color=greens_it.next(),
                 marker=marker, label=label, linewidth=1,
                 markersize=markersize)
        if draw_blue_curve:
            if not draw_green_curve and not draw_red_curve:
                label = labelbase
            else:
                label = "{0} (B)".format(labelbase)
            plot(input_range, blue_values, color=blues_it.next(), marker=marker,
                 label=label, linewidth=1, markersize=markersize)
    matplotlib.pyplot.legend(loc=4)
    return show_plot(fig, filename)


def plot_cube(lutfile, cube_size, processor):
    """Plot a lutfile as a cube

    Args:
        lutfile (str): path to a color transformation file (lut, matrix...)

        cube_size (int): number of segments. Ex : If set to 17, 17*17*17
        points will be displayed

        processor (PyOpenColorIO.config.Processor): an OpenColorIO processor
        for lutfile

    Returns:
        str.

    """
    # matplotlib : general plot
    from matplotlib.pyplot import title, figure
    # matplotlib : for 3D plot
    # mplot3d has to be imported for 3d projection
    import mpl_toolkits.mplot3d
    # init vars
    processed_values = get_3d_list_values(cube_size, processor,
                                          hexa_values=True)
    red_values = processed_values['red_values']
    green_values = processed_values['green_values']
    blue_values = processed_values['blue_values']
    input_colors = processed_values['input_colors']
    # init plot
    fig = figure()
    fig.canvas.set_window_title('Plot That 3D LUT')
    axis = fig.add_subplot(111, projection='3d')
    axis.set_xlabel('Red')
    axis.set_ylabel('Green')
    axis.set_zlabel('Blue')
    axis.set_xlim(min(red_values), max(red_values))
    axis.set_ylim(min(green_values), max(green_values))
    axis.set_zlim(min(blue_values), max(blue_values))
    filename = os.path.basename(lutfile)
    title(filename)
    # plot 3D values
    axis.scatter(red_values, green_values, blue_values, c=input_colors,
                 marker="o")
    return show_plot(fig, filename)


def supported_formats():
    """Return supported formats

    Returns:
        str.

    """
    return "Supported LUT formats : {0}".format(', '.join(OCIO_LUTS_FORMATS))


def plot_that_lut(lutfiles, plot_type=None, count=None, inverse=False,
                  prelutfile=None, postlutfile=None, display_markers=False):
    """Plot a lut depending on its type and/or args

    Args:
        lutfiles (str): pathes to color transformation files (lut, matrix...)

    kwargs:
        plot_type (str): possible values are 'curve' or 'cube'

        count: possible values are curve size or curve samples count or 'auto'

        prelutfile (str): path to a pre LUT

        postlutfile (str): path to a post LUT

        display_markers (bool): should display markers on curve

    Raises:
        PlotThatLutException
        Exception from OpenColorIO binding

    """
    if not isinstance(lutfiles, list):
        lutfiles = [lutfiles]
    mplh.set_matplotlib_backend()
    processors = []
    for lutfile in lutfiles:
        # check if LUT format is supported
        fileext = os.path.splitext(lutfile)[1]
        if not fileext:
            raise PlotThatLutException((
                "Error: Couldn't extract extension in this\n"
                "path : {0}"
            ).format(lutfile))
        if fileext not in OCIO_LUTS_FORMATS:
            raise PlotThatLutException("Error: {0} file aren't supported.\n{1}"
                                       .format(fileext, supported_formats()))
        # create OCIO processor
        processors.append(create_ocio_processor(lutfile, INTERP_LINEAR,
                                                inverse, prelutfile,
                                                postlutfile))
    # init args
    if not plot_type or plot_type == 'auto':
        # deduce plot type considering first lutfile
        if is_3d_lut(processors[0], lutfiles[0]):
            plot_type = 'cube'
        else:
            plot_type = 'curve'
    if not count or count == 'auto':
        # set plot_type from the command line and init default count
        if 'curve' in plot_type:
            count = DEFAULT_SAMPLE
        else:
            count = DEFAULT_CUBE_SIZE
    # plot
    print "Plotting a {0} with {1} samples...".format(plot_type, count)
    if 'curve' in plot_type:
        draw_red_curve = True
        draw_green_curve = True
        draw_blue_curve = True
        if 'red' in plot_type:
            # red_curve option
            draw_green_curve = False
            draw_blue_curve = False
        elif 'green' in plot_type:
            # green_curve option
            draw_red_curve = False
            draw_blue_curve = False
        elif 'blue' in plot_type:
            # blue_curve option
            draw_red_curve = False
            draw_green_curve = False
        return plot_curve(lutfiles, count, processors,
                          draw_red_curve=draw_red_curve,
                          draw_green_curve=draw_green_curve,
                          draw_blue_curve=draw_blue_curve,
                          display_markers=display_markers)
    elif plot_type == 'cube':
        # TODO support multiple cubes display
        return plot_cube(lutfiles[0], count, processors[0])
    else:
        raise PlotThatLutException((
            "Unknown plot type : {0}\n"
            "Plot type should be curve or cube.\n"
        ).format(plot_type))
