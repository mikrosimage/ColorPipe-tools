""" General Testing

"""
import unittest
from plotThatLut import plot_that_lut
import os
import tempfile
import shutil
from utils.colors_helper import get_colorspace_matrix, get_RGB_to_RGB_matrix


DISPLAY = False


class GeneralTest(unittest.TestCase):
    """General Test : plot lut 1d/3d, convert lut, extract 1d lut

    """
    def setUp(self):
        test_dir = os.path.join(os.path.dirname(__file__), 'test_files')
        self.lut1d = os.path.join(test_dir, 'CineonToLin_1D.csp')
        self.lut3d = os.path.join(test_dir, 'identity.3dl')
        self.tmp_dir = os.path.join(tempfile.gettempdir(), 'testCoPipe')
        os.mkdir(self.tmp_dir)

    def test_lut_1d(self):
        """Open a 1D LUT and display it

        """
        if DISPLAY:
            plot_that_lut.plot_that_lut(self.lut1d,
                                        count=plot_that_lut.DEFAULT_SAMPLE)
        else:
            # TODO
            pass

    def test_lut_3d(self):
        """Open a 3D LUT and display it

        """
        if DISPLAY:
            plot_that_lut.plot_that_lut(self.lut3d,
                                        count=plot_that_lut.DEFAULT_CUBE_SIZE)
        else:
            # TODO
            pass

    def tearDown(self):
        # Remove test directory
        shutil.rmtree(self.tmp_dir)


if __name__ == '__main__':
    unittest.main()
