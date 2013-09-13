#!/usr/bin/python

"""A cherrypy **Web** app for plot_that_lut.

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""

from os import path
import sys

from cherrypy import quickstart, tree, server
from plot_that_lut import plot_that_lut


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
            '    <input type="checkbox" name="inverse" value="1">Inverse'
            "(1D / 2D LUT only)<br>"
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

    def upload(self, lutfile, lut_type, count, custom_count, inverse=False):
        """Upload page

        Args:
            lutfile (str): path to a color transformation file (lut, matrix...)

            lut_type (str): possible values are 'curve' or 'cube'

            count: possible values are curve size or curve samples count or
            'auto'

            custom_count (int): custom cube size or curve samples count

        Returns:
            str.

        """

        all_data = ''
        while True:
            data = lutfile.file.read(8192)
            if not data:
                break
            all_data += data
        # copy uploaded file on the server to use it with plot_that_lut
        backup_filename = "uploads/{0}".format(lutfile.filename)
        saved_file = open(backup_filename, 'wb')
        saved_file.write(all_data)
        saved_file.close()
        # init args
        if count == 'custom':
            tmp_count = int(custom_count)
            display_count = str(tmp_count)
        else:
            tmp_count = None
            display_count = count
        label = 'Displaying : {0} (type : {1}, samples : {2})'.format(
                backup_filename, lut_type, display_count)
        # call plot_that_lut to export the graph
        try:
            result = plot_that_lut(backup_filename, lut_type, tmp_count,
                                   inverse)
        except Exception, e:
            error = str(e).replace('\n', '<br>')
            result = (
                "<h2>Something went wrong ! </h2>"
                "<br>"
                '<font color="#FF0000">{0}</font><br>'
            ).format(error)
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
                           }
        }

sys.path.append(currdir)

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    quickstart(PlotThatLutWeb(), config=conf)
else:
    # This branch is for the test suite; you can ignore it.
    tree.mount(PlotThatLutWeb(), config=conf)
