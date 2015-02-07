#!/usr/bin/python

import os
import cgi
import cgitb
import re
import string
import random
import subprocess
import shutil

cgitb.enable()
form = cgi.FieldStorage()

tmpDir = os.getenv('OPENSHIFT_TMP_DIR') # Deploy
# tmpDir = 'openshift_tmp_dir' # Test

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
	randomFileName = ''.join(random.choice(string.ascii_lowercase) for i in xrange(1,10))
	tmpPath = os.path.join(tmpDir, randomFileName + ext)
	open(tmpPath, 'wb').write(fileitem.file.read())

	cmd = ['identify', tmpPath] # Deploy
	# cmd = ['/usr/local/bin/identify', tmpPath] # Test

	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()
	identifyResult = out.split()
	fileFormat = identifyResult[1]
	if not ((re.search(".jpg$", fileitem.filename) and fileFormat == "JPEG") or (re.search(".png$", fileitem.filename) and fileFormat == "PNG") or (re.search(".gif$", fileitem.filename) and fileFormat == "GIF")):
		print "Status: 301 No file selected"
		print "Location: /index.cgi?err=3" # no file selected
		print
	else:
		print "Status: 302"
		print "Location: /editor.cgi?fn=%s&original_fn=%s" % (randomFileName, fileitem.filename)
		print
