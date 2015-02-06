#!/usr/bin/python

import os
import cgi
import cgitb

cgitb.enable()
form = cgi.FieldStorage()
# saveDir = os.getenv('OPENSHIFT_DATA_DIR') # Deploy
saveDir = 'openshift_data_dir' # Test
readDir = 'data'

print "Content-Type: text/html"
if ('pic' not in form):
	print "Status: 301 No file uploaded"
	print "Location: /index.cgi?err=1" # no file uploaded
	print
elif (not form['pic'].filename):
	print "Status: 301 No file selected"
	print "Location: /index.cgi?err=2" # no file selected
	print
else:
	print

	print '<html><head>'
	print '''<title>Upload</title>
			<!-- Bootstrap core CSS -->
	    	<link href="css/bootstrap.min.css" rel="stylesheet">
	    	<!-- Bootstrap theme -->
	    	<link href="css/bootstrap-theme.min.css" rel="stylesheet">'''
	print '</head>'
	print '<body><div class="container">'

	fileitem = form['pic']

	(fn, ext) = os.path.splitext(os.path.basename(fileitem.filename))
	savePath = os.path.join(saveDir, fn + ext)

	open(savePath, 'wb').write(fileitem.file.read())

	# print 'File uploaded. <br /><img src="%s" />'%(os.path.join(readDir, fn + ext)) # Deploy
	print '<h3>File uploaded: %s</h3>' % fileitem.filename
	print '<div class="row"><img class="col-md-12" src="%s" /></div>'%(os.path.join(saveDir, fn + ext)) # Test

	print '</div></body></html>'
