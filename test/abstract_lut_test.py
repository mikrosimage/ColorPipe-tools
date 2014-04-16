""" Testing Abstract LUT model

"""
import unittest
import os
import shutil
import tempfile
from utils.ocio_helper import create_ocio_processor
from PyOpenColorIO.Constants import INTERP_LINEAR, INTERP_TETRAHEDRAL
from utils.cube_helper import CUBE_HELPER
from utils import lut_presets as presets
import utils.abstract_lut_helper as alh


class AbstractLUTTest(unittest.TestCase):
    """ Test export of different type of LUTs

    """
    def setUp(self):
        test_dir = os.path.join(os.path.dirname(__file__), 'test_files')
        self.tmp_dir = os.path.join(tempfile.gettempdir(), 'testCoPipe')
        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)
        # create OCIO processor
        lut1d = os.path.join(test_dir, 'CineonToLin_1D.csp')
        lut3d = os.path.join(test_dir, 'saturation.3dl')
        self.processor_1d = create_ocio_processor(lut1d,
                                                 interpolation=INTERP_LINEAR)
        self.processor_3d = create_ocio_processor(lut3d,
                                            interpolation=INTERP_TETRAHEDRAL)

    def test_default_1d_lut(self):
        """ Test a default cube 1d LUT export

        """
        outlutfile = os.path.join(self.tmp_dir, "default_1D.cube")
        args_1d = CUBE_HELPER.get_default_preset()
        CUBE_HELPER.write_1d_lut(self.processor_1d, outlutfile, args_1d)
        # create a processor and try it
        proc = create_ocio_processor(outlutfile, interpolation=INTERP_LINEAR)
        proc.applyRGB([0, 0, 0])

    def test_default_3d_lut(self):
        """ Test a default cube 3d LUT export

        """
        outlutfile = os.path.join(self.tmp_dir, "default_3D.cube")
        args_3d = CUBE_HELPER.get_default_preset()
        CUBE_HELPER.write_3d_lut(self.processor_3d, outlutfile, args_3d)
        # create a processor and try it
        proc = create_ocio_processor(outlutfile, interpolation=INTERP_LINEAR)
        proc.applyRGB([0, 0, 0])

    def test_check_attributes(self):
        """ Test preset check function

        """
        outlutfile = os.path.join(self.tmp_dir, "test.cube")
        default_preset = presets.PRESET_HELPER.get_default_preset()
        presets.PRESET_HELPER.check_preset(default_preset)
        # test missing attr
        cust_preset = {}
        self.failUnlessRaises(presets.PresetException,
                              presets.PRESET_HELPER.check_preset, cust_preset)
        for attr in presets.BASIC_ATTRS:
            cust_preset[attr] = default_preset[attr]
            self.failUnlessRaises(presets.PresetException,
                              presets.PRESET_HELPER.check_preset, cust_preset)
        ## test specific attr
        # change type to 1D
        cust_preset[presets.TYPE] = '1D'
        self.failUnlessRaises(presets.PresetException,
                              presets.PRESET_HELPER.check_preset, cust_preset)
        cust_preset[presets.OUT_BITDEPTH] = 12
        presets.PRESET_HELPER.check_preset(cust_preset)
        # try to write a 3D LUT with a 1D preset
        self.failUnlessRaises(alh.AbstractLUTException,
                              CUBE_HELPER.write_3d_lut,
                              self.processor_1d,
                              outlutfile,
                              cust_preset)
        # change type to 2D
        cust_preset[presets.TYPE] = '3D'
        self.failUnlessRaises(presets.PresetException,
                              presets.PRESET_HELPER.check_preset, cust_preset)
        cust_preset[presets.CUBE_SIZE] = 17
        presets.PRESET_HELPER.check_preset(cust_preset)
        # try to write a 1D LUT with a 3D preset
        self.failUnlessRaises(alh.AbstractLUTException,
                      CUBE_HELPER.write_1d_lut,
                      self.processor_1d,
                      outlutfile,
                      cust_preset)
        ## test value type
        # cube size
        cust_preset[presets.CUBE_SIZE] = 129
        self.failUnlessRaises(presets.PresetException,
                              presets.PRESET_HELPER.check_preset, cust_preset)
        cust_preset[presets.CUBE_SIZE] = default_preset[presets.CUBE_SIZE]
        # range
        tests = 'test', ['a', 'a'], [0.0, 0.5, 1.0], 0.1
        for test in tests:
            cust_preset[presets.IN_RANGE] = test
            self.failUnlessRaises(presets.PresetException,
                                  presets.PRESET_HELPER.check_preset,
                                  cust_preset)
        cust_preset[presets.IN_RANGE] = 0.1, 1
        presets.PRESET_HELPER.check_preset(cust_preset)
        cust_preset[presets.IN_RANGE] = (0.1, 1)
        presets.PRESET_HELPER.check_preset(cust_preset)

    def test_complete_attributes(self):
        """ Test preset complete function

        """
        cust_preset = {}
        presets.PRESET_HELPER.complete_preset(cust_preset)

    def tearDown(self):
        #Remove test directory
        shutil.rmtree(self.tmp_dir)


if __name__ == '__main__':
    unittest.main()
