""" Preset Testing

"""
import unittest
import tempfile
import shutil
import os
from utils import lut_presets as presets
from lutLab.lut_to_lut import lut_to_lut
from lutLab.curve_to_lut import curve_to_lut
from utils.csp_helper import CSP_HELPER
from utils.ocio_helper import create_ocio_processor
from PyOpenColorIO.Constants import INTERP_LINEAR

DISPLAY = False


class GeneralTest(unittest.TestCase):
    """General Test : plot lut 1d/3d, convert lut, extract 1d lut

    """
    def setUp(self):
        test_dir = os.path.join(os.path.dirname(__file__), 'test_files')
        self.sample_preset = os.path.join(test_dir, 'preset_sample.json')
        self.lut3d = os.path.join(test_dir, 'saturation.3dl')
        self.tmp_dir = os.path.join(tempfile.gettempdir(), 'testCoPipe')
        self.preset_path = os.path.join(self.tmp_dir, "test_preset.json")
        os.mkdir(self.tmp_dir)

    def test_write_and_readback(self):
        """Write and read back a preset

        """
        preset = {presets.TYPE: '1D'}
        preset = CSP_HELPER.complete_preset(preset)
        presets.write_preset(self.preset_path, preset)
        back_preset = presets.read_preset(self.preset_path)
        expression = set(back_preset).issubset(set(preset))
        self.assert_(expression,
                     ("Something went wrong in preset write and read :\n"
                      "Write preset:\n{0}\nRead one:\n{1}"
                      ).format(preset, back_preset))

    def test_convert_from_preset(self):
        """Read a preset file and write a LUT

        """
        preset = presets.read_preset(self.sample_preset)
        outlutfile = os.path.join(self.tmp_dir, 'test_preset.cube')
        lut_to_lut(self.lut3d, preset=preset, outlutfile=outlutfile)
        proc = create_ocio_processor(outlutfile,
                                     interpolation=INTERP_LINEAR)
        proc.applyRGB([0, 0, 0])
        proc.applyRGB([1, 1, 1])
        if DISPLAY:
            import plot_that_lut
            plot_that_lut.plot_that_lut(outlutfile)

    def test_env_presets(self):
        """ Load presets from env

        """
        loaded_presets = presets.get_presets_from_env()
        self.assert_(len(loaded_presets) > 0, ("No preset loaded. "
                                               "Default presets should at "
                                               "least have been detected"))
        # try to use the first preset
        preset = loaded_presets.values()[0]
        curve_to_lut('sRGB', None, outlutfile=self.tmp_dir, preset=preset)

    def tearDown(self):
        # Remove test directory
        shutil.rmtree(self.tmp_dir)

if __name__ == '__main__':
    unittest.main()
