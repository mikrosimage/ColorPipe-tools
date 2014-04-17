""" Testing Abstract LUT model

"""
import unittest
import os
import shutil
import tempfile
from PyOpenColorIO.Constants import INTERP_LINEAR, INTERP_TETRAHEDRAL
from utils import lut_presets as presets
import utils.abstract_lut_helper as alh
from utils.colorspaces import REC709, SGAMUTSLOG, ALEXALOGCV3
from utils.csp_helper import CSP_HELPER
from utils.cube_helper import CUBE_HELPER
from utils.ocio_helper import create_ocio_processor

DISPLAY = False


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
        self.helpers_to_test = [
                                (CUBE_HELPER, '.cube'),
                                (CSP_HELPER, '.csp'),
                                ]

    def test_default_1d_lut(self):
        """ Test a default 1d LUT export

        """
        outlutfiles = []
        for helper, ext in self.helpers_to_test:
            outlutfile = os.path.join(self.tmp_dir, "default_1D" + ext)
            args_1d = helper.get_default_preset()
            helper.write_1d_lut(self.processor_1d.applyRGB, outlutfile,
                                args_1d)
            # create a processor and try it
            proc = create_ocio_processor(outlutfile,
                                         interpolation=INTERP_LINEAR)
            proc.applyRGB([0, 0, 0])
            outlutfiles.append(outlutfile)
        if DISPLAY:
            import plot_that_lut
            plot_that_lut.plot_that_lut(outlutfiles)

    def test_default_3d_lut(self):
        """ Test a default 3d LUT export

        """
        for helper, ext in self.helpers_to_test:
            outlutfile = os.path.join(self.tmp_dir, "default_3D" + ext)
            args_3d = helper.get_default_preset()
            helper.write_3d_lut(self.processor_3d.applyRGB, outlutfile,
                                args_3d)
            # create a processor and try it
            proc = create_ocio_processor(outlutfile,
                                         interpolation=INTERP_LINEAR)
            proc.applyRGB([0, 0, 0])
            if DISPLAY:
                import plot_that_lut
                plot_that_lut.plot_that_lut(outlutfile)

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

    def test_float_luts(self):
        """ Test float LUT transparency

        """
        colorspace_to_test = [REC709, SGAMUTSLOG, ALEXALOGCV3]
        delta = 0.00001
        for colorspace in colorspace_to_test:
            # define file name
            name = colorspace.__class__.__name__
            encode_filename = "linTo{0}_1D.csp".format(name)
            decode_filename = "{0}ToLin_1D.csp".format(name)
            encode_filepath = os.path.join(self.tmp_dir, encode_filename)
            decode_filepath = os.path.join(self.tmp_dir, decode_filename)
            # set preset
            args_1d = CSP_HELPER.get_default_preset()
            args_1d[presets.OUT_BITDEPTH] = 16
            decode_min = colorspace.decode_gradation(0)
            decode_max = colorspace.decode_gradation(1)
            encode_min = colorspace.encode_gradation(decode_min)
            encode_max = colorspace.encode_gradation(decode_max)
            args_1d[presets.IN_RANGE] = [decode_min, decode_max]

            # write encode LUT
            CSP_HELPER.write_2d_lut(colorspace.encode_gradation,
                                    encode_filepath,
                                    args_1d)
            # write decode LUT
            args_1d[presets.IN_RANGE] = [encode_min, encode_max]
            CSP_HELPER.write_2d_lut(colorspace.decode_gradation,
                                    decode_filepath,
                                    args_1d)
            # test transparency
            proc = create_ocio_processor(encode_filepath,
                                         postlutfile=decode_filepath,
                                         interpolation=INTERP_LINEAR)
            test_values = [[decode_min] * 3,
                           [decode_max] * 3,
                           [0] * 3,
                           [0.5] * 3,
                           [1] * 3]
            for rgb in test_values:
                res = proc.applyRGB(rgb)
                abs_value = abs(rgb[0] - res[0])
                self.assert_(abs_value < delta,
                             "{0} transparency test failed : {1:8f} >"
                             " acceptable delta ({2:8f})".format(name,
                                                              abs_value,
                                                              delta)
                             )

    def test_complete_attributes(self):
        """ Test preset complete function

        """
        cust_preset = {}
        cust_preset = presets.PRESET_HELPER.complete_preset(cust_preset)
        presets.PRESET_HELPER.check_preset(cust_preset)

    def tearDown(self):
        #Remove test directory
        shutil.rmtree(self.tmp_dir)


if __name__ == '__main__':
    unittest.main()
