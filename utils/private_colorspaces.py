""" Private colorspace definitions
    These colorspaces don't have public specifications.
    To add a colorspace, see example below.

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
from utils.colorspaces import AbstractColorspace

# class DCI(AbstractColorspace):
#     """DCI colorspace

#     """
#     def get_red_primaries(self):
#         # See DCI specifications
#         pass

#     def get_green_primaries(self):
#         # See DCI specifications
#         pass

#     def get_blue_primaries(self):
#         # See DCI specifications
#         pass

#     def get_white_point(self):
#         # See DCI specifications
#         pass

#     def encode_gradation(self, value):
#         # See DCI specifications
#         pass

#     def decode_gradation(self, value):
#         # See DCI specifications
#         pass


# class DCID60(DCI):
#     """DCI colorspace with D60 white point

#     """
#     def get_white_point(self):
#         return 0.3217, 0.3378

PRIVATE_COLORSPACES = {
    # 'DCI': DCI(),
    # 'DCI_D60': DCID60()
}
