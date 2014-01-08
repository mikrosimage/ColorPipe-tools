""" Christophe Lorenz Colour Cube LUT format (extension .cc) helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import datetime


class CLCCHelperException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


def get_header(cubesize, comment, title, version="v1.0"):
    """Return clcc header

    Args:
        cubesize (int): cube size. Ex: 17, 32...

        comment (str): an optionnal comment

        title (str): title of the LUT

    Kwargs:
        version (str): colour cube version

    Returns:
        .string

    """
    date = datetime.datetime.now()
    header = ("Colour Cube data {4}\n"
              "{4}\n\n"
              "Name\n"
              "{0}\n"
              "Description\n"
              "{1}\n"
              "Input Colour space - RGB=1, CIEXYZ=2, DENSITY=3\n"
              "1\n"
              "Output Colour space - RGB=1, CIEXYZ=2, DENSITY=3\n"
              "1\n"
              "Size x,y,z\n"
              "{2},{2},{2}\n"
              "Name component A\n"
              "component A\n"
              "Name component B\n"
              "component B\n"
              "Name component C\n"
              "component C\n"
              "Creation Date\n"
              "{3}\n"
              "Data\n"
              ).format(title, comment, cubesize, date, version)
    return header


def write_3d_clcc_lut(filename, cubesize, processor,
                      comment="Created with LutLab",
                      title="Colour Cube LUT"):
    """Write a 3D CL CC LUT

    Args:
        filename (str): out LUT path

        cubesize (int): cube size. Ex: 17, 32...

        processor (PyOpenColorIO.config.Processor): an OpenColorIO processor

    Kwargs:
        comment (str): an optionnal comment

        title (str): title of the LUT

    """
    lutfile = open(filename, 'w+')
    # header
    lutfile.write("{0}".format(get_header(cubesize, comment, title)))
    input_range = range(0, cubesize)
    max_value = cubesize - 1.0
    # process color values
    for blue in input_range:
        for green in input_range:
            for red in input_range:
                # get a value between [0..1]
                norm_r = red/max_value
                norm_g = green/max_value
                norm_b = blue/max_value
                # apply correction via OCIO
                res = processor.applyRGB([norm_r, norm_g, norm_b])
                lutfile.write("{0:.10f},{1:.10f},{2:.10f}\n".format(res[0],
                                                              res[1],
                                                              res[2]))
    lutfile.close()
