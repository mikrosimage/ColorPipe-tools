""" Testing Colorspaces model

"""
import unittest
import numpy
from utils.colorspaces import (REC709, ALEXALOGCV3, WIDEGAMUT, REC2020_12B,
                               ACESLOG_32f, sRGB, SGAMUTSLOG, SGAMUTSLOG2,
                               SGAMUTSLOG3, ACESCC, ACESPROXY_10i
                               )
from utils.colors_helper import apply_matrix, get_RGB_to_RGB_matrix, get_colorspace_matrix


class ColorspaceTest(unittest.TestCase):
    """ Test colorspaces transparency

    """
    def test_gradation(self):
        """ Test encode + decode

        """

        colorspace_to_test = [REC709,
                              ALEXALOGCV3,
                              WIDEGAMUT,
                              REC2020_12B,
                              ACESLOG_32f,
                              ACESCC,
                              sRGB,
                              SGAMUTSLOG,
                              SGAMUTSLOG2,
                              SGAMUTSLOG3,
                              ]
        for space in colorspace_to_test:
            name = space.__class__.__name__
            for value in [0.0, 1.0, 0.5]:
                res = space.decode_gradation(space.encode_gradation(value))
                message = ("{0} gradations not transparent ! "
                           "in: {1:8f} out: {2:8f}").format(name,
                                                            value,
                                                            res)
                self.assertTrue(numpy.isclose(res, value, atol=0.00000000000001), message)

    def test_aces_proxy(self):
        """Test ACES proxy (matrix + encoding)

        """
        ref_colors = [[0.001184464, 64.0, 0.001185417],
                      [222.875, 940.0, 222.860944204]
                      ]
        ACES_to_proxy_matrix = get_RGB_to_RGB_matrix('ACES', 'ACESproxy_10')
        proxy_to_ACES_matrix = get_RGB_to_RGB_matrix('ACESproxy_10', 'ACES')
        for color in ref_colors:
            aces_proxy_lin = apply_matrix(ACES_to_proxy_matrix, [color[0]]*3)[2]
            aces_proxy = ACESPROXY_10i._encode_gradation(aces_proxy_lin)
            self.assertEqual(aces_proxy, color[1])
            aces_proxy_lin = ACESPROXY_10i._decode_gradation(aces_proxy)
            aces = apply_matrix(proxy_to_ACES_matrix, [aces_proxy_lin]*3)[0]
            message = ("ACESproxy not valid ! "
                       "in: {0} out: {1}").format(aces, color[2])
            self.assertTrue(numpy.isclose(aces, color[2], atol=0.000001), message)

    def test_colorspace_matrices(self):
        """Test matrix conversions

        """
        ACES_to_XYZ = [[0.95255239593818575, 0.0, 9.3678631660468553e-05],
                       [0.34396644976507507, 0.72816609661348575, -0.072132546378560786],
                       [0.0, 0.0, 1.0088251843515859]]

        XYZ_to_ACES = [[1.0498110174979742, 0.0, -9.7484540579252874e-05],
                       [-0.49590302307731976, 1.3733130458157063, 0.098240036057309993],
                       [0.0, 0.0, 0.99125201820049902]]
        self.assertEqual(ACES_to_XYZ, get_colorspace_matrix("ACES").tolist())
        self.assertEqual(XYZ_to_ACES, get_colorspace_matrix("ACES", inv=True).tolist())

    def test_rgb_to_rgb_matrix(self):
        """Test rgb to rgb matrix

        """
        ACES_to_proxy_matrix = get_RGB_to_RGB_matrix('ACES', 'ACEScc')
        ref_value = numpy.matrix([[1.4514393161, -0.2365107469, -0.2149285693],
                                  [-0.0765537734,  1.1762296998,  -0.0996759264],
                                  [0.0083161484, -0.0060324498, 0.9977163014]])
        self.assertTrue(numpy.allclose(ACES_to_proxy_matrix, ref_value),
                        "Processed ACES to ACEScc matrix is different from reference ! ")
        ACES_to_Rec2020_matrix = get_RGB_to_RGB_matrix("ACES", 'Rec2020_12bits')
        ref_value = [[1.5128613853114372, -0.2589874063019148, -0.22978603267468098],
                            [-0.079036464595355627, 1.1770668323294038, -0.10075565571179679],
                            [0.0020912324769753847, -0.03114411050570343, 0.95350416068074784]]
        self.assertTrue(numpy.allclose(ACES_to_Rec2020_matrix, ref_value),
                        "Processed ACES to Rec2020 matrix is different from reference ! ")


if __name__ == "__main__":
    unittest.main()
