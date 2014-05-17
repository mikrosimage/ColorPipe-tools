---
layout: page
title: "Curve to LUT"
permalink: /LUTLab/Curve_to_LUT/
---

Convert a gradation function in a 1D/2D LUT.

Supported output formats :  csp, cube, 3dl, spi1d, spi3d, cc (Ace Color Cube), lut, json…  (to be continued)

Curve to LUT let you process LUTs that correspond to the gradation of a standard color space (for which we know the mathematical functions) :

* sRGB to lin (and its inverse), 
* AlexaLogCV3 to lin (and its inverse),
* But also Gamma 2.2 to lin (and its inverse),
* ...

Process from the mathematical functions (and not from another LUT) allows to compute a more precise LUT.

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



Required parameters
-------------------------

* outlutfile : path to the output LUT or to the output directory.
If it’s a directory : LUT name will be deduced from the applied transformation.

**Gradation options**

* --colorspace : standard color space. Possible values : ACESlog_16i / ACESlog_32f, ACESproxy_10 / ACESproxy_12, AlexaLogCV3, DCI / DCI_D60, Rec2020_10bits / Rec2020_12bits, Rec709, sRGB, SGamut3CineSLog3, SGamutSLog, SGamutSLog2, SGamutSLog3, WideGamut

**OR**

* --gamma : gamma value. Ex: 1.8, 2.2, 2.4...

**LUT export options**

You need to define at least a type (1D, 2D, 3D) and an output format (csp, cube, 3dl...) OR a preset.

* --out_type : 1D, 2D, 3D. Output LUT type. Beware: every format doesn't support each type. See format help.

* --out_format : 3dl,csp,cube,lut,spi,clcc,json. Output LUT format. Beware: 3dl, clcc, json are 3D only and lut is 1D/2D only.

**OR**

* --preset : lustre_3d, scratch_1d, scratch_3d, rv_3d, resolve_3d, csp_1d, clipster_1d, lustre_1d, clipster_3d, smoke_flame_3d . Use a LUT export preset to set output LUT arguments

[Find out more about presets]({{ site.url }}/presets/).

Warning : Curve to LUT doesn’t prevent you from writing those LUTs in 3D formats. However it’s strongly advised to use 1D/2D LUTs. A 3D LUT may not be precise enough to bake a gradation.


Optional parameters
-------------------------

**Gradation parameters**

* --direction : encode (lin to color space or gamma) or decode (color space or gamma to lin). Default : encode.

* --process-input-range : compute automatically input range. Useful when a transformation goes far beyond classical [0.0, 1.0] range to process a LUT that doesn’t clip. Ex : Lin to Log.

**LUT export parameters**

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

Lustre supports a specific 1D/2D LUT format. A preset is available to export this format.

`curve_to_lut --colorspace sRGB --preset lustre_3d /path/`   
This command will write /path/Lin_to_sRGB.lut (we encode by default).

To get inverse transform:   

`curve_to_lut --colorspace sRGB --preset lustre_3d --direction decode /path/`   
This command will write  /path/sRGB_to_Lin.lut.

All options :   
`curve_to_lut -h`   

For more tips on command line usage and export options, see LUT to LUT example.
