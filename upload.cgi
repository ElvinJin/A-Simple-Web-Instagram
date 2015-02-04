#!/usr/bin/python

import os
import cgi
import cgitb

print "Content-Type: text/html"
print

cgitb.enable()

form = cgi.FieldStorage()

print '<html><head>'
print '''<title>Elvin's Web Instagram</title>
		<!-- Bootstrap core CSS -->
    	<link href="css/bootstrap.min.css" rel="stylesheet">
    	<!-- Bootstrap theme -->
    	<link href="css/bootstrap-theme.min.css" rel="stylesheet">'''
print '</head>'
print '<body>'

saveDir = os.getenv('OPENSHIFT_DATA_DIR') # Deploy
# saveDir = 'openshift_data_dir' # Test

readDir = 'data'

if ('pic' not in form):
    print "No file uploaded. "
elif (not form['pic'].filename):
    print "No file selected. "
else:
    fileitem = form['pic']

    print "Filename: " + fileitem.filename

    (fn, ext) = os.path.splitext(os.path.basename(fileitem.filename))
    savePath = os.path.join(saveDir, fn + ext)

    open(savePath, 'wb').write(fileitem.file.read())

    print 'File uploaded. <br /><img src="%s" />'%(os.path.join(readDir, fn + ext)) # Deploy
    # print 'File uploaded. <br /><img src="%s" />'%(os.path.join(saveDir, fn + ext)) # Test

print '</body></html>'
