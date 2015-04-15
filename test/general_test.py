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

    def test_colorspace_matrices(self):
        """Test matrix conversions

        """
        ACES_to_XYZ = [[0.95255239593818575, 0.0, 9.3678631660468553e-05],
                       [0.34396644976507507, 0.72816609661348575, -0.072132546378560786],
                       [0.0, 0.0, 1.0088251843515859]]

        XYZ_to_ACES = [[1.0498110174979742, 0.0, -9.7484540579252874e-05],
                       [-0.49590302307731976, 1.3733130458157063, 0.098240036057309993],
                       [0.0, 0.0, 0.99125201820049902]]
        ACES_to_Rec2020 = [[1.5128613853114372, -0.2589874063019148, -0.22978603267468098],
                           [-0.079036464595355627, 1.1770668323294038, -0.10075565571179679],
                           [0.0020912324769753847, -0.03114411050570343, 0.95350416068074784]]

        self.assertEqual(ACES_to_XYZ, get_colorspace_matrix("ACES").tolist())
        self.assertEqual(XYZ_to_ACES, get_colorspace_matrix("ACES", inv=True).tolist())
        self.assertEqual(ACES_to_Rec2020, get_RGB_to_RGB_matrix("ACES", 'Rec2020_12bits').tolist())

    def tearDown(self):
        # Remove test directory
        shutil.rmtree(self.tmp_dir)


if __name__ == '__main__':
    unittest.main()
