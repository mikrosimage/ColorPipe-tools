---
layout: page
title: About
permalink: /about/
---

ColorPipe-tools is a set of tools to handle and process LUTs or color spaces.
This project is in line with [ColorPipe blog](http://colorpipe.mikrosimage.eu/en/).


It includes : 

**PlotThatLUT**


Based on [OpenColorIO](http://opencolorio.org/), PlotThatLut allows to plot a LUT to understand its color transformation.
If it’s a 3D LUT, it displays a cube; if its a 1D LUT, a curve.

PlotThatLUT is available as a command line tool or as a web service.

[Find out more]({{ site.url }}/PlotThatLUT/).

**LUTLab**


Also based on [OpenColorIO](http://opencolorio.org/), LUTLab gathers a set of scripts to convert LUTs or color spaces.

For now, LUTLab is only available in command line but is intended to become part of a web service.

[Find out more]({{ site.url }}/LUTLab/).

##Dev

Github : [mikrosimage/ColorPipe-tools](https://github.com/mikrosimage/ColorPipe-tools)

License : see [LICENSE](https://github.com/mikrosimage/ColorPipe-tools/blob/master/LICENSE)

###Requirements

+ OpenColorIO / PyOpenColorIO
+ Numpy 1.7.1 
+ Scipy 0.12
+ Argparse
+ Clint (optional)

####For plot tools
+ Matplotlib 1.2.1

####For web app
+ cherryPy 3.2.4
