LUT Lab
========================

** Developments under progress **

Utility scripts to convert and manipulate Look Up Tables.
It uses [OpenColorIO](http://opencolorio.org/) to read and process input LUTs.

Available scripts :   

- **lut_to_lut**: convert a lut into another format. For now, only conversion to 1D/2D/3D cube or 1D/2D csp is supported   

- **ext_1d_lut**: extract the tone mapping curve of a 3D LUT using a bicubic interpolation (or not)   


Supported input LUT formats : 3dl, csp, cub, cube, hdl, look, mga/m3d, spid1d, spi3d, spimtx, vf.   
See [OpenColorIO FAQ](http://opencolorio.org/FAQ.html) for more informations.

Requirements
------------
- Python
- OpenColorIO Python binding

Optional:   
- matplotlib + a backend (for exemple Qt, Gtk...)

Tested config
-------------
- Python 2.6, Qt 4.8, OpenColorIO 1.0.8, matplotlib 1.2 on openSuse 12.1

Command line usage
-----
See command line help :   
`lut_to_lut.py -h`   
`ext_1d_lut.py -h`   

Screenshots
-----------
ext_1d_lut : no smooth vs smooth option
![ext_1d_lut](https://dl.dropboxusercontent.com/u/2979643/ext_1d_lut_compare.png "ext_1d_lut")


