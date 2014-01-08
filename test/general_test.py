""" General Testing

"""
import unittest
import plot_that_lut
import os
import tempfile
import shutil
import lut_to_lut
import ext_1d_lut
import rgb_to_xyz_matrix


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
        plot_that_lut.plot_that_lut(self.lut1d,
                                    count=plot_that_lut.DEFAULT_SAMPLE)

    def test_lut_3d(self):
        """Open a 3D LUT and display it

        """
        plot_that_lut.plot_that_lut(self.lut3d,
                                    count=plot_that_lut.DEFAULT_CUBE_SIZE)

    def test_convert_lut(self):
        """Open a CSP LUT into a CUBE lut, and the resulting LUT into a csp
            LUT

        """
        cube_lut = os.path.join(self.tmp_dir, "identity.cube")
        lut_to_lut.lut_to_lut(self.lut1d, cube_lut, lut_type='1D_CUBE')
        lut_to_lut.lut_to_lut(cube_lut, lut_type='1D_CSP')

    def test_extract_lut(self):
        """Extract the 1d composante of a 3D LUT and plot the result

        """
        csp_lut = os.path.join(self.tmp_dir, "identity_3d_export.csp")
        ext_1d_lut.extract_1d_lut(self.lut3d, 10, csp_lut, True)
        plot_that_lut.plot_that_lut(csp_lut)

    def tearDown(self):
        #Remove test directory
        shutil.rmtree(self.tmp_dir)


if __name__ == '__main__':
    unittest.main()
