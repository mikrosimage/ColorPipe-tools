""" Utility function for LUTS

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.4"
import os
import ntpath
import math


class LUTException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


def check_arrays_length(array1, array2, array3):
    """ Check if the 3 arrays have the same length

    Args:
        array1: first array
        array2: second array
        array3: third array

    Raise:
        LUTException when arrays have different lengths

    """
    if (len(array1) != len(array2)) or (len(array2) != len(array3)):
        raise LUTException((
            "2D LUT inconsistency : arrays should have the same length.\n"
            "Found : array1({0}) Array2({1}) Array3({2})".format(len(array1),
                                                                 len(array2),
                                                                 len(array3))
        ))


def get_default_out_path(filepath, ext):
    """ Return a defaut output LUT path from an input LUT path

    Args:
        filepath (str): input LUT file path
        ext (str): output file extension

    Returns:
        .str

    """
    split_filename = os.path.splitext(filepath)
    return "{0}_export{1}".format(split_filename[0], ext)


def get_3d_list_values(cubesize, processor, hexa_values=False):
    """Process cube values

    Args:
        filepath (str): out LUT path

        cubesize (int): cube size. Ex: 17, 32...

        processor (PyOpenColorIO.config.Processor): an OpenColorIO processor

    Kwargs:
        hexa_values (bool): if true, input colors will be hexa values and rgb
        float triplets if false

    Returns:
        .dict containing cubesize and red, green, blue, input color values
        as lists

    TODO Use by plot_that_lut, to remove someday

    """
    input_range = range(0, cubesize)
    max_value = cubesize - 1.0
    red_values = []
    green_values = []
    blue_values = []
    input_colors = []
    if hexa_values:
        from matplotlib.colors import rgb2hex
    # process color values
    for blue in input_range:
        for green in input_range:
            for red in input_range:
                # get a value between [0..1]
                norm_r = red / max_value
                norm_g = green / max_value
                norm_b = blue / max_value
                # apply correction via OCIO
                res = processor.applyRGB([norm_r, norm_g, norm_b])
                red_values.append(res[0])
                green_values.append(res[1])
                blue_values.append(res[2])
                # append corresponding input color
                if hexa_values:
                    color = rgb2hex([norm_r, norm_g, norm_b])
                else:
                    color = [norm_r, norm_g, norm_b]
                input_colors.append(color)
    return {'cubesize': cubesize,
            'red_values': red_values,
            'green_values': green_values,
            'blue_values': blue_values,
            'input_colors': input_colors
            }


def check_extension(filepath, extension):
    """Raise an exception if filepath doesn't match extention

    Args:
        filepath (str): path

        extension (str): extension. Ex: .csp

    """
    if not filepath.lower().endswith(extension.lower()):
        raise LUTException(("File path \'{0}\' doesn't match "
                            "extension \'{1}\'").format(filepath, extension))


def int_scale_range(values, out_value, in_value=1.0):
    """Scale a range of values

    Args:
        values (array): range to convert

        out_value (int): max out value

    kwargs:
        in_value (int): input range max value

    """
    return [int(value / float(in_value) * out_value) for value in values]


def get_file_shortname(file_path):
    """ Get file name (without ext and path)

    Returns:
        .str
    """
    return os.path.splitext(ntpath.basename(file_path))[0]


def get_bitdepth(max_value):
    """ Return bitdepth from max value

    Args:
        max_value (int): ex, 1023, 4095...

    Return:
        .int

    """
    return int(math.log(max_value + 1, 2))
