---
layout: page
title: LUTLab
permalink: /LUTLab/
---

Based on [OpenColorIO](http://opencolorio.org/), LUTLab gathers a set of scripts to convert LUTs or color spaces.
For now, LUTLab is only available in command line but is intended to become part of a web service.

Four tools are currently available :

lut_to_lut
-------------------------
**convert a LUT into another one.**

Supported input formats :  .3dl, .csp, .cub, .cube, .hdl, .look, .mga/m3d, .spi1d, .spi3d, .spimtx, .vf
Supported output formats :  csp, cube, 3dl, spi1d, spi3d, cc (Ace Color Cube), lut, json…  (to be continued)

lut_to_lut can also invert or smooth an 1D/2D LUT.

[Find out more]({{ site.url }}/LUTLab/LUT_to_LUT/).

curve_to_lut 
-------------------------
**convert a gradation function in a 1D/2D LUT.**

Supported output formats :  csp, cube, 3dl, spi1d, spi3d, cc (Ace Color Cube), lut, json…  (to be continued)

Available gradations : 

* ACESlog_16i / ACESlog_32f, ACESproxy_10 / ACESproxy_12,
* AlexaLogCV3,
* DCI / DCI_D60,
* Rec2020_10bits / Rec2020_12bits,
* Rec709,
*  sRGB,
* SGamut3CineSLog3, SGamutSLog, SGamutSLog2, 
* SGamutSLog3,
* WideGamut,
* gamma custom,
* to be continued …

[Find out more]({{ site.url }}/LUTLab/Curve_to_LUT/).

rgb_to_xyz_matrix 
-------------------------
**display XYZ conversion matrices and their inverse.**

Available gradations : 

* ACES, ACESlog_16i / ACESlog_32f, ACESproxy_10 / ACESproxy_12,
* AlexaLogCV3,
* DCI, DCI_D60,
* Rec2020_10bits / Rec2020_12bits
* Rec709 / sRGB,
* SGamut3CineSLog3, SGamutSLog, SGamutSLog2, SGamutSLog3,
* WideGamut,
* to be continued …

Find out more:
`rgb_to_xyz_matrix -h`

plot_that_chroma 
-------------------------
**Plot chromaticities in a xy or u'v' diagram**

Main options

* --colorspace : RGB Colorspace. See colorspaces.py to see available colorspaces.
* --point x y : Display an xy point
* --spectrum-locus : Display spectrum locus

See all options :
`python plot_that_chroma.py -h`

![PlotThatChroma]({{ site.url }}/imgs/plot_that_chroma.jpg)
