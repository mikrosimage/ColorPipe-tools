#!/usr/bin/python

############################
#
# Plot That LUT **Web**
# Version : 0.1
# Author : mfe
#
# CherryPy Web app
# for Plot That LUT
#
############################

from os import path
import sys

from cherrypy import quickstart, tree, server
from plot_that_lut import plot_that_lut


class PlotThatLutWeb(object):
    def html(self, body):
        return """
<html>
<head>
    <title>Plot That Lut</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
        <div id="content">
            <div id='header'><h1># Plot That LUT #</h1></div>
            <div id='text'>
               {0}
            </div>
        </div>
</body>
</html>
                """.format(body)

    def form(self):
        return """
<form action="upload" method="post" enctype="multipart/form-data">
    Choose LUT file: <input type="file" name="lut_file" /><br/>
    Lut Type:
    <input type="radio" name="lut_type" value="auto" checked=true> auto
    <input type="radio" name="lut_type" value="curve"> curve
    <input type="radio" name="lut_type" value="cube"> cube
    <br>
    Samples count:
    <input type="radio" name="count" value="auto" checked=true> auto
    <input type="radio" name="count" value="custom"> custom :
    <input type="text" name="custom_count" value=17 size=5>
    <br>
    <input type="submit" />
</form>

                """

    def index(self):
        return self.html(self.form())
    index.exposed = True

    def upload(self, lut_file, lut_type, count, custom_count):
        all_data = ''
        while True:
            data = lut_file.file.read(8192)
            if not data:
                break
            all_data += data
        # copy uploaded file on the server to use it with plot_that_lut
        backup_filename = "uploads/{0}".format(lut_file.filename)
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

        label = 'Displaying : {0} (type : {1}, samples : {2}'.format(
                backup_filename, lut_type, display_count)
        # call plot_that_lut to export the graph
        try:
            result = plot_that_lut(backup_filename, lut_type, tmp_count)
        except Exception, e:
            error = str(e).replace('\n', '<br>')
            result = """
<h2>Something went wrong ! </h2>
<br>
<font color="#FF0000">{0}</font><br>
                     """.format(error)
        return self.html("""
{0}<br>
{1}<br>
<a href=javascript:history.back()>Go back</a>
                         """.format(label, result))
    upload.exposed = True

# CherryPy configuration
currdir = path.dirname(path.abspath(__file__))
server.socket_host = 'devpc17.mikros.int'
server.socket_port = 8080
conf = {'/css/style.css': {'tools.staticfile.on': True,
                           'tools.staticfile.filename': path.join(currdir,
                                                                  'css',
                                                                  'style.css')
                           },
        '/img': {'tools.staticdir.on': True,
                 'tools.staticdir.dir': path.join(currdir, 'img')},
        '/uploads': {'tools.staticdir.on': True,
                     'tools.staticdir.dir': path.join(currdir, 'uploads')}
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
