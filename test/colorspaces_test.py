""" Testing Colorspaces model

"""
import unittest
from utils.colorspaces import (REC709, ALEXALOGCV3, WIDEGAMUT, REC2020_12B,
                               ACESLOG_32f, sRGB, SGAMUTSLOG, SGAMUTSLOG2,
                               SGAMUTSLOG3,
                               )


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
                                sRGB,
                                SGAMUTSLOG,
                                SGAMUTSLOG2,
                                SGAMUTSLOG3,
                            ]
        delta = 0.000000000000001
        for space in colorspace_to_test:
            name = space.__class__.__name__
            for value in [0.0, 1.0, 0.5]:
                res = space.decode_gradation(space.encode_gradation(value))
                diff = abs(res - value)
                message = ("{0} gradations not transparent ! "
                           "in: {1:8f} out: {2:8f}").format(name,
                                                      value,
                                                      res)
                self.assert_(diff < delta, message)


if __name__ == "__main__":
    unittest.main()
