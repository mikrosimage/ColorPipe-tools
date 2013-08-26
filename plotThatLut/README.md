Plot that LUT
========================

Plot that LUT is a python script for plotting look up tables.
It uses [OpenColorIO](http://opencolorio.org/) to read and process input LUTs, and [matplotlib](http://matplotlib.org/) to plot results.

Supported LUT formats : 3dl, csp, cub, cube, hdl, look, mga/m3d, spid1d, spi3d, spimtx, vf.
See [OpenColorIO FAQ](http://opencolorio.org/FAQ.html) for more informations.

Requirements
------------
- Python
- matplotlib + a backend (for exemple Qt, Gtk...)
- OpenColorIO Python binding

To use plotThatLutWeb.py :  

- CherryPy

Tested config
-------------
- Python 2.6, Qt 4.8, OpenColorIO 1.0.8, matplotlib 1.2, CherryPy 3.2.4 on openSuse 12.1

Command line usage
-----
* Dispay a cube (17 segments) for 3D LUTs and matrixes or a curve (256 points) for 1D/2D LUTs :   
`plotThatLut.py < path to a LUT >`

* Display a curve with x points (default value : 256) :   
`plotThatLut.py < path to a LUT > curve [points count]`

* Display a cube with x segments (default value : 17) :   
`plotThatLut.py < path to a LUT > cube [cube size]`

Web app usage
-------------
You can test quickly in local by :  
- setting up your environnement ($PYTHONPATH, ...).  
- creating img and uploads directories.  
- and then launching :  
`plotThatWeb.py`

For deeper usages, you'll have to customize your own cherryPy config.

Screenshots
-----------
![identity 3D](https://dl.dropboxusercontent.com/u/2979643/identity_3D_LUT.png "identity 3D")

![Rec709 1D](https://dl.dropboxusercontent.com/u/2979643/Rec709_1D_LUT.png "Rec709 1D")

![Web app](https://dl.dropboxusercontent.com/u/2979643/PlotThatLUT_webapp.png "Web app")
