""" Cube (Iridas LUTs) helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
import itertools
from utils.lut_utils import check_arrays_length


class CubeHelperException(Exception):
    pass

CUBE_1D = "LUT_1D_SIZE"
CUBE_3D = "LUT_3D_SIZE"


def write_2d_cube_lut(filename, xvalues, yvalues=None, zvalues=None,
                      comment=None, title="Cube LUT"):
    """Write a 2D Cube LUT

    Args:
        filename (str): out LUT path

        xvalues (float array): 1st channel values

    Kwargs:
        yvalues (float array): 2nd channel values

        zvalues (float array): 3rd channel values

        comment (str): an optionnal comment

        title (str): title of the LUT

    """
    if yvalues and zvalues:
        # 2D lut
        check_arrays_length(xvalues, yvalues, zvalues)
    else:
        # 1D lut
        yvalues = xvalues
        zvalues = xvalues

    f = open(filename, 'w+')
    # comment
    if comment:
        f.write("#{0}\n".format(comment))
    # title
    f.write("TITLE {0}\n\n".format(title))
    # lut size
    f.write("{0} {1}\n\n".format(CUBE_1D, len(xvalues)))
    # values
    for x, y, z in itertools.izip(xvalues, yvalues, zvalues):
        f.write("{0:.6f} {1:.6f} {2:.6f}\n".format(x, y, z))
    f.close()


def write_1d_cube_lut(filename, values, comment=None, title="Iridas LUT"):
    """ Write a 1D Cube LUT

    Args:
        filename (str): out LUT path

        xvalues (float array): 1st channel values

    Kwargs:
        comment (str): an optionnal comment

        title (str): title of the LUT
    """
    write_2d_cube_lut(filename, values, comment, title)


def write_3d_cube_lut(filename, cubesize, processor,
                      comment=None, title="Cube LUT"):
    """Write a 3D Cube LUT

    Args:
        filename (str): out LUT path

        cubesize (int): cube size. Ex: 17, 32...

        processor (PyOpenColorIO.config.Processor): an OpenColorIO processor

    Kwargs:
        comment (str): an optionnal comment

        title (str): title of the LUT

    """
    f = open(filename, 'w+')
    # comment
    if comment:
        f.write("#{0}\n".format(comment))
    # title
    f.write("TITLE {0}\n\n".format(title))
    # lut size
    f.write("{0} {1}\n\n".format(CUBE_3D, cubesize))
    input_range = range(0, cubesize)
    max_value = cubesize - 1.0
    # process color values
    for b in input_range:
        for g in input_range:
            for r in input_range:
                # get a value between [0..1]
                norm_r = r/max_value
                norm_g = g/max_value
                norm_b = b/max_value
                # apply correction via OCIO
                res = processor.applyRGB([norm_r, norm_g, norm_b])
                f.write("{0:.6f} {1:.6f} {2:.6f}\n".format(res[0],
                                                           res[1],
                                                           res[2]))
    f.close()
