#!/usr/bin/python
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
plot1DLUT
lutfile : path to a LUT
samplesCount : number of points for the displayed curve
"""
def plot1DLUT(lutfile, samplesCount):
    # create OCIO processor
    processor = createOCIOProcessor(lutfile, INTERP_LINEAR)
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
plot3DLUT
lutfile : path to a LUT
cubeSize : number of segments. Ex : If set to 17, 17*17*17 points will be displayed
"""
def plot3DLUT(lutfile, cubeSize):
    # create OCIO processor
    processor = createOCIOProcessor(lutfile, INTERP_TETRAHEDRAL)
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
    plot1DLUT(lutfile, samplesCount=256)

def testLUT3D():
    lutfile = "testFiles/identity.3dl"
    plot3DLUT(lutfile, cubeSize=17)

def dumpSupportedFomats():
    print "Supported LUT formats : " + ', '.join(OCIO_LUTS_FORMATS)

def dumpHelp():
    print "--- Help ---"
    dumpSupportedFomats()
    print "How to plot : "
    print "* To plot a 1D LUT : ./plotThatLut.py <path to a lut> 1D <samples count>"
    print "* To plot a 3D LUT : ./plotThatLut.py <path to a lut> 3D <cube size>"
    print "ex :"
    print "./plotThatLut.py testFiles/identity.csp 1D 256"
    print "./plotThatLut.py testFiles/identity.3dl 3D 17"

def main():
    if len(sys.argv) < 4:
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
        # set Args from the command line
        lutType = sys.argv[2]
        count = int(sys.argv[3])
        if lutType=='1D':
            plot1DLUT(lutfile, count)
        elif lutType=='3D':
            plot3DLUT(lutfile, count)
        else:
            print "Unknown LUT tppe : " + lutType
            print "LUT type should be 1D or 3D."
            dumpHelp()

if __name__ == '__main__':
    main()