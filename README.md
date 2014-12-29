ColorPipe-tools
===============

** Developments under progress **

Tools for Color Pipelines.

See [documentation site](http://mikrosimage.github.io/ColorPipe-tools/about/).

Tools overview
---------------

###Plot That LUT
[plotThatLUT](https://github.com/mikrosimage/ColorPipe-tools/tree/master/plotThatLut) is a python script for plotting look up tables based on [OpenColorIO](http://opencolorio.org/) and [matplotlib](http://matplotlib.org/).

![plotThatLUT](https://dl.dropboxusercontent.com/u/2979643/plotThatLUT.png "plotThatLUT")

###LUT Lab
[lutLab](https://github.com/mikrosimage/ColorPipe-tools/tree/master/lutLab) contains utility python scripts to convert and manipulate Look Up Tables.

Available scripts :   

**lut_to_lut**: convert a 1D/2D/3D LUT into another format.   

**curve_to_lut**: export a LUT from a colorspace gradation function

**rgb_to_xyz_matrix**: generate RGB colorspace to XYZ conversion matrix     

**plot_that_chroma**: plot chromaticity coordinates.

![Plot that chroma](https://dl.dropboxusercontent.com/u/2979643/plot_that_chroma.jpg "Plot that chroma")

###Web app
[web_app](https://github.com/mikrosimage/ColorPipe-tools/tree/master/web_app) is a web version of the previous tools based on [cherryPy](http://www.cherrypy.org/).

![Web app](https://dl.dropboxusercontent.com/u/2979643/PlotThatLUT_webapp2.png "Web app")

Requirements
-------------------

+ OpenColorIO / PyOpenColorIO (tested versions: 1.0.8 | 1.0.9) 
+ Numpy (tested versions: 1.7.1 | 1.9.1) 
+ Scipy (tested versions: 0.12 | 0.14) 
+ Argparse
+ Clint (optional)

####For plot tools
+ Matplotlib (tested versions: 1.2.1 | 1.4.2) 

####For web app
+ cherryPy (tested versions: 3.2.4 | 3.6.0) 
