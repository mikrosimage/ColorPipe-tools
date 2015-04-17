""" Colorspace definitions

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.3"
from utils import colors_helper
from abc import ABCMeta, abstractmethod
import math
import collections


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
    def _encode_gradation(self, value):
        """Gradation encoding function

        Args:
            value (float): value to transform

        Returns:
            .float

        """
        pass

    @abstractmethod
    def _decode_gradation(self, value):
        """Gradation decoding function

        Args:
            values (float): values to transform

        Returns:
            .float

        """
        pass

    def encode_gradation(self, values):
        """Gradation encoding function

        Args:
            values (float): values to transform

        Returns:
            .float

        """
        if not isinstance(values, (list, tuple)):
            return self._encode_gradation(values)
        return [self._encode_gradation(value) for value in values]

    def decode_gradation(self, values):
        """Gradation decoding function

        Args:
            value (float): value to transform

        Returns:
            .float

        """
        if not isinstance(values, (list, tuple)):
            return self._decode_gradation(values)
        return [self._decode_gradation(value) for value in values]


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

    def _encode_gradation(self, value):
        if value > 0.0031308:
            return 1.055 * pow(value, 1.0 / 2.4) - 0.055
        else:
            return 12.92 * value

    def _decode_gradation(self, value):
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

    def _encode_gradation(self, value):
        if value < self._beta:
            return value * 4.5
        else:
            return pow(value, 0.45) * self._alpha - (self._alpha - 1)

    def _decode_gradation(self, value):
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

    def _encode_gradation(self, value):
        if value > 0.0106232378792:
            value = (0.2471896 * math.log10((value + 0.00937677) / 0.18)
                     + 0.385537)
        else:
            value = 0.9661776 * ((value + 0.00937677) / 0.18 + 0.04378604)
        return value

    def _decode_gradation(self, value):
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

    def _encode_gradation(self, value):
        return colors_helper.lin_to_gamma(value, self._gamma)

    def _decode_gradation(self, value):
        return colors_helper.gamma_to_lin(value, self._gamma)


class ACES(AbstractColorspace):
    """ACES Colorspace (P0 primaries and linear encoding)

    """
    def get_red_primaries(self):
        return 0.73470, 0.26530

    def get_green_primaries(self):
        return 0.00000, 1.00000

    def get_blue_primaries(self):
        return 0.00010, -0.07700

    def get_white_point(self):
        return 0.32168, 0.33767

    def _encode_gradation(self, value):
        return value

    def _decode_gradation(self, value):
        return value


class ACEScg(ACES):
    """ACES cg Colorspace (P1 primaries and linear encoding)

    """
    def get_red_primaries(self):
        return 0.713, 0.293

    def get_green_primaries(self):
        return 0.165, 0.830

    def get_blue_primaries(self):
        return 0.128, 0.044

    def get_white_point(self):
        return 0.32168, 0.33767


class ACEScc(ACEScg):
    """ACEScc Colorspace (P1 primaries and log encoding)

    """
    def __init__(self):
        self.enc_threshold = math.pow(2.0, -15)
        self.denorm_fake0 = math.pow(2.0, -16)
        self.offset = 9.72
        self.factor = 17.52

        # encode constants
        self.enc_threshold = math.pow(2.0, -15)
        self.enc_threshold_cst = (math.log(self.enc_threshold * 0.5, 2.0) + self.offset) / self.factor

        # decode constants
        self.dec_low_threshold = (self.offset - 15) / self.factor
        self.dec_white_threshold = 65504.0
        self.dec_up_threshold = (math.log(self.dec_white_threshold, 2.0) + self.offset) / self.factor

    def _encode_gradation(self, value):
        if value <= 0:
            return self.enc_threshold_cst
        elif value < self.enc_threshold:
            return (math.log(self.denorm_fake0 + value * 0.5, 2) + self.offset) / self.factor
        else:
            return (math.log(value, 2.0) + self.offset) / self.factor

    def _decode_gradation(self, value):
        if value < self.dec_low_threshold:
            return (math.pow(2.0, value * self.factor - self.offset) - self.denorm_fake0) * 2
        elif value >= self.dec_up_threshold:
            return self.dec_white_threshold
        else:
            return math.pow(2.0, value * self.factor - self.offset)


class ACESlog(ACES):
    """ACES LOG colorspace (deprecated by ACEScc)

    """
    def __init__(self, is_integer=False):
        self.is_integer = is_integer
        self.unity = 32768
        self.xperstop = 2048
        self.denorm_trans = math.pow(2.0, -15)
        self.denorm_fake0 = math.pow(2.0, -16)

    def _encode_gradation(self, value):
        if value < 0:
            res = 0
        elif value < self.denorm_trans:
            # log2(2.0^-16 + ACES * 0.5) * 2048 + 32768
            res = (math.log(self.denorm_fake0 + value * 0.5, 2) * self.xperstop
                   + self.unity)
        else:
            # log2(ACES) * 2048 + 32768
            res = math.log(value, 2) * self.xperstop + self.unity
        if self.is_integer:
            return min(math.floor(res) + 0.5, 65535)
        else:
            return res

    def _decode_gradation(self, value):
        if value < self.xperstop:
            # (2^((ACESlog - 32768) / 2048) - 2^-16) * 2
            return ((math.pow(2, (value - self.unity) / self.xperstop)
                     - self.denorm_fake0) * 2.0)
        else:
            # 2^((ACESlog - 32768) / 2048)
            return math.pow(2, (value - self.unity) / self.xperstop)


class ACESproxy(ACEScg):
    """ACESproxy colorspace
    """
    def __init__(self, cv_min, cv_max, steps_per_stop, mid_cv_offset,
                 mid_log_offset):
        """ACESproxy general implementation

            Args:
                cv_min (int): minimum code value available for representation
                of ACES image data

                cv_max (int): maximum code value available for representation
                of ACES image data

                steps_per_stop (int): number of code values representing a
                change of 1 stop in exposure

                mid_cv_offset (int): integer code value representing the
                assigned midpoint of the exposure scale for a particular
                bit-depth encoding. (e.g. the point to which a mid-grey
                exposure value would be mapped)

                mid_log_offset (float): base2 logarithmic value representing
                the assigned midpoint of the exposure scale in log space,
                [e.g. MidLogOffset = log2( 2^(-2.5) ) = -2.5 ]

        """
        self.cv_min = cv_min
        self.cv_max = cv_max
        self.steps_per_stop = steps_per_stop
        self.mid_cv_offset = mid_cv_offset
        self.mid_log_offset = mid_log_offset
        self.threshold = math.pow(2.0, -9.72)

    def float_to_cv(self, value):
        """Math function returning MAX(cv_min, MIN(cv_max, ROUND(value)))
        """
        return max(self.cv_min, min(self.cv_max, round(value)))

    def _encode_gradation(self, value):
        if value <= self.threshold:
            return self.cv_min
        else:
            return self.float_to_cv((math.log(value, 2.0) - self.mid_log_offset)
                                    *
                                    self.steps_per_stop + self.mid_cv_offset
                                    )

    def _decode_gradation(self, value):
        return math.pow(2.0, (value - self.mid_cv_offset) / self.steps_per_stop
                        + self.mid_log_offset)


class ACESproxy10(ACESproxy):
    """10 bit int implementation of ACESproxy

    """
    def __init__(self):
        ACESproxy.__init__(self, cv_min=64.0, cv_max=940.0, steps_per_stop=50.0,
                           mid_cv_offset=425.0, mid_log_offset=-2.5)


class ACESproxy12(ACESproxy):
    """12 bit int implementation of ACESproxy

    """
    def __init__(self):
        ACESproxy.__init__(self, cv_min=256.0, cv_max=3760.0, steps_per_stop=200.0,
                           mid_cv_offset=1700.0, mid_log_offset=-2.5)


class SGamutSLog(AbstractColorspace):
    """Sony SGammut and SLog

    """
    def get_red_primaries(self):
        return 0.73, 0.28

    def get_green_primaries(self):
        return 0.14, 0.855

    def get_blue_primaries(self):
        return 0.10, -0.05

    def get_white_point(self):
        return 0.3127, 0.3290

    def _encode_gradation(self, value):
        return (0.432699 * math.log10(value + 0.037584) + 0.616596) + 0.03

    def _decode_gradation(self, value):
        return (math.pow(10.0, ((value - 0.616596 - 0.03) / 0.432699))
                - 0.037584)


class SGamutSLog2(SGamutSLog):
    """Sony SGamut and SLog2
    Inspired from OpenColorIO ACES profil SLog2

    """
    def __init__(self):
        self.min = 64.0 / 1023.0
        self.max = 940.0 / 1023.0
        self.decode_threshold = 0.030001222851889303

    def _encode_gradation(self, value):
        value = value / 0.9
        if value < self.decode_gradation(self.decode_threshold):
            value = value / 0.28258064516129 + self.decode_threshold
        else:
            value = (0.432699 * math.log10(155.0 * value / 219.0 + 0.037584)
                     + 0.616596 + 0.03)
        value = value * (self.max - self.min) + self.min
        return value

    def _decode_gradation(self, value):
        value = (value - self.min) / (self.max - self.min)
        if value < self.decode_threshold:
            value = ((value - self.decode_threshold) * 0.28258064516129)
        else:
            value = (219.0 *
                     (math.pow(10.0, (value - 0.616596 - 0.03) / 0.432699)
                      - 0.037584) / 155.0)
        return value * 0.9


class SGamutSLog3(SGamutSLog):
    """Sony SGamut/SGamut3 and SLog3
    SGamut3 has the same primaries than SGamut

    """
    def _encode_gradation(self, value):
        if value >= 0.01125000:
            return ((420.0 + math. log10((value + 0.01) / (0.18 + 0.01))
                     * 261.5) / 1023.0)
        else:
            return ((value * (171.2102946929 - 95.0) / 0.01125000 + 95.0)
                    / 1023.0)

    def _decode_gradation(self, value):
        if value >= 171.2102946929 / 1023.0:
            return ((math.pow(10.0, (value * 1023 - 420) / 261.5))
                    * (0.18 + 0.01) - 0.01)
        else:
            return ((value * 1023.0 - 95.0) * 0.01125000
                    / (171.2102946929 - 95.0))


class SGamut3CineSLog3(SGamutSLog3):
    """Sony SGamut3Cine and SLog3

    """
    def get_red_primaries(self):
        return 0.766, 0.275

    def get_green_primaries(self):
        return 0.225, 0.8

    def get_blue_primaries(self):
        return 0.089, -0.087

    def get_white_point(self):
        return 0.31270, 0.329


REC709 = Rec709()
ALEXALOGCV3 = AlexaLogCV3()
WIDEGAMUT = WideGamut()
REC2020_10B = Rec2020(is_ten_bits=True)
REC2020_12B = Rec2020(is_ten_bits=False)
ACES = ACES()
ACESLOG_32f = ACESlog(is_integer=False)
ACESLOG_16i = ACESlog(is_integer=True)
ACESPROXY_10i = ACESproxy10()
ACESPROXY_12i = ACESproxy12()
ACESCG = ACEScg()
ACESCC = ACEScc()
sRGB = sRGB()
SGAMUTSLOG = SGamutSLog()
SGAMUTSLOG2 = SGamutSLog2()
SGAMUTSLOG3 = SGamutSLog3()
SGAMUT3CINESLOG3 = SGamut3CineSLog3()

COLORSPACES = {
    'Rec709': REC709,
    'AlexaLogCV3': ALEXALOGCV3,
    'WideGamut': WIDEGAMUT,
    'Rec2020_10bits': REC2020_10B,
    'Rec2020_12bits': REC2020_12B,
    'ACES': ACES,
    'sRGB': sRGB,
    'ACESlog_32f': ACESLOG_32f,
    'ACESlog_16i': ACESLOG_16i,
    'ACESproxy_10': ACESPROXY_10i,
    'ACESproxy_12': ACESPROXY_12i,
    'ACEScg': ACESCG,
    'ACEScc': ACESCC,
    'SGamutSLog': SGAMUTSLOG,
    'SGamutSLog2': SGAMUTSLOG2,
    'SGamutSLog3': SGAMUTSLOG3,
    'SGamut3CineSLog3': SGAMUT3CINESLOG3,
}
