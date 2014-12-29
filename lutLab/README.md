LUT Lab
========================

** Developments under progress **

Utility scripts to convert and manipulate Look Up Tables.
It uses [OpenColorIO](http://opencolorio.org/) to read and process input LUTs.

Supported input LUT formats : 3dl, csp, cub, cube, hdl, look, mga/m3d, spid1d, spi3d, spimtx, vf.   
See [OpenColorIO FAQ](http://opencolorio.org/FAQ.html) for more informations.

See on [documentation site](http://mikrosimage.github.io/ColorPipe-tools/LUTLab/).

Available scripts :   

###lut_to_lut
> Convert a LUT into another format

>Main options  
>  *--out_type {1D,2D,3D}* : Output LUT type   
>  *--out_format {3dl,csp,cube,lut,spi,clcc,json}* : Output LUT format   
>  *--input-range INPUT_RANGE* : Input range. Ex: 0.0 1.0 or 0 4095   
>  *--output-range OUTPUT_RANGE* : Output range. Ex: 0.0 1.0 or 0 4095   
>  *--out-bit-depth OUT_BIT_DEPTH* : Output lut bit precision (1D only). Ex : 10, 16, 32.   
>  *--out-cube-size OUT_CUBE_SIZE* : Output cube size (3D only). Ex : 17, 32.   
>  *--preset PRESET* : Use a LUT export preset to set output LUT arguments   
>  *--inverse*       Inverse input LUT (1D only)   
>  *--smooth-size SMOOTH_SIZE* : Smooth sub-sampling size (1D only). Ex : 10

See all options :   
`python lut_to_lut.py -h`  

###curve_to_lut   
>Create lut file corresponding to a colorspace or gamma gradation

>Main options  
>  *--colorspace* : RGB Colorspace. See colorspaces.py to see available colorspaces.  
>  *--gamma GAMMA* :Input pure gamma gradation   
>  *--direction {encode,decode}* : Direction : encode or decode.   
>  *--out_type {1D,2D,3D}* : Output LUT type   
>  *--out_format {3dl,csp,cube,lut,spi,clcc,json}* : Output LUT format   
>  *--input-range INPUT_RANGE* : Input range. Ex: 0.0 1.0 or 0 4095   
>  *--output-range OUTPUT_RANGE* : Output range. Ex: 0.0 1.0 or 0 4095   
>  *--out-bit-depth OUT_BIT_DEPTH* : Output lut bit precision (1D only). Ex : 10, 16, 32.   
>  *--out-cube-size OUT_CUBE_SIZE* : Output cube size (3D only). Ex : 17, 32.   
>  *--preset PRESET* : Use a LUT export preset to set output LUT arguments  

See all options :   
`python curve_to_lut.py -h` 

###rgb_to_xyz_matrix   
> Generate RGB colorspace <-> XYZ conversion matrix     

>Main options  
>  *--colorspace* : RGB Colorspace. See colorspaces.py to see available colorspaces.   
>  *-format {matrix,spimtx,simple}* : Output formatting.

See all options :   
`python rgb_to_xyz_matrix.py -h`

###plot_that_chroma   
>Plot chromaticities in a xy or u'v' diagram

>Main options   
>  *--colorspace* : RGB Colorspace. See colorspaces.py to see available colorspaces.   
>  *--point x y* :  Display an xy point   
>  *--spectrum-locus* : Display spectrum locus   

See all options :   
`python plot_that_chroma.py -h` 


Requirements
-------------------

+ OpenColorIO / PyOpenColorIO (tested versions: 1.0.8 | 1.0.9)
+ Numpy (tested versions: 1.7.1 | 1.9.1)
+ Scipy 0.12 (tested versions: 0.12 | 0.14)
+ Argparse
+ Clint (optional)

####For plot that chroma
+ Matplotlib (tested versions: 1.2.1 | 1.4.2) + a backend (for exemple Qt, Gtk...)

Tested config
-------------
- Python 2.6/2.7, Qt 4.8, OpenColorIO 1.0.8 / 1.0.8, matplotlib 1.2 on openSuse 12.1 and Windows 7
- Python 2.6/2.7, Qt 4.8, OpenColorIO 1.0.9, matplotlib 1.4.2 on Centos 6.5

Screenshots
-----------
####lut_to_lut : no smooth vs smooth option
![LUT to LUT smooth](https://dl.dropboxusercontent.com/u/2979643/ext_1d_lut_compare.png "ext_1d_lut")

####Plot that chroma   
![Plot that chroma](https://dl.dropboxusercontent.com/u/2979643/plot_that_chroma.jpg "Plot that chroma")
