#!/bin/bash
export PATH=/datas/libs/build/build-OCIO-git/bin/:$PATH
export LD_LIBRARY_PATH=/datas/libs/build/build-OCIO-git/lib/:$LD_LIBRARY_PATH

##### versions and pathes
export python_version=2.6.2
export python_major_version=python2.6
export python_prefix=/datas/libs/pythonbrew/pythons/Python-$python_version
export python_exe_prefix=$python_prefix/bin

pythonbrew switch Python-$python_version

##### env var
##python
export PYTHONHOME=$python_prefix
export PYTHONPATH=$python_prefix/lib/$python_major_version/:$python_prefix/lib/$python_major_version/site-packages/

##bins and libs
export PATH=$python_prefix/bin/:/datas/mfe/workspace_ColorPipe_tools/ColorPipe-tools/plotThatLut:$PATH
export LD_LIBRARY_PATH=$python_prefix/lib/:$LD_LIBRARY_PATH

########## Setup OCIO binding path
export PYTHONPATH=/datas/libs/build/build-OCIO-git/lib/python2.6/site-packages/:/datas/mfe/workspace_ColorPipe_tools/ColorPipe-tools/:$PYTHONPATH

cd /datas/mfe/ColorPipe_tools/ColorPipe-tools/plotThatLut/
python plot_that_lut_web.py
