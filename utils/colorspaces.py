""" Colorspace definitions

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
from utils import colors_helper
from abc import ABCMeta, abstractmethod
import math


class AbstractColorspace:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_red_primaries(self):
        """Return colorspace primaries

        Returns:
            .float, float

        """
        pass

    @abstractmethod
    def get_green_primaries(self):
        """Return colorspace primaries

        Returns:
            .float, float

        """
        pass

    @abstractmethod
    def get_blue_primaries(self):
        """Return colorspace primaries

        Returns:
            .float, float

        """
        pass

    @abstractmethod
    def get_white_point(self):
        """Return white coords

        Returns:
            .numpy.matrix (3x1)

        """
        pass

    @abstractmethod
    def lin_to_gamma(self, value):
        """Convert value from lin to gamma

        Args:
            value (float): value to transform

        Returns:
            .float

        """
        pass

    @abstractmethod
    def gamma_to_lin(self, value):
        """Convert value from lin to gamma

        Args:
            value (float): value to transform

        Returns:
            .float

        """
        pass


class Rec709(AbstractColorspace):
    """rec709 colorspace

    """
    def __init__(self):
        self._alpha = 1.099
        self._beta = 0.018
        self._round_depth = 3

    def get_red_primaries(self):
        return 0.64, 0.33

    def get_green_primaries(self):
        return 0.30, 0.60

    def get_blue_primaries(self):
        return 0.15, 0.06

    def get_white_point(self):
        return 0.3127, 0.3290

    def lin_to_gamma(self, value):
        if value < self._beta:
            return value * 4.5
        else:
            return pow(value, 0.45)*self._alpha - (self._alpha - 1)

    def gamma_to_lin(self, value):
        inv_beta = round(self.lin_to_gamma(self._beta), self._round_depth)
        if value < inv_beta:
            return value * 1/4.5
        else:
            return pow((value + (self._alpha - 1)) * (1/self._alpha), 1/0.45)


class AlexaLogCV3(AbstractColorspace):
    """AlexaLogCV3 colorspace

    """
    def get_red_primaries(self):
        return 0.6840, 0.3130

    def get_green_primaries(self):
        return 0.2210, 0.8480

    def get_blue_primaries(self):
        return 0.0861, -0.1020

    def get_white_point(self):
        return 0.3127, 0.3290

    def lin_to_gamma(self, value):
        if value > 0.010591:
            value = (0.247190 * math.log10(5.555556 * value + 0.052272)
                     + 0.385537)
        else:
            value = 5.367655 * value + 0.092809
        return value

    def gamma_to_lin(self, value):
        if value > 0.1496582:
            value = (math.pow(10.0, (value - 0.385537) / 0.2471896) * 0.18
                     - 0.00937677)
        else:
            value = (value / 0.9661776 - 0.04378604) * 0.18 - 0.00937677
        return value


class WideGamut(AbstractColorspace):
    """WideGamut colorspace

    """
    def __init__(self):
        self._gamma = 2.2

    def get_red_primaries(self):
        return 0.7347, 0.2653

    def get_green_primaries(self):
        return 0.1152, 0.8264

    def get_blue_primaries(self):
        return 0.1566, 0.0177

    def get_white_point(self):
        return 0.3457, 0.3585

    def lin_to_gamma(self, value):
        return colors_helper.lin_to_gamma(value, self._gamma)

    def gamma_to_lin(self, value):
        return colors_helper.gamma_to_lin(value, self._gamma)

REC709 = Rec709()
ALEXALOGCV3 = AlexaLogCV3()
WIDEGAMUT = WideGamut()
COLORSPACES = {
    'REC709': REC709,
    'ALEXALOGCV3': ALEXALOGCV3,
    'WIDEGAMUT': WIDEGAMUT
}
