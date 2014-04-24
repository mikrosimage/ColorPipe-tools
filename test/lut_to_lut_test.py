""" Testing lut_to_lut model

"""
import unittest
import shutil
import os
import tempfile
from lutLab.lut_to_lut import lut_to_lut
from utils.lut_utils import LUTException
from utils.lut_presets import PresetException
from utils.threedl_helper import ThreeDLHelperException
from utils.clcc_helper import CLCCHelperException
from utils.json_helper import JsonHelperException
from utils.ascii_helper import AsciiHelperException


class LUTToLUTTest(unittest.TestCase):
    """ Test lut_to_lut tool

    """
    def setUp(self):
        test_dir = os.path.join(os.path.dirname(__file__), 'test_files')
        self.tmp_dir = os.path.join(tempfile.gettempdir(), 'testCoPipe')
        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)
        # test LUT
        self.lut1d = os.path.join(test_dir, 'CineonToLin_1D.csp')
        self.lut3d = os.path.join(test_dir, 'saturation.3dl')

    def test_export_csp_cube(self):
        """ Test CSP / Cube export

        """
        for form in ['csp', 'cube']:
            # test 1D/2D export
            outlutfile = os.path.join(self.tmp_dir,
                                      "CineonToLin_export." + form)
            lut_to_lut(self.lut1d, "1D", form, outlutfile)
            # test 3D export
            outlutfile = os.path.join(self.tmp_dir,
                                      "saturation_export." + form)
            lut_to_lut(self.lut3d, "3D", form, outlutfile)
            # test wrong int range
            self.failUnlessRaises(PresetException, lut_to_lut, self.lut3d,
                                  "3D", form, outlutfile,
                                  output_range=[0, 1024])

    def test_export_3dl(self):
        """ Test 3dl export

        """
        outlutfile = os.path.join(self.tmp_dir, "CineonToLin_export.3dl")
        lut_to_lut(self.lut1d, "3D", "3dl", outlutfile)
        # test wrong float range
        self.failUnlessRaises(PresetException, lut_to_lut, self.lut3d,
                              "3D", "3dl", outlutfile, input_range=[0.0, 1.0])
        # test wrong type
        self.failUnlessRaises(ThreeDLHelperException, lut_to_lut, self.lut3d,
                              "2D", "3dl", outlutfile, input_range=[0.0, 1.0])

        # test wrong extension
        self.failUnlessRaises(LUTException, lut_to_lut, self.lut3d,
                              "3D", "csp", outlutfile, input_range=[0.0, 1.0])

    def test_export_cc_json(self):
        """ Test cc / json export

        """
        for form, ext, excep in [('json', '.json', JsonHelperException),
                          ('clcc', '.cc', CLCCHelperException)]:
            outlutfile = os.path.join(self.tmp_dir, "CineonToLin_export" + ext)
            lut_to_lut(self.lut1d, "3D", form, outlutfile)
            # test wrong type
            self.failUnlessRaises(excep, lut_to_lut, self.lut3d,
                                  "2D", form, outlutfile)

    def test_export_spi(self):
        """ Test spi export

        """
        outlutfile = os.path.join(self.tmp_dir, "CineonToLin_export.spi1d")
        # test 1D/2D export
        lut_to_lut(self.lut1d, "1D", "spi", outlutfile, inverse=True)
        lut_to_lut(self.lut1d, "2D", "spi", outlutfile)
        # test wrong int range
        self.failUnlessRaises(PresetException, lut_to_lut, self.lut1d,
                              "1D", "spi", outlutfile, output_range=[0, 1024])
        # test 3D export with wrong ext
        self.failUnlessRaises(LUTException, lut_to_lut, self.lut3d, "3D",
                              "spi", outlutfile)
        # test 3D export
        outlutfile = os.path.join(self.tmp_dir, "saturation_export.spi3d")
        lut_to_lut(self.lut3d, "3D", "spi", outlutfile)

    def test_export_ascii(self):
        """ Test ascii export

        """
        outlutfile = os.path.join(self.tmp_dir, "CineonToLin_export.lut")
        # test 1D/2D export
        lut_to_lut(self.lut1d, "1D", "lut", outlutfile)
        lut_to_lut(self.lut1d, "2D", "lut", outlutfile)
        # test wrong type
        self.failUnlessRaises(AsciiHelperException, lut_to_lut, self.lut3d,
                              "3D", "lut", outlutfile)
        # test wrong out bit depth
        # (default output range is [0, 1023], out bit depth must be 10
        self.failUnlessRaises(AsciiHelperException, lut_to_lut, self.lut1d,
                              "1D", "lut", outlutfile, out_bit_depth=12)

    def tearDown(self):
        #Remove test directory
        shutil.rmtree(self.tmp_dir)

if __name__ == '__main__':
    unittest.main()
