#!/usr/bin/python
"""A cherrypy **Web** app for ColorPipe-Tools.

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.0"
import cherrypy
from mako.lookup import TemplateLookup
import os
import ntpath
import traceback
from plotThatLut import plot_that_lut
from utils import matplotlib_helper as mplh

mplh.WEB_MODE = True

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MY_LOOKUP = TemplateLookup(directories=[os.path.join(CURRENT_DIR, 'html')])


class Application(object):
    """CherryPy Application

    """
    @cherrypy.expose
    def index(self):
        """ColorPipe-tools index page

        """
        mytemplate = MY_LOOKUP.get_template("index.html")
        return mytemplate.render()

    @cherrypy.expose
    def plotThatLutIndex(self):
        """PlotThatLUT index page

        """
        mytemplate = MY_LOOKUP.get_template("PlotThatLut/index.html")
        return mytemplate.render()

    @cherrypy.expose
    def plotThatLutUpload(self, lutfile, lut_type, count, custom_count,
                          inverse=False, prelutfile=None, postlutfile=None):
        """PlotThatLUT plot page

        Args:
            lutfile (str): path to a color transformation file (lut, matrix...)

            lut_type (str): possible values are 'curve' or 'cube'

            count: possible values are 'custom' or 'auto'

            custom_count (int): custom count value

        kwargs:
            inverse (bool): inverse input lut

            prelutfile (str): path to a pre LUT

            postlutfile (str): path to a post LUT

        """
        # copy uploaded files on the server to use it with plot_that_lut
        backup_filename = self.__copy_uploaded_file(lutfile)
        backup_pre_filename = None
        backup_post_filename = None
        if prelutfile.file:
            backup_pre_filename = self.__copy_uploaded_file(prelutfile)
        if postlutfile.file:
            backup_post_filename = self.__copy_uploaded_file(postlutfile)
        # init args
        if count == 'custom':
            tmp_count = int(custom_count)
            display_count = str(tmp_count)
        else:
            tmp_count = None
            display_count = count
        if inverse:
            inverse_text = "Yes"
        else:
            inverse_text = "No"
        label = ('Displaying : {0} (type : {1}, samples : {2}, inverted : {3})'
                 ).format(backup_filename, lut_type, display_count,
                          inverse_text)
        if prelutfile.file:
            label = ('{0}<br>Pre-LUT : {1}').format(label, backup_pre_filename)
        if postlutfile.file:
            label = ('{0}<br>Post-LUT : {1}').format(label,
                                                     backup_post_filename)
        # call plot_that_lut to export the graph
        try:
            result = plot_that_lut.plot_that_lut(backup_filename, lut_type,
                                                 tmp_count, inverse,
                                                 backup_pre_filename,
                                                 backup_post_filename)
            result = (
                '<img src="/{0}" width="640" height="480"'
                'border="0"/>'
            ).format(result)
        except Exception, e:
            error = str(e).replace('\n', '<br>')
            result = (
                "<h2>Something went wrong ! </h2>"
                "<br>"
                '<font color="#FF0000">{0}</font><br>'
            ).format(error)
            print traceback.format_exc()
        # call template
        mytemplate = MY_LOOKUP.get_template("PlotThatLut/plot.html")
        return mytemplate.render(label=label, image=result)

    @staticmethod
    def __copy_uploaded_file(upfile):
        """Copy uploaded file on the server and return its path

        Args:
            file (file): path to a file

        Returns:
            str.
        """
        # read data
        all_data = ''
        while True:
            data = upfile.file.read(8192)
            if not data:
                break
            all_data += data
        # copy uploaded file on the server
        filename = ntpath.basename(upfile.filename)
        backup_filename = "{0}/uploads/{1}".format(CURRENT_DIR, filename)
        saved_file = open(backup_filename, 'wb')
        saved_file.write(all_data)
        saved_file.close()
        return backup_filename

# Application root
APP_ROOT = Application()

# Set up root configuration
CSS_FILE = os.path.join(CURRENT_DIR, 'css', 'style.css')
IMG_DIR = os.path.join(CURRENT_DIR, 'img')
UPLOAD_DIR = os.path.join(CURRENT_DIR, 'uploads')
FAVICON_FILE = os.path.join(CURRENT_DIR, 'icons', 'favicon.ico')
APP_CONF = {'/css/style.css': {'tools.staticfile.on': True,
                               'tools.staticfile.filename': CSS_FILE
                               },
            '/img':           {'tools.staticdir.on': True,
                               'tools.staticdir.dir': IMG_DIR
                               },
            '/uploads':       {'tools.staticdir.on': True,
                               'tools.staticdir.dir': UPLOAD_DIR
                               },
            '/favicon.ico': {'tools.staticfile.on': True,
                             'tools.staticfile.filename': FAVICON_FILE
                             }
            }

# Update server config
cherrypy.config.update(os.path.join(CURRENT_DIR, "server.conf"))

# Start server
cherrypy.quickstart(APP_ROOT, config=APP_CONF)
cherrypy.engine.start()
