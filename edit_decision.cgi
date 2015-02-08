#!/usr/bin/python

import cgi
import cgitb
import os
import db
import time
import shutil
import subprocess

cgitb.enable()
form = cgi.FieldStorage()
sessionValue = form.getvalue('sid')
nowTime = time.time()

tmpDir = os.getenv('OPENSHIFT_TMP_DIR') # Deploy
# tmpDir = 'openshift_tmp_dir' # Test

saveDir = os.getenv('OPENSHIFT_DATA_DIR') # Deploy
# saveDir = 'openshift_data_dir' # Test

action = form['action'].value

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

def generate_thumbnail(fn, ext):
	origin_path = os.path.join(saveDir, fn + ext)
	thumb_path = os.path.join(saveDir, fn + '_thumb' + ext)
	cmd = ['convert', origin_path, '-resize', '200x200', thumb_path]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()

if action == 'Undo':
	newestProgress = db.get_newest_progress(sessionValue)
	db.undo(sessionValue, newestProgress)
	deletePath = os.path.join(tmpDir, newestProgress[2]+newestProgress[4])
	os.remove(deletePath)

	print "Status: 301"
	print "Location: /editor.cgi"
	print

elif action == 'Discard':
	discard(sessionValue)

	print "Status: 301"
	print "Location: /index.cgi"
	print

elif action == 'Finish':

	newestProgress = db.get_newest_progress(sessionValue)
	tmpPath = os.path.join(tmpDir, newestProgress[2] + newestProgress[4])
	savePath = os.path.join(saveDir, newestProgress[2] + newestProgress[4])
	shutil.move(tmpPath, savePath)

	generate_thumbnail(newestProgress[2], newestProgress[4])

	db.finish(newestProgress[0], nowTime, newestProgress[2], newestProgress[3], newestProgress[4])

	discard(sessionValue)

	print "Status: 301"
	print "Location: /index.cgi"
	print

