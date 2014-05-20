---
layout: post
title: "LUT to LUT"
permalink: /LUTLab/LUT_to_LUT/
---

Convert a LUT into another one.

Supported input formats :  .3dl, .csp, .cub, .cube, .hdl, .look, .mga/m3d, .spi1d, .spi3d, .spimtx, .vf

See [OpenColorIO documentation](http://opencolorio.org/FAQ.html).

Supported output formats :  csp, cube, 3dl, spi1d, spi3d, cc (Ace Color Cube), lut, json…  (to be continued)


Required parameters
-------------------------

* inlutfile : path to a LUT. Available input formats : ['.3dl', '.csp', '.cub', '.cube', '.hdl', '.look', '.mga/m3d', '.spi1d', '.spi3d', '.spimtx', '.vf']


**LUT export option**
You need to define at least a type (1D, 2D, 3D) and an output format (csp, cube, 3dl...) OR a preset.

* --out_type : 1D, 2D, 3D. Output LUT type. Beware: every format doesn't support each type. See format help.

* --out_format : 3dl,csp,cube,lut,spi,clcc,json. Output LUT format. Beware: 3dl, clcc, json are 3D only and lut is 1D/2D only.

**OR**

* --preset : lustre_3d, scratch_1d, scratch_3d, rv_3d, resolve_3d, csp_1d, clipster_1d, lustre_1d, clipster_3d, smoke_flame_3d . Use a LUT export preset to set output LUT arguments

[Find out more about presets]({{ site.url }}/presets/).

Optional parameters
-------------------------

**LUT export options**

* --outlutfile : path to the output LUT or to the output directory.
If it’s a directory : LUT name will be input LUT name + "export" suffix + new extension.
If this option is not used, output LUT will be written in input LUT directory and will be named as describe above.

* --input-range : Input range. Ex: 0.0 1.0 or 0 4095.  

* --output-range : Output range. Ex: 0.0 1.0 or 0 4095

* --out-bit-depth : Output lut bit precision (1D only). Ex : 10, 16, 32.

* --out-cube-size : Output cube size (3D only). Ex : 17, 33.

* --overwrite-preset : If a preset + other options are specified, it will overwrite preset values with the option values. Ex:  --preset lustre --output-range [0, 255], will use range defined by  --output-range

* --inverse : Invert input LUT (1D only)

* --smooth-size : smooth sub-sampling size (1D only). Ex : 10

**Debug parameters**

* --version : show program's version number and exit

* --full-versions : show version number of the program and its dependencies. And then exit

* --silent : hide log

* --trace : in case of error, print stack trace

Usage example
-------------------------

Let’s consider à 3D LUT named display.cube and imagine we want to use it in Clipster.
Clipster supports 3dl format with a 10 bits input bit depth (0-1023 range), a 12 bits output bit depth (0-4095 range) and a 17 cube size.

Precise command: 
  
`lut_to_lut --out_type 3D --out_format 3dl --input-range 0 1023 --output-range 0 4095 --out-cube-size 17 --outlutfile /path/display.3dl /path/display.cube`   

This extended version enables you to control precisely every parameter.
However, we may want to export a LUT more simply. That’s the role of default values which depends on the chosen format.
For example, for 3dl format, default values are : --input-range 0 1023 --output-range 0 4095 --out-cube-size 17.

Simplified command:   
 `lut_to_lut --out_type 3D --out_format 3dl --outlutfile /path/display.3dl /path/display.cube`   

We can also omit outlutfile parameter. This way, output LUT will be written in input LUT directory and will be named input LUT name + "export" suffix + new extension :   

 `lut_to_lut --out_type 3D --out_format 3dl /path/display.cube`   


This kind of command lines is possible when you know exactly what kind of formats are supported by the production software you are using. But there are many softwares and many combinations that may work… or not.

That’s why a preset system is also available.

Command with preset :   
 `lut_to_lut --preset clipster_3d /path/display.cube`   
[Find out more about presets]({{ site.url }}/presets/).

And if you just want a bigger cube size ? Use --overwrite-preset :   
 `lut_to_lut --preset clipster_3d  --out-cube-size 33 --overwrite-preset    /path/display.cube`

Those parameters seem too long ? Be aware that, as soon as there is no ambiguity, they can be shortened to their minimum. A good practise is to shorten the parameter so that the option is still recognizable :   

`lut_to_lut --preset clipster_3d  --out-cub 33 --overw /path/display.cube`   

Some shortcut are also available :    

`lut_to_lut --preset clipster_3d  --ocs 33 --overw /path/display.cube`   

All options can always be displayed with :   

`lut_to_lut -h`   
