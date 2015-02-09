#!/usr/bin/python

import os
import cgi
import cgitb
import re
import string
import random
import subprocess
import shutil
import db
import Cookie
import time

tmpDir = os.getenv('OPENSHIFT_TMP_DIR') # Deploy
# tmpDir = 'openshift_tmp_dir' # Test

def discard(sid):
	allProgress = db.get_progress(sid)
	if allProgress != None:
		db.discard(sid)

		for progress in allProgress:
			deletePath = os.path.join(tmpDir, progress[2]+progress[4])
			try:
				os.remove(deletePath)
			except OSError:
				pass

cgitb.enable()
form = cgi.FieldStorage()


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

	cmd = ['identify', tmpPath]

	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()
	identifyResult = out.split()
	try:
		fileFormat = identifyResult[1]
	except IndexError:
		fileFormat = 'NONE'
	if not ((re.search(".jpg$", fileitem.filename) and fileFormat == "JPEG") or (re.search(".png$", fileitem.filename) and fileFormat == "PNG") or (re.search(".gif$", fileitem.filename) and fileFormat == "GIF")):
		os.remove(tmpPath)
		print "Status: 301 No file selected"
		print "Location: /index.cgi?err=3" # no file selected
		print
	else:
		nowTime = time.time()
		try: 
		    cookieDict = Cookie.SimpleCookie(os.environ['HTTP_COOKIE'])
		except KeyError: 
		    cookieDict = Cookie.SimpleCookie()

		try: 
			sessionValue = cookieDict['session'].value
			discard(sessionValue)
			db.add_tmp_progress(sessionValue, nowTime, randomFileName, fn, ext)
			print "Status: 302"
			print "Location: /editor.cgi"
			print
		except KeyError: 
			sessionValue = random.randint(0, 100000)
			discard(sessionValue)
			db.add_tmp_progress(sessionValue, nowTime, randomFileName, fn, ext)
			print "Status: 302"
			print "Location: /editor.cgi?tmp_id=%s" % sessionValue
			print

