""" Colorspace definitions

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
from utils import colors_helper
from abc import ABCMeta, abstractmethod
import math


class AbstractColorspace(object):
    """Abstract Color Space

    """
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
    def encode_gradation(self, value):
        """Gradation encoding function

        Args:
            value (float): value to transform

        Returns:
            .float

        """
        pass

    @abstractmethod
    def decode_gradation(self, value):
        """Gradation decoding function

        Args:
            value (float): value to transform

        Returns:
            .float

        """
        pass


class sRGB(AbstractColorspace):
    """sRGB colorspace

    """
    def get_red_primaries(self):
        return 0.64, 0.33

    def get_green_primaries(self):
        return 0.30, 0.60

    def get_blue_primaries(self):
        return 0.15, 0.06

    def get_white_point(self):
        return 0.3127, 0.3290

    def encode_gradation(self, value):
        if value > 0.0031308:
            return 1.055 * pow(value, 1.0 / 2.4) - 0.055
        else:
            return 12.92 * value

    def decode_gradation(self, value):
        if value > 0.04045:
            return pow((value + 0.055) / 1.055, 2.4)
        else:
            return value / 12.92


class Rec709(sRGB):
    """rec709 colorspace

    """
    def __init__(self):
        self._alpha = 1.099
        self._beta = 0.018
        self._round_depth = 3

    def encode_gradation(self, value):
        if value < self._beta:
            return value * 4.5
        else:
            return pow(value, 0.45) * self._alpha - (self._alpha - 1)

    def decode_gradation(self, value):
        inv_beta = round(self.encode_gradation(self._beta), self._round_depth)
        if value < inv_beta:
            return value * 1 / 4.5
        else:
            return pow((value + (self._alpha - 1)) * (1 / self._alpha),
                       1 / 0.45)


class Rec2020(Rec709):
    """Rec2020 colorspace (10 and 12 bits)
    """
    def __init__(self, is_ten_bits=True):
        """ Ctor

        Kwargs:
            is_ten_bits (bool): if true, 10 bits Rec709 constants will be used,
            else 12 bits ones are defined

        """
        Rec709.__init__(self)
        if not is_ten_bits:
            # define value for 12 bits per sample display
            self._alpha = 1.0993
            self._beta = 0.0181
            self._round_depth = 4

    def get_red_primaries(self):
        return 0.708, 0.292

    def get_green_primaries(self):
        return 0.170, 0.797

    def get_blue_primaries(self):
        return 0.131, 0.046

    def get_white_point(self):
        return 0.3127, 0.3290


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

    def encode_gradation(self, value):
        if value > 0.010591:
            value = (0.247190 * math.log10(5.555556 * value + 0.052272)
                     + 0.385537)
        else:
            value = 5.367655 * value + 0.092809
        return value

    def decode_gradation(self, value):
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

    def encode_gradation(self, value):
        return colors_helper.lin_to_gamma(value, self._gamma)

    def decode_gradation(self, value):
        return colors_helper.gamma_to_lin(value, self._gamma)


class ACES(AbstractColorspace):
    """ACES Colorspace

    """
    def get_red_primaries(self):
        return 0.73470, 0.26530

    def get_green_primaries(self):
        return 0.00000, 1.00000

    def get_blue_primaries(self):
        return 0.00010, -0.07700

    def get_white_point(self):
        return 0.32168, 0.33767

    def encode_gradation(self, value):
        return value

    def decode_gradation(self, value):
        return value


REC709 = Rec709()
ALEXALOGCV3 = AlexaLogCV3()
WIDEGAMUT = WideGamut()
REC2020_10B = Rec2020(is_ten_bits=True)
REC2020_12B = Rec2020(is_ten_bits=False)
ACES = ACES()
sRGB = sRGB()
COLORSPACES = {
    'REC709': REC709,
    'ALEXALOGCV3': ALEXALOGCV3,
    'WIDEGAMUT': WIDEGAMUT,
    'REC2020_10bits': REC2020_10B,
    'REC2020_12bits': REC2020_12B,
    'ACES': ACES,
    'sRGB': sRGB,
}
