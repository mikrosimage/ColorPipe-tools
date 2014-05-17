---
layout: page
title: "About presets"
permalink: /presets/
---

Presets allow to define export parameters for a specific LUT format.
Ex: 3D LUT for Lustre, or 1D LUT for Clipster.

They can be used in LUT to LUT and Curve to LUT, and come in the form of json files.

Unless stipulated otherwise, presets are loaded from utils/presets directory that already contains some well known use cases : 

* clipster_1d.json,  
* clipster_3d.json,  
* lustre_1d.json,  
* lustre_3d.json,  
* resolve_3d.json,  
* rv_3d.json,  
* scratch_1d.json,  
* scratch_3d.json,  
* smoke_flame_3d.json

Customize preset path
-------------------------
You can specify where to load presets or add a path with LUT_PRESETS environment variable.

Write a preset
-------------------------

**Required attributes :**

* title: "a title"
* comment: "a comment"
* type: "1D", "2D", "3D"
* extension: ".csp", ".cube", ".spi1d", ".spi3d", ".cc", ".json", ".3dl" , ".lut"
* input_range: [0.0, 0.1], [-2.0, 5.0], [0, 1023], ...
* output_range: [0.0, 0.1], [-2.0, 5.0], [0, 1023], ...
* version: "1",  "version 1"...

**Required attributes for 1D/2D LUT :**

* output_bitdepth: 8, 10, 12, 16..

**Required attributes for 3D LUT :**

* cube_size: 17, 33, …

**Required attributes for 3dl format :**

3dl format can have two types of non-exclusive headers : a shaper LUT or a mesh. These headers are used to precise LUT sampling.

A shaper LUT defines an input range and a cube size.
Example with a [0, 1023] range and a 17 cube size : 
0 63 127 191 255 319 383 447 511 575 639 703 767 831 895 959 1023

A mesh defines a cube size and an output range. 
Example with a 17 cube size (17=(2^4)+1) and a 12 bits output range (=[0, 4095]) :
mesh 4 12

shaper: true ou false. If true, write shaper lut. Default = true.
mesh: true ou false.  If true, write mesh. Default = false.

**Optional attributes for ascii LUT (.lut)**

* layout: "triplet" or "block" ( default = "block").
Define how rgb values are written.
If "triplet" :    
r g b   
r g b   
(...)   
If "block" :    
r   
r   
(...)   
g   
g   
(...)   
b   
b   
* header_type: "lustre_header", "scratch_header", custom header (default : no header)
* is_float: true, false (default = false)

if layout = "triplet":   

* write_index: true, false (default = false). If true, write index value :    
0 r g b   
1 r g b   
(...)   

* write_alpha: true, false (default = false). If true,  write a default alpha :   
r g b 0.0   
r g b 0.0   
(...)   

* separator: " ", "\t", "     "... (default = " "). string between RGB values.   

Examples
-------------------------
**Preset 1D pour Lustre**   
`{   
"title": "Autodesk Lustre 1D LUT",   
"comment": "Generated with ColorPipe-tools",   
"type": "2D",   
"extension": ".lut",   
"output_range": [0, 65535],   
"input_range": [0, 65535],   
"output_bitdepth": 16,   
"version": "1",   
"layout": "triplet",   
"write_index": true,   
"separator": "\t",   
"header_type": "lustre_header"    
}`   

**Preset 3D pour Lustre**   
`{
"title": "Autodesk Lustre 3D LUT",
"comment": "Generated with ColorPipe-tools",
"type": "3D",
"extension": ".3dl",
"input_range": [0, 1023],
"output_range": [0, 4095],
"cube_size": 17,
"version": "1",
"shaper": true,
"mesh": true
}`

**Preset 1D pour Scratch**   
`{
"title": "Assimilate Scratch 1D LUT",
"comment": "Generated with ColorPipe-tools",
"type": "1D",
"extension": ".lut",
"output_range": [0, 1023],
"input_range": [0, 1023],
"output_bitdepth": 10,
"version": "1",
"layout": "block",
"header_type": "scratch_header"
}`

**Preset 3D pour RV**   
`{
"title": "Tweak Software RV 3D LUT",
"comment": "Generated with ColorPipe-tools",
"type": "3D",
"extension": ".cube",
"output_range": [0.0, 1.0],
"cube_size": 17,
"input_range": [0.0, 1.0],
"version": "1"
}`
