""" String Matrix helper

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"


def matrix_to_string(matrix, red_offset=None, green_offset=None, blue_offset=None):
    """Return a string version of the matrix

    Args:
        matrix (numpy.matrix (3x3)): matrix to convert
        red_offset, green_offset, blue_offset (float): channel offset in 16bit int (spimtx format)

    Returns:
        string

    """
    return ("{0:.10f} {1:.10f} {2:.10f} {9}\n"
            "{3:.10f} {4:.10f} {5:.10f} {10}\n"
            "{6:.10f} {7:.10f} {8:.10f} {11} \n").format(matrix.item(0, 0),
                                                         matrix.item(0, 1),
                                                         matrix.item(0, 2),
                                                         matrix.item(1, 0),
                                                         matrix.item(1, 1),
                                                         matrix.item(1, 2),
                                                         matrix.item(2, 0),
                                                         matrix.item(2, 1),
                                                         matrix.item(2, 2),
                                                         red_offset is None and "" or red_offset,
                                                         green_offset is None and "" or green_offset,
                                                         blue_offset is None and "" or blue_offset)


def matrix_to_spimtx_string(matrix, red_offset=0, green_offset=0, blue_offset=0):
    """Return a spimtx string version of the matrix

    Args:
        matrix (numpy.matrix (3x3)): matrix to convert
        red_offset, green_offset, blue_offset (float): channel offset in 16bit int

    Returns:
        string

    """
    return matrix_to_string(matrix, red_offset, green_offset, blue_offset)


def write_spimtx(matrix, file_path, red_offset=0, green_offset=0, blue_offset=0):
    f = open(file_path, 'w+')
    f.write(matrix_to_spimtx_string(matrix, red_offset, green_offset, blue_offset))
    f.close()
