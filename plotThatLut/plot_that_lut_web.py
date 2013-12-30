#!/usr/bin/python

"""A cherrypy **Web** app for plot_that_lut.

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "Prototype"
from os import path
import ntpath
import sys
import traceback

from cherrypy import quickstart, tree, server
import plot_that_lut


class PlotThatLutWeb(object):
    """cherrypy publication object

    """
    def html(self, body):
        """ Return an html page

        Args:
            body (str): html code to insert in the body of the html page

        Returns:
            str.

        """
        return (
            "<html>\n"
            "<head>\n"
            "    <title>Plot That Lut</title>\n"
            '    <link rel="stylesheet" type="text/css" href="css/style.css">\n'
            "</head>\n"
            "<body>\n"
            '        <div id="content">\n'
            '            <div id="header"><h1># Plot That LUT #</h1></div>\n'
            '            <div id="text">\n'
            '               {0}\n'
            '           </div>\n'
            '        </div>\n'
            '</body>\n'
            '</html>\n'
        ).format(body)

    def form(self):
        """Return plot that lut web ui

        Returns:
            str.

        """
        return (
            '<form action="upload" method="post" '
            'enctype="multipart/form-data">\n'
            '    Choose LUT file: <input type="file" name="lutfile"/><br/>\n'
            "    Lut Type:"
            '    <input type="radio" name="lut_type" value="auto" '
            'checked=true> auto\n'
            '    <input type="radio" name="lut_type" value="curve"> curve\n'
            '    <input type="radio" name="lut_type" value="cube"> cube\n'
            "    <br>\n"
            "    Samples count:\n"
            '    <input type="radio" name="count" value="auto" checked=true> '
            'auto\n'
            '    <input type="radio" name="count" value="custom"> custom :\n'
            '    <input type="text" name="custom_count" value=17 size=5>\n'
            "    <br>\n"
            '    <div id="advanced">\n'
            "    # Advanced options #<br>\n"
            '    <input type="checkbox" name="inverse" value="1">Reverse main '
            "LUT (for 1D / 2D LUT only)<br>\n"
            '    Choose a pre-lut : <input type="file" name="prelutfile"/>\n'
            "    <br>\n"
            '    Choose a post-lut : <input type="file" name="postlutfile"/>\n'
            '    </div>\n'
            "<br>\n"
            '    <input type="submit"/>\n'
            "</form>"
        )

    def index(self):
        """Index page

        Returns:
            str.

        .. note:: required by cherrypy

        """
        return self.html(self.form())
    index.exposed = True

    @staticmethod
    def __copyUploadedFile(upfile):
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
        backup_filename = "{0}/uploads/{1}".format(currdir,
                                                   ntpath.basename(
                                                   upfile.filename))
        saved_file = open(backup_filename, 'wb')
        saved_file.write(all_data)
        saved_file.close()
        return backup_filename

    def upload(self, lutfile, lut_type, count, custom_count, inverse=False,
               prelutfile=None, postlutfile=None):
        """Upload page

        Args:
            lutfile : path to a color transformation file (lut, matrix...)

            lut_type (str): possible values are 'curve' or 'cube'

            count: possible values are curve size or curve samples count or
            'auto'

            custom_count (int): custom cube size or curve samples count

            inverse (bool): inverse LUT

            prelutfile : path to a prelut

            postlutfile : path to a prelut

        Returns:
            str.

        """
        # copy uploaded files on the server to use it with plot_that_lut
        backup_filename = self.__copyUploadedFile(lutfile)
        backup_pre_filename = None
        backup_post_filename = None
        if prelutfile.file:
            backup_pre_filename = self.__copyUploadedFile(prelutfile)
        if postlutfile.file:
            backup_post_filename = self.__copyUploadedFile(postlutfile)
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
        return self.html((
            "{0}<br>"
            "{1}<br>"
            "<a href=javascript:history.back()>Go back</a>"
        ).format(label, result))
    upload.exposed = True

# CherryPy configuration
currdir = path.dirname(path.abspath(__file__))
server.socket_host = '127.0.0.1'
server.socket_port = 8282
conf = {'/css/style.css': {'tools.staticfile.on': True,
                           'tools.staticfile.filename': path.join(currdir,
                                                                  'css',
                                                                  'style.css')
                           },
        '/img':           {'tools.staticdir.on': True,
                           'tools.staticdir.dir': path.join(currdir, 'img')
                           },
        '/uploads':       {'tools.staticdir.on': True,
                           'tools.staticdir.dir': path.join(currdir, 'uploads'
                                                            )
                           },
        '/favicon.ico': {'tools.staticfile.on': True,
                         'tools.staticfile.filename':
                         path.join(currdir, 'icons', 'favicon.ico')
                         }
        }

sys.path.append(currdir)

if __name__ == '__main__':
    plot_that_lut.web_mode = True
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    quickstart(PlotThatLutWeb(), config=conf)
else:
    # This branch is for the test suite; you can ignore it.
    tree.mount(PlotThatLutWeb(), config=conf)
