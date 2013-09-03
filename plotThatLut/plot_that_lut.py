#!/usr/bin/python

############################
#
# Plot That Lut
# Version : 0.2
# Author : mfe
#
############################

## imports
from os import path
from os import sys
# OpenColorIO
from PyOpenColorIO import Config, ColorSpace, FileTransform
from PyOpenColorIO.Constants import INTERP_LINEAR, COLORSPACE_DIR_TO_REFERENCE
# matplotlib
import matplotlib

cherry_py_mode = True


def setMatplotlibBackend():
    if cherry_py_mode:
        matplotlib.use('Agg')
    else:
        matplotlib.use('Qt4Agg')

OCIO_LUTS_FORMATS = ['.3dl', '.csp', '.cub', '.cube', '.hdl', '.look',
                     '.mga/m3d', '.spi1d', '.spi3d', '.spimtx', '.vf']

DEFAULT_SAMPLE = 256
DEFAULT_CUBE_SIZE = 17


def showPlot(fig, filename):
    if cherry_py_mode:
        splitFilename = path.splitext(filename)
        filename = '{0}{1}'.format(splitFilename[0],
                                   splitFilename[1].replace(".", "_"))
        exportPath = 'img/export_{0}.png'.format(filename)
        fig.savefig(exportPath)
        return """
               <img src="/{0}"" width="640" height="480"
               border="0"/>
               """.format(exportPath)
    else:
        matplotlib.pyplot.show()
        return ""


def createOCIOProcessor(lutfile, interpolation):
    """
    Create an OpenColorIO processor for lutfile

    Keyword arguments:
    lutfile -- path to a LUT
    interpolation -- can be INTERP_NEAREST, INTERP_LINEAR or
    INTERP_TETRAHEDRAL (only for 3D LUT)

    """
    config = Config()
    # In colorspace (LUT)
    colorspace = ColorSpace(name='RawInput')
    t = FileTransform(lutfile, interpolation=interpolation)
    colorspace.setTransform(t, COLORSPACE_DIR_TO_REFERENCE)
    config.addColorSpace(colorspace)
    # Out colorspace
    colorspace = ColorSpace(name='ProcessedOutput')
    config.addColorSpace(colorspace)
    # Create a processor corresponding to the LUT transformation
    return config.getProcessor('RawInput', 'ProcessedOutput')


def plotCurve(lutfile, samplesCount, processor):
    """
    plot lutfile as a curve

    Keyword arguments:
    lutfile -- path to a color transformation file (lut, matrix...)
    samplesCount -- number of points for the displayed curve

    """
    # matplotlib : general plot
    from matplotlib.pyplot import (title, plot, xlabel, ylabel, grid,
                                   figure)
    # init vars
    maxValue = samplesCount - 1.0
    redValues = []
    greenValues = []
    blueValues = []
    inputRange = []
    # process color values
    for n in range(0, samplesCount):
        x = n/maxValue
        res = processor.applyRGB([x, x, x])
        redValues.append(res[0])
        greenValues.append(res[1])
        blueValues.append(res[2])
        inputRange.append(x)
    # init plot
    fig = figure()
    fig.canvas.set_window_title('Plot That 1D LUT')
    filename = path.basename(lutfile)
    title(filename)
    xlabel("Input")
    ylabel("Output")
    grid(True)
    # plot curves
    plot(inputRange, redValues, 'r-', label='Red values', linewidth=1)
    plot(inputRange, greenValues, 'g-', label='Green values', linewidth=1)
    plot(inputRange, blueValues, 'b-', label='Blue values', linewidth=1)
    return showPlot(fig, filename)


