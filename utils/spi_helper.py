""" Spi LUT helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""


class SpiHelperException(Exception):
    pass


def write_1d_spi_lut(filename, values, input_range=[0, 1], version=1):
    """ Write a 1D spi LUT

    Args:
        filename (str): out LUT path

        values (float array): values

    Kwargs:
        input_range ([nb, nb]): input range

        version (float): version of the lut

    """
    f = open(filename, 'w+')
    f.write("Version {0}\n".format(version))
    f.write("From {0} {1}\n".format(input_range[0], input_range[1]))
    f.write("Length {0}\n".format(len(values)))
    # TODO handle more than one component
    f.write("Components 1\n")
    f.write("{\n")
    for x in values:
        f.write("\t\t{0:.8f}\n".format(x))
    f.write("}\n")
    f.close()
