""" Testing curve_to_lut model

"""
import unittest
import shutil
import os
import tempfile
from lutLab.curve_to_lut import curve_to_lut


class CurveToLUTTest(unittest.TestCase):
    """ Test lut_to_lut tool

    """
    def setUp(self):
        self.tmp_dir = os.path.join(tempfile.gettempdir(), 'testCoPipe')
        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)

    def test_curve(self):
        """ Test curve to LUT

        """
        # test colorspace
        curve_to_lut('sRGB', None, '1D', 'csp', self.tmp_dir)
        curve_to_lut('sRGB', None, '1D', 'csp', self.tmp_dir,
                     direction="decode")
        # test gamma
        curve_to_lut(None, 2.2, '1D', 'csp', self.tmp_dir)
        curve_to_lut(None, 2.2, '1D', 'csp', self.tmp_dir, direction="decode")

    def tearDown(self):
        #Remove test directory
        shutil.rmtree(self.tmp_dir)

if __name__ == '__main__':
    unittest.main()