def plotCube(lutfile, cubeSize, processor):
    """
    plot lutfile as a cubue

    Keyword arguments:
    lutfile -- path to a color transformation file (lut, matrix...)
    cubeSize -- number of segments. Ex : If set to 17, 17*17*17 points will be
    displayed

    """
    # matplotlib : general plot
    from matplotlib.pyplot import title, figure
    # matplotlib : for 3D plot
    # mplot3d has to be imported for 3d projection
    import mpl_toolkits.mplot3d
    from matplotlib.colors import rgb2hex
    # init vars
    inputRange = range(0, cubeSize)
    maxValue = cubeSize - 1.0
    redValues = []
    greenValues = []
    blueValues = []
    colors = []
    # process color values
    for r in inputRange:
        for g in inputRange:
            for b in inputRange:
                # get a value between [0..1]
                normR = r/maxValue
                normG = g/maxValue
                normB = b/maxValue
                # apply correction via OCIO
                res = processor.applyRGB([normR, normG, normB])
                # append values
                redValues.append(res[0])
                greenValues.append(res[1])
                blueValues.append(res[2])
                # append corresponding color
                colors.append(rgb2hex([normR, normG, normB]))
    # init plot
    fig = figure()
    fig.canvas.set_window_title('Plot That 3D LUT')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')
    ax.set_xlim(min(redValues), max(redValues))
    ax.set_ylim(min(greenValues), max(greenValues))
    ax.set_zlim(min(blueValues), max(blueValues))
    filename = path.basename(lutfile)
    title(filename)
    # plot 3D values
    ax.scatter(redValues, greenValues, blueValues, c=colors, marker="o")
    return showPlot(fig, filename)


def testLUT1D():
    lutfile = "testFiles/identity.csp"
    plotCurve(lutfile, samplesCount=DEFAULT_SAMPLE)


def testLUT3D():
    lutfile = "testFiles/identity.3dl"
    plotCube(lutfile, cubeSize=DEFAULT_CUBE_SIZE)


def supportedFormats():
    return "Supported LUT formats : {0}".format(', '.join(OCIO_LUTS_FORMATS))


def help():
    return """
----
plotThatLut.py <path to a LUT>
            dispay a cube ({0} segments) for 3D LUTs and matrixes
            or a curve ({1} points) for 1D/2D LUTs.

plotThatLut.py <path to a LUT> curve [points count]
            display a curve with x points (default value : {2}).

plotThatLut.py <path to a LUT> cube [cube size]
            display a cube with x segments (default value : {3}).

{4}
           """.format(DEFAULT_CUBE_SIZE, DEFAULT_SAMPLE, DEFAULT_SAMPLE,
                      DEFAULT_CUBE_SIZE, supportedFormats())


def plotThatLut(lutfile, plotType=None, count=None):
    setMatplotlibBackend()
    # check if LUT format is supported
    fileext = path.splitext(lutfile)[1]
    if not fileext:
        raise Exception("""
Error: Couldn't extract extension in this
path : {0}
                        """.format(lutfile))
    if fileext not in OCIO_LUTS_FORMATS:
        raise Exception("Error: {0} file format aren't supported.\n{1}"
                        .format(fileext, supportedFormats()))
    # create OCIO processor
    processor = createOCIOProcessor(lutfile, INTERP_LINEAR)
    # init args
    if not plotType or plotType == 'auto':
        if processor.hasChannelCrosstalk() or fileext == '.spimtx':
            plotType = 'cube'
        else:
            plotType = 'curve'
    if not count or count == 'auto':
        # set plotType from the command line and init default count
        if plotType == 'curve':
            count = DEFAULT_SAMPLE
        else:
            count = DEFAULT_CUBE_SIZE
    # plot
    print "Plotting a {0} with {1} samples...".format(plotType, count)
    if plotType == 'curve':
        return plotCurve(lutfile, count, processor)
    elif plotType == 'cube':
        return plotCube(lutfile, count, processor)
    else:
        raise Exception("""Unknown plot type : {0}
Plot type should be curve or cube.\n{1}
                        """.format(plotType, help()))

if __name__ == '__main__':
    cherry_py_mode = False
    paramsCount = len(sys.argv)
    lutfile = ""
    plotType = None
    count = None
    if paramsCount < 2:
        print "Syntax error !"
        print help()
        sys.exit(1)
    elif paramsCount == 2:
        lutfile = sys.argv[1]
    elif paramsCount == 3:
        lutfile = sys.argv[1]
        plotType = sys.argv[2]
    elif paramsCount == 4:
        lutfile = sys.argv[1]
        plotType = sys.argv[2]
        count = int(sys.argv[3])
    else:
        print "Syntax error !"
        print help()
        sys.exit(1)
    try:
        plotThatLut(lutfile, plotType, count)
    except Exception, e:
        print "Watch out !\n%s"% e
