#!/usr/bin/python

############################
#
# Plot That Lut
# Version : 0.1
# Author : mfe
#
############################

## imports
from os import path
from os import sys
# OpenColorIO
from PyOpenColorIO import Config, ColorSpace, FileTransform
from PyOpenColorIO.Constants import INTERP_NEAREST, INTERP_LINEAR, INTERP_TETRAHEDRAL, COLORSPACE_DIR_TO_REFERENCE
# matplotlib : general plot
from matplotlib.pyplot import title, plot, xlabel, ylabel, grid, show
# matplotlib : for 3D plot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure
from matplotlib.colors import rgb2hex

OCIO_LUTS_FORMATS =     ['.3dl',
                        '.csp',
                        '.cub',
                        '.cube',
                        '.hdl',
                        '.look',
                        '.mga/m3d',
                        '.spi1d',
                        '.spi3d',
                        '.spimtx',
                        '.vf'
                        ]

DEFAULT_SAMPLE = 256
DEFAULT_CUBE_SIZE = 17

"""
createOCIOProcessor
lutfile : path to a LUT
interpolation : can be INTERP_NEAREST, INTERP_LINEAR or INTERP_TETRAHEDRAL (only for 3D LUT)
"""
def createOCIOProcessor(lutfile, interpolation):
    config = Config()
    # In colorspace (LUT)
    colorspace = ColorSpace(name='RawInput')
    t = FileTransform(lutfile,interpolation=interpolation)
    colorspace.setTransform(t, COLORSPACE_DIR_TO_REFERENCE)
    config.addColorSpace(colorspace)
    # Out colorspace
    colorspace = ColorSpace(name='ProcessedOutput')
    config.addColorSpace(colorspace)
    # Create a processor corresponding to the LUT transformation
    return config.getProcessor('RawInput', 'ProcessedOutput')

"""
plotCurve
lutfile : path to a color transformation file (lut, matrix...)
samplesCount : number of points for the displayed curve
"""
def plotCurve(lutfile, samplesCount, processor):
    # init vars
    maxValue = samplesCount - 1.0
    redValues = []
    greenValues = []
    blueValues = []
    inputRange = []
    # process color values
    for n in range(0, samplesCount):
        x = n/maxValue
        res = processor.applyRGB([x,x,x])
        redValues.append(res[0])
        greenValues.append(res[1])
        blueValues.append(res[2])
        inputRange.append(x)
    # init plot
    figure().canvas.set_window_title('Plot That 1D LUT')
    title(path.basename(lutfile))
    xlabel("Input")
    ylabel("Output")
    grid(True)
    # plot curves
    plot(inputRange, redValues, 'r-', label='Red values', linewidth=1)
    plot(inputRange, greenValues, 'g-', label='Green values', linewidth=1)
    plot(inputRange, blueValues, 'b-', label='Blue values', linewidth=1)
    show()

"""
plotCube
lutfile : path to a color transformation file (lut, matrix...)
cubeSize : number of segments. Ex : If set to 17, 17*17*17 points will be displayed
"""
def plotCube(lutfile, cubeSize, processor):
    # init vars
    inputRange  = range(0, cubeSize)
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
                res = processor.applyRGB([normR,normG,normB])
                # append values
                redValues.append(res[0])
                greenValues.append(res[1])
                blueValues.append(res[2])
                # append corresponding color
                colors.append(rgb2hex([normR,normG,normB]))
    # init plot
    fig = figure()
    fig.canvas.set_window_title('Plot That 3D LUT')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')
    ax.set_xlim(min(redValues),max(redValues))
    ax.set_ylim(min(greenValues),max(greenValues))
    ax.set_zlim(min(blueValues),max(blueValues))
    title(path.basename(lutfile))
    # plot 3D values
    ax.scatter(redValues, greenValues, blueValues, c=colors, marker="o")
    show()

def testLUT1D():
    lutfile = "testFiles/identity.csp"
    plotCurve(lutfile, samplesCount=DEFAULT_SAMPLE)

def testLUT3D():
    lutfile = "testFiles/identity.3dl"
    plotCube(lutfile, cubeSize=DEFAULT_CUBE_SIZE)

def dumpSupportedFomats():
    print "Supported LUT formats : " + ', '.join(OCIO_LUTS_FORMATS)

def dumpHelp():
    print "----"
    print "plotThatLut.py <path to a LUT>                               :   dispay a cube ("+ str(DEFAULT_CUBE_SIZE) +" segments) for 3D LUTs and matrixes"
    print "                                                                 or a curve ("+ str(DEFAULT_SAMPLE) +" points) for 1D/2D LUTs.\n"
    print "plotThatLut.py <path to a LUT> curve [points count]          :   display a curve with x points (default value : "+ str(DEFAULT_SAMPLE) +").\n"
    print "plotThatLut.py <path to a LUT> cube [cube size]              :   display a cube with x segments (default value : "+ str(DEFAULT_CUBE_SIZE) +").\n"
    dumpSupportedFomats()

def main():
    if len(sys.argv) < 2:
        print "Syntax error !"
        dumpHelp()
    else:
        lutfile = sys.argv[1]
        # check if LUT format is supported
        fileext = path.splitext(lutfile)[1]
        if not fileext:
            print "Error: Couldn't extract extension in this path : "+ lutfile
            sys.exit(1)
        if fileext not in OCIO_LUTS_FORMATS:
            print "Error: " + fileext + " file format aren't supported."
            dumpSupportedFomats()
            sys.exit(1)
        # create OCIO processor
        processor = createOCIOProcessor(lutfile, INTERP_LINEAR)
        # init args
        if len(sys.argv) == 4:
            # set args from the command line
            plotType = sys.argv[2]
            count = int(sys.argv[3])
        elif len(sys.argv) == 3:
            # set plotType from the command line and init default count
            plotType = sys.argv[2]
            if plotType=='curve':
                count = DEFAULT_SAMPLE
            else:
                count = DEFAULT_CUBE_SIZE
        elif len(sys.argv) == 2:
            # auto-detect args
            if processor.hasChannelCrosstalk() or fileext == '.spimtx':
                plotType = 'cube'
                count = DEFAULT_CUBE_SIZE
            else:
                plotType = 'curve'
                count = DEFAULT_SAMPLE
        else:
            print "Syntax error !"
            dumpHelp()
            sys.exit(1)
        # plot
        print "Plotting a " + plotType + " with " + str(count) + " samples..."
        if plotType=='curve':
            plotCurve(lutfile, count, processor)
        elif plotType=='cube':
            plotCube(lutfile, count, processor)
        else:
            print "Unknown plot type : " + plotType
            print "Plot type should be curve or cube."
            dumpHelp()

if __name__ == '__main__':
    main()