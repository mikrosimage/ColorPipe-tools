""" Abstract LUT Helper

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.2"
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from numpy import linspace
from utils.lut_utils import get_file_shortname
from utils import lut_presets as presets
from utils.lut_presets import (TYPE, IN_RANGE, OUT_RANGE, OUT_BITDEPTH,
                               CUBE_SIZE, BASIC_ATTRS, RAISE_MODE, FILL_MODE,
                               TYPE_CHOICE, BITDEPTH_MAX_VALUE,
                               BITDEPTH_MIN_VALUE, CUBE_SIZE_MAX_VALUE,
                               CUBE_SIZE_MIN_VALUE, PresetException,
                               MISSING_ATTR_MESSAGE)

# RGB triplet object
Rgb = namedtuple('Rgb', 'r g b')


class AbstractLUTException(Exception):
    """Module custom exception

    """
    pass


class AbstractLUTHelper(object):
    """Abstract LUT helper

    """
    __metaclass__ = ABCMeta

    @staticmethod
    def _get_pattern_1d(preset):
        """ Get string pattern considering sampling types (float / int)

        Args:
            preset (dict): lut generic and sampling informations

        Returns:
            .str

        """
        is_int = AbstractLUTHelper.is_output_int(preset)
        if is_int:
            pattern = "{0}\n"
        else:
            pattern = "{0:.6f}\n"
        return pattern

    @staticmethod
    def _get_pattern(preset):
        """ Get string pattern considering sampling types (float / int)

        Args:
            preset (dict): lut generic and sampling informations

        Returns:
            .str

        """
        is_int = AbstractLUTHelper.is_output_int(preset)
        if is_int:
            pattern = "{0} {1} {2}\n"
        else:
            pattern = "{0:.6f} {1:.6f} {2:.6f}\n"
        return pattern

    def _get_r_value_line(self, preset, rgb):
        """ Get string pattern for a 1D LUT

        Args:
            preset (dict): lut generic and sampling informations

            rgb (Rgb): values

        Returns:
            .str

        """
        return self._get_pattern_1d(preset).format(rgb.r)

    def _get_rgb_value_line(self, preset, rgb):
        """ Get string pattern for a 2D / 3D LUT
        Args:
            preset (dict): lut generic and sampling informations

            rgb Rgb): values

        Returns:
            .str

        """
        return self._get_pattern(preset).format(rgb.r, rgb.g, rgb.b)

    def _get_1d_data(self, process_function, preset):
        """ Process 1D/2D data considering LUT params

        Args:
            process_function (func): could be a processor.applyRGB
            (PyOpenColorIO.config.Processor) or a function that took a range
            of values and return the modified values. Ex: colorspace gradation
            functions

            preset (dict): lut generic and sampling informations

        Returns:
            .[Rgb]

        """
        self.check_preset(preset)
        if not presets.is_1d_or_2d_preset(preset):
            raise AbstractLUTException(("Preset isn't valid for 1D / 2D LUT:"
                                        " {0}").format(preset))
        input_range = preset[presets.IN_RANGE]
        output_range = preset[presets.OUT_RANGE]
        samples_count = pow(2,  preset[presets.OUT_BITDEPTH])
        is_int = AbstractLUTHelper.is_output_int(preset)
        compute_range = linspace(input_range[0],
                                      input_range[1],
                                      samples_count)
        data = []
        for code_value in compute_range:
            norm_value = code_value
            if is_int:
                norm_value = (code_value - input_range[0]) / input_range[1]
            res = process_function([norm_value, norm_value, norm_value])
            res = [(x * output_range[1]) + output_range[0] for x in res]
            if is_int:
                res = [int(x) for x in res]
            data.append(Rgb(res[0], res[1], res[2]))
        return data

    def _get_3d_data(self, process_function, preset):
        """ Process 3D data considering LUT params

        Args:
            process_function (func): could be a processor.applyRGB
            (PyOpenColorIO.config.Processor) or a function that took a range
            of values and return the modified values. Ex: colorspace gradation
            functions

            preset (dict): lut generic and sampling informations

        Returns:
            .[Rgb]

        """
        self.check_preset(preset)
        if not presets.is_3d_preset(preset):
            raise AbstractLUTException(("Preset isn't valid for 3D LUT:"
                                        " {0}").format(preset))
        cube_size = preset[presets.CUBE_SIZE]
        input_range = preset[presets.IN_RANGE]
        output_range = preset[presets.OUT_RANGE]
        is_int = False
        if (isinstance(output_range[0], int)
            and isinstance(output_range[1], int)):
            is_int = True
        compute_range = linspace(input_range[0],
                                 input_range[1],
                                 cube_size)
        data = []
        for blue in compute_range:
            for green in compute_range:
                for red in compute_range:
                    norm_red = red
                    norm_green = green
                    norm_blue = blue
                    if is_int:
                        norm_red = (red - input_range[0]) / input_range[1]
                        norm_green = (green - input_range[0]) / input_range[1]
                        norm_blue = (blue - input_range[0]) / input_range[1]
                    res = process_function([norm_red, norm_green, norm_blue])
                    res = [(x * output_range[1]) + output_range[0]
                           for x in res]
                    if is_int:
                        res = [int(x) for x in res]
                    data.append(Rgb(res[0], res[1], res[2]))
        return data

    @abstractmethod
    def _write_1d_2d_lut(self, process_function, file_path, preset,
                         line_function):
        """ Write 1d / 2d LUT in output file

        Args:
            process_function (func): could be a processor.applyRGB
            (PyOpenColorIO.config.Processor) or a function that took a range
            of values and return the modified values. Ex: colorspace gradation
            functions

            preset (dict): lut generic and sampling informations

            line_function (function): describe how color values are written.
            Ex: "r g b" or "r, g, b" or "r".
            Use _get_rgb_value_line or _get_r_value_line

        """
        pass

    def write_2d_lut(self, process_function, file_path, preset):
        """ Write 2d LUT in output file

        Args:
            process_function (func): could be a processor.applyRGB
            (PyOpenColorIO.config.Processor) or a function that took a range
            of values and return the modified values. Ex: colorspace gradation
            functions

            preset (dict): lut generic and sampling informations
        """
        self._write_1d_2d_lut(process_function, file_path, preset,
                              self._get_rgb_value_line)

    def write_1d_lut(self, process_function, file_path, preset):
        """ Write 2d LUT in output file

        Args:
            process_function (func): could be a processor.applyRGB
            (PyOpenColorIO.config.Processor) or a function that took a range
            of values and return the modified values. Ex: colorspace gradation
            functions

            preset (dict): lut generic and sampling informations
        """
        self._write_1d_2d_lut(process_function, file_path, preset,
                              self._get_r_value_line)

    @abstractmethod
    def write_3d_lut(self, process_function, file_path, preset):
        """ Write 3d LUT in output file

        Args:
            process_function (func): could be a processor.applyRGB
            (PyOpenColorIO.config.Processor) or a function that took a range
            of values and return the modified values. Ex: colorspace gradation
            functions

            preset (dict): lut generic and sampling informations
        """
        pass

    @staticmethod
    @abstractmethod
    def get_default_preset():
        """ Return default preset
            See utils.lut_presets module
        """
        pass

    @staticmethod
    def get_export_message(file_path):
        """ Get export message

        Returns:
            .str

        """
        return "a new LUT was written in {1}".format(
                                                get_file_shortname(file_path),
                                                file_path)

    @staticmethod
    def _validate_preset(preset, mode=RAISE_MODE, default_preset=None):
        """ Check preset. When an irregularity is found, if mode is 'raise'
        an exception is thrown, else preset is completed with default values

        Args:
            preset (dict): preset to validate

        Kwargs:
            mode (str): raise or fill. Default is raise.

        """
        # check if basic attribute are present
        if default_preset is None:
            default_preset = presets.get_default_preset()
        for attr in BASIC_ATTRS:
            if attr not in preset:
                if mode == RAISE_MODE:
                    raise PresetException(MISSING_ATTR_MESSAGE.format(attr))
                preset[attr] = default_preset[attr]
        # check if type is correct
        if not preset[TYPE] in TYPE_CHOICE:
            if mode == RAISE_MODE:
                raise PresetException(("{0} is not a valid type: "
                                      "{1}").format(preset[TYPE], TYPE_CHOICE))
            preset[TYPE] = default_preset[TYPE]
        ## check if type specific attr are set
        # default type
        if preset[TYPE] == 'default' and (OUT_BITDEPTH not in preset
                                          or CUBE_SIZE not in preset):
            if mode == RAISE_MODE:
                raise PresetException(("A default preset must define '{0} and "
                                       "'{1}' attributes").format(OUT_BITDEPTH,
                                                                  CUBE_SIZE))
            if OUT_BITDEPTH not in preset:
                preset[OUT_BITDEPTH] = default_preset[OUT_BITDEPTH]
            if CUBE_SIZE not in preset:
                preset[CUBE_SIZE] = default_preset[CUBE_SIZE]
            preset[TYPE] = default_preset[TYPE]
        # 1D / 2D type
        if preset[TYPE] == '1D' or preset[TYPE] == '2D':
            if OUT_BITDEPTH not in preset:
                if mode == RAISE_MODE:
                    raise PresetException(("A 1D/2D preset must define '{0}"
                                           "attribute").format(OUT_BITDEPTH))
                preset[OUT_BITDEPTH] = default_preset[OUT_BITDEPTH]
            elif (not isinstance(preset[OUT_BITDEPTH], int)
                  or preset[OUT_BITDEPTH] < BITDEPTH_MIN_VALUE
                  or preset[OUT_BITDEPTH] > BITDEPTH_MAX_VALUE):
                if mode == RAISE_MODE:
                    raise PresetException(("Invalid bit depth: {0}"
                                           ).format(preset[OUT_BITDEPTH]))
                preset[OUT_BITDEPTH] = default_preset[OUT_BITDEPTH]
        # 3D type
        if preset[TYPE] == '3D':
            if CUBE_SIZE not in preset:
                if mode == RAISE_MODE:
                    raise PresetException(("A 3D preset must define '{0}"
                                           "attribute").format(CUBE_SIZE))
                preset[CUBE_SIZE] = default_preset[CUBE_SIZE]
            elif (not isinstance(preset[CUBE_SIZE], int)
                  or preset[CUBE_SIZE] < CUBE_SIZE_MIN_VALUE
                  or preset[CUBE_SIZE] > CUBE_SIZE_MAX_VALUE):
                if mode == RAISE_MODE:
                    raise PresetException(("Invalid cube size: {0}"
                                           ).format(preset[CUBE_SIZE]))
                preset[CUBE_SIZE] = default_preset[CUBE_SIZE]
        # Check ranges
        ranges = IN_RANGE, OUT_RANGE
        for arange in ranges:
            if not presets.is_range(preset[arange]):
                if mode == RAISE_MODE:
                    raise PresetException(("Invalid range: {0}"
                                           ).format(preset[arange]))
                preset[arange] = default_preset[arange]
        # return updated preset
        return preset

    def check_preset(self, preset, default_preset=None):
        """ Check preset. When an irregularity is found, an exception is thrown

        Args:
            preset (dict): preset to validate

        """
        self._validate_preset(preset, RAISE_MODE, default_preset)

    def complete_preset(self, preset, default_preset=None):
        """ Check preset. When an irregularity is found, preset is completed
        with default values

        Args:
            preset (dict): preset to validate

        """
        return self._validate_preset(preset, FILL_MODE,
                                                  default_preset)

    @staticmethod
    def is_int(test_range):
        """ Check if a range is int

        Args:
            test_range ([int/float, int/float]): range to test

        Returns:
            .boolean

        """
        is_int = False
        if (isinstance(test_range[0], int)
            and isinstance(test_range[1], int)):
            is_int = True
        return is_int

    @staticmethod
    def is_intput_int(preset):
        """ Check if a in range is int
        Returns:
            .boolean

        """
        return AbstractLUTHelper.is_int(preset[presets.IN_RANGE])

    @staticmethod
    def is_output_int(preset):
        """ Check if a out range is int
        Returns:
            .boolean

        """
        return AbstractLUTHelper.is_int(preset[presets.OUT_RANGE])

    @staticmethod
    def get_generated_title(file_path, preset):
        """ Title with file short name and ranges

        """
        return "{0} {1} {2}".format(get_file_shortname(file_path),
                                    preset[presets.IN_RANGE],
                                    preset[presets.OUT_RANGE])
