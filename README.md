ColorPipe-tools
===============

** Developments under progress **

Tools for Color Pipelines.

Includes :

+ [plotThatLUT](https://github.com/mikrosimage/ColorPipe-tools/tree/master/plotThatLut) is a python script for plotting look up tables based on [OpenColorIO](http://opencolorio.org/) and [matplotlib](http://matplotlib.org/).

![plotThatLUT](https://dl.dropboxusercontent.com/u/2979643/plotThatLUT.png "plotThatLUT")

+ [lutLab](https://github.com/mikrosimage/ColorPipe-tools/tree/master/lutLab) contains utility python scripts to convert and manipulate Look Up Tables.

Available scripts :   

**lut_to_lut**: convert a 1D/2D/3D lut into another format.   

**ext_1d_lut**: extract the tone mapping curve of a 3D LUT using a bicubic interpolation (or not)   

**rgb_to_xyz_matrix**: generate RGB colorspace to XYZ conversion matrix    

**curve_to_lut**: Export a LUT from a colorspace gradation function



+ [web_app](https://github.com/mikrosimage/ColorPipe-tools/tree/master/web_app) is a web version of the previous tools based on [cherryPy](http://www.cherrypy.org/).

![Web app](https://dl.dropboxusercontent.com/u/2979643/PlotThatLUT_webapp2.png "Web app")