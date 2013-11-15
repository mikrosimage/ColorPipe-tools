""" Colors helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""


def xy_to_XYZ(xy, Y=1):
    """Convert xyY into XYZ

    Args:
        xy ([float, float]): x, y input values

    Kwargs:
        Y (float): Y input value

    Returns:
        .[float, float, float]

    """
    x, y = xy
    X = (x*Y)/y
    Z = ((1-x-y)*Y)/y
    return [X, Y, Z]
