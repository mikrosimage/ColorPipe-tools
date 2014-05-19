Plot that LUT
========================

** Developments under progress **

Plot that LUT is a python script for plotting look up tables.
It uses [OpenColorIO](http://opencolorio.org/) to read and process input LUTs, and [matplotlib](http://matplotlib.org/) to plot results.

Supported LUT formats : 3dl, csp, cub, cube, hdl, look, mga/m3d, spid1d, spi3d, spimtx, vf.
See [OpenColorIO FAQ](http://opencolorio.org/FAQ.html) for more informations.

See on [documentation site](http://mikrosimage.github.io/ColorPipe-tools/PlotThatLUT/).

Requirements
------------

+ OpenColorIO / PyOpenColorIO
+ Numpy 1.7.1 
+ Scipy 0.12
+ Argparse
+ Clint (optional)
+ Matplotlib 1.2.1 + a backend (for exemple Qt, Gtk...)

Tested config
-------------
- Python 2.6/2.7, Qt 4.8, OpenColorIO 1.0.8 / 1.0.8, matplotlib 1.2 on openSuse 12.1 and Windows 7

Command line usage
-----
See command line help :   
`ptlut.py -h`


Screenshots
-----------
![identity 3D](https://dl.dropboxusercontent.com/u/2979643/identity_3D_LUT.png "identity 3D")

![Rec709 1D](https://dl.dropboxusercontent.com/u/2979643/Rec709_1D_LUT.png "Rec709 1D")

![Web app](https://dl.dropboxusercontent.com/u/2979643/PlotThatLUT_webapp2.png "Web app")
