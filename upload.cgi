#!/usr/bin/python

import os
import cgi
import cgitb
import subprocess
import re
import string
import random
import shutil

cgitb.enable()
form = cgi.FieldStorage()
# saveDir = os.getenv('OPENSHIFT_DATA_DIR') # Deploy
saveDir = 'openshift_data_dir' # Test
readDir = 'data'
# tmpDir = os.getenv('OPENSHIFT_TMP_DIR') # Deploy
tmpDir = 'openshift_tmp_dir' # Test

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
	fileitem = form['pic']

	(fn, ext) = os.path.splitext(os.path.basename(fileitem.filename))
	tmpPath = os.path.join(tmpDir, fn + ext)
	open(tmpPath, 'wb').write(fileitem.file.read())

	# cmd = ['identify', tmpPath] # Deploy
	cmd = ['/usr/local/bin/identify', tmpPath] # Test

	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()
	identifyResult = out.split()
	fileFormat = identifyResult[1]
	if not ((re.search(".jpg$", fileitem.filename) and fileFormat == "JPEG") or (re.search(".png$", fileitem.filename) and fileFormat == "PNG") or (re.search(".gif$", fileitem.filename) and fileFormat == "GIF")):
		print "Status: 301 No file selected"
		print "Location: /index.cgi?err=3" # no file selected
		print

	randomFileName = ''.join(random.choice(string.ascii_lowercase) for i in xrange(1,10))
	savePath = os.path.join(saveDir, randomFileName + ext)
	shutil.move(tmpPath, savePath)
	print

	print '<html><head>'
	print '''<title>Upload</title>
			<!-- Bootstrap core CSS -->
	    	<link href="css/bootstrap.min.css" rel="stylesheet">
	    	<!-- Bootstrap theme -->
	    	<link href="css/bootstrap-theme.min.css" rel="stylesheet">'''
	print '</head>'
	print '<body><div class="container">'
	print '<h3>File uploaded: %s</h3>' % fileitem.filename

	# print '''<table>
	# <tr><td>cmd</td><td>%s</td></tr>
	# <tr><td>stdout</td><td>%s</td></tr>
	# <tr><td>stderr</td><td>%s</td></tr>
	# </table>''' % (cmd, identifyResult[1], err.replace('\n', '<br />'))
	print '<div class="row"><img class="col-md-12" src="%s" /></div>'%(os.path.join(saveDir, randomFileName + ext)) # Test

	print '</div></body></html>'
