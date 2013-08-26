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
from plotThatLut import plotThatLut

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
                                """ + body + """
                            </div>
                        </div>
                </body>
                </html>
                """
    def form(self):
        return """
                    <form action="upload" method="post" enctype="multipart/form-data">
                        Choose LUT file: <input type="file" name="lutFile" /><br/>
                        Lut Type: <input type="radio" name="lutType" value="auto" checked=true> auto
                        <input type="radio" name="lutType" value="curve"> curve
                        <input type="radio" name="lutType" value="cube"> cube
                        <br>
                        Samples count: <input type="radio" name="count" value="auto" checked=true> auto
                        <input type="radio" name="count" value="custom"> custom : <input type="text" name="customCount" value=17 size=5>
                        <br>
                        <input type="submit" />
                    </form>

                """
    def index(self):
        return self.html(self.form())
    index.exposed = True

    def upload(self, lutFile, lutType, count, customCount):
        allData=''
        while True:
            data = lutFile.file.read(8192)
            if not data:
                break
            allData+=data
        # copy uploaded file on the server to use it with plotThatLUT
        backup_filename = "uploads/"+lutFile.filename
        savedFile=open(backup_filename, 'wb')
        savedFile.write(allData)
        savedFile.close()
        # init args
        label = 'Displaying : ' + backup_filename + " (type : " + lutType + ", samples : "
        if count == 'custom':
            tmpCount = int(customCount)
            label += str(tmpCount)
        else:
            tmpCount = None
            label += count
        label +=  ")"
        # call plotThatLut to export the graph
        try:
            result = plotThatLut(backup_filename, lutType, tmpCount)
        except Exception, e:
            error = str(e).replace('\n', '<br>')
            result = """<h2>Something went wrong ! </h2><br><font color="#FF0000">%s</font><br>"""%error
        return self.html(label + "<br>" + result + """<br><a href=javascript:history.back()>Go back</a>""")
    upload.exposed = True

# CherryPy configuration
currdir = path.dirname(path.abspath(__file__))
server.socket_host = 'devpc17.mikros.int'
server.socket_port = 8080
conf = {
    '/css/style.css':{'tools.staticfile.on':True,
    'tools.staticfile.filename': path.join(currdir,'css','style.css')},
    '/img':{'tools.staticdir.on':True,
    'tools.staticdir.dir': path.join(currdir,'img')},
    '/uploads':{'tools.staticdir.on':True,
    'tools.staticdir.dir': path.join(currdir,'uploads')}}

sys.path.append(currdir)

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    quickstart(PlotThatLutWeb(), config=conf)
else:
    # This branch is for the test suite; you can ignore it.
    tree.mount(PlotThatLutWeb(), config=conf)
