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
        curve_to_lut('sRGB', None, self.tmp_dir, '1D', 'csp')
        curve_to_lut('sRGB', None, self.tmp_dir, '1D', 'csp',
                     direction="decode")
        # test gamma
        curve_to_lut(None, 2.2, self.tmp_dir, '1D', 'csp')
        curve_to_lut(None, 2.2, self.tmp_dir, '1D', 'csp', direction="decode")

        # test AlexaLogC, processed input range
        curve_to_lut('AlexaLogCV3', None, self.tmp_dir, '1D', 'csp',
                     process_input_range=True)

    def tearDown(self):
        # Remove test directory
        shutil.rmtree(self.tmp_dir)

if __name__ == '__main__':
    unittest.main()
