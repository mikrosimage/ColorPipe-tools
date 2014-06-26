""" Chroma plot Testing

"""
import unittest
import matplotlib.pyplot as plt
from utils import matplotlib_helper as mplh
from utils import colorspaces

DISPLAY = False


class Test(unittest.TestCase):
    """Test chromaticity plotting

    """
    def test_chroma_plot(self):
        """Plot spectrum locus and standard gamut

        """
        plt.xlabel('chromaticity x')
        plt.ylabel('chromaticity y')
        plt.title("Standard Gamut")
        plt.axis([-0.1, 0.8, -0.4, 0.65])
        plt.grid(True)
        mplh.plot_spectrum_locus_76()
        mplh.plot_colorspace_gamut(colorspaces.ACES, lines_color="c",
                                   upvp_conversion=True)
        mplh.plot_colorspace_gamut(colorspaces.REC709, lines_color="m",
                                   upvp_conversion=True)
        plt.legend(loc=4)
        if DISPLAY:
            plt.show()
        plt.clf()
        plt.close()


if __name__ == "__main__":
    unittest.main()
