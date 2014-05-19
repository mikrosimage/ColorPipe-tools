---
layout: page
title: PlotThatLUT
permalink: /PlotThatLUT/
---

Based on [OpenColorIO](http://opencolorio.org/), PlotThatLut allows to plot a LUT to understand its color transformation.
If it’s a 3D LUT, it displays a cube; if its a 1D LUT, a curve.

**Supported input formats** :  .3dl, .csp, .cub, .cube, .hdl, .look, .mga/m3d, .spi1d, .spi3d, .spimtx, .vf   
See [OpenColorIO documentation](http://opencolorio.org/FAQ.html).

PlotThatLUT can be used in command line :

`python plotThatLut/ptlut.py -h`

Or via the [web service]({{ site.url }}/Web_app/).

Examples :   

**Brightness**   

![Brightness]({{ site.url }}/imgs/brigthness.png)   

**Gamma curves**   

![Gamma curves]({{ site.url }}/imgs/gamma_curves.png)   

**Color temperature correction**   

![Color temperature correction]({{ site.url }}/imgs/colorbalance.png)   

**Desaturation**  

![Desaturation]({{ site.url }}/imgs/desaturation.png)   

**Gamut mapping (AdobeRGB -> sRGB)**  

![Gamut mapping (AdobeRGB -> sRGB)]({{ site.url }}/imgs/gamut_mapping.png)   
