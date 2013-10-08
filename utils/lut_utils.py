""" Utility function for LUTS

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
import os


class LUTException(Exception):
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

    Returns:
        .str

    """
    split_filename = os.path.splitext(filepath)
    return "{0}_export{1}".format(split_filename[0], ext)
