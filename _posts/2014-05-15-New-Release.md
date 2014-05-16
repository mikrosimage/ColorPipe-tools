---
layout: post
title: "New release - v0.11"
date: "2014-05-15"
author: Marie FETIVEAU
version: v0.11
categories: [release]
---

**LUTLab**
* lut_to_lut and curve_to_lut can now use presets file to define export LUT settings.
See some samples [here](https://github.com/mikrosimage/ColorPipe-tools/tree/master/utils/presets).

* ext_to_1d_lut has been merge into lut_to_lut. Say hello to  --smooth-size option !

* curve_to_lut has now on option to auto-detect input range : --process-input-range

There's many changes on these tools, see [LUT to LUT]({{ site.url }}/LUTLab/LUT_to_LUT/), [Curve to LUT]({{ site.url }}/LUTLab/Curve_to_LUT/) and [presets]({{ site.url }}/presets/) pages.

**Utils**
* New helper : 3dl
* Improved helper : spi, cube, csp, ascii


**Dev**
* Lots of refactoring
* New tests (and a jenkins build).

**Doc**
* Update of the github.io site
