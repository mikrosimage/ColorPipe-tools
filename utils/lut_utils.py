""" Utility function for LUTS

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import os


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
                norm_r = red/max_value
                norm_g = green/max_value
                norm_b = blue/max_value
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


def write_3d_json_file(filepath, cubesize, processor):
    """Export cube into a json file

    Args:
        filepath (str): out LUT path

        cubesize (int): cube size. Ex: 17, 32...

        processor (PyOpenColorIO.config.Processor): an OpenColorIO processor

    """
    processed_values = get_3d_list_values(cubesize, processor)
    import json
    lutfile = open(filepath, 'w+')
    json.dump(processed_values, lutfile)
    lutfile.close()
