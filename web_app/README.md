ColorPipe-tools Web App
========================

** Developments under progress **

Use PlotThatLut and LutLab tools through a browser.

For now, only basic features of PlotThatLut are available.

See on [documentation site](http://mikrosimage.github.io/ColorPipe-tools/Web_app/).

Requirements
-------------------
+ OpenColorIO / PyOpenColorIO
+ Numpy 1.7.1 
+ Scipy 0.12
+ Argparse
+ Clint (optional)
+ Matplotlib 1.2.1
+ cherryPy 3.2.4
+ mako

Web app usage
-------------
You can test quickly in local by :  
- setting up your environnement ($PYTHONPATH, ...).  
- creating img and uploads directories.  
- and then launching :  
`python app.py`

For deeper usages, you'll have to customize your own cherryPy config (see server.conf).


Screenshots
-----------
![Web app](https://dl.dropboxusercontent.com/u/2979643/PlotThatLUT_webapp2.png "Web app")