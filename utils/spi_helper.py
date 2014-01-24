""" Spi LUT helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"


class SpiHelperException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


def write_1d_spi_lut(filename, values, input_range=None, version=1):
    """ Write a 1D spi LUT

    Args:
        filename (str): out LUT path

        values (float array): values

    Kwargs:
        input_range ([nb, nb]): input range

        version (float): version of the lut

    """
    if input_range == None:
        input_range = [0, 1]
    lutfile = open(filename, 'w+')
    lutfile.write("Version {0}\n".format(version))
    lutfile.write("From {0} {1}\n".format(input_range[0], input_range[1]))
    lutfile.write("Length {0}\n".format(len(values)))
    # TODO handle more than one component
    lutfile.write("Components 1\n")
    lutfile.write("{\n")
    for value in values:
        lutfile.write("\t\t{0:.8f}\n".format(value))
    lutfile.write("}\n")
    lutfile.close()
