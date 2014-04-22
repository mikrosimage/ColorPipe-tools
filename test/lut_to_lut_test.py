""" Testing lut_to_lut model

"""
import unittest
import shutil
import os
import tempfile
from lutLab.lut_to_lut import lut_to_lut
from utils.csp_helper import CSPHelperException
from utils.threedl_helper import ThreeDLHelperException
from utils.lut_utils import LUTException


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

    def test_export_csp(self):
        """ Test 3D LUT to CSP 3D LUT

        """
        outlutfile = os.path.join(self.tmp_dir, "saturation_export.csp")
        lut_to_lut(self.lut3d, "3D", "csp", outlutfile)
        # test wrong int range
        self.failUnlessRaises(CSPHelperException, lut_to_lut, self.lut3d,
                              "3D", "csp", outlutfile, output_range=[0, 1024])

    def test_export_3dl(self):
        """ Test 1D LUT to 3dl LUT

        """
        outlutfile = os.path.join(self.tmp_dir, "CineonToLin_export.3dl")
        lut_to_lut(self.lut1d, "3D", "3dl", outlutfile)
        # test wrong float range
        self.failUnlessRaises(ThreeDLHelperException, lut_to_lut, self.lut3d,
                              "3D", "3dl", outlutfile, input_range=[0.0, 1.0])
        # test wrong extension
        self.failUnlessRaises(LUTException, lut_to_lut, self.lut3d,
                              "3D", "csp", outlutfile, input_range=[0.0, 1.0])

    def tearDown(self):
        #Remove test directory
        shutil.rmtree(self.tmp_dir)

if __name__ == '__main__':
    unittest.main()
