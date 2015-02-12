#!/usr/bin/python

import cgi
import cgitb
import os
import db
import time
import shutil
import subprocess
import Cookie
import env

cgitb.enable()
form = cgi.FieldStorage()

try: 
    cookieDict = Cookie.SimpleCookie(os.environ['HTTP_COOKIE'])
except KeyError: 
    cookieDict = Cookie.SimpleCookie()

try: 
    sessionValue = cookieDict['session'].value
except KeyError: 
    sessionValue = None

if sessionValue == None:
	print "Status: 301"
	print "Location: /index.cgi"
	print

progress = db.get_newest_progress(sessionValue)
if progress == None:
	print "Status: 301"
	print "Location: /index.cgi"
	print

nowTime = time.time()

action = form['action'].value

def discard(sid):
	allProgress = db.get_progress(sid)
	if allProgress != None:
		db.discard(sid)

		for progress in allProgress:
			deletePath = os.path.join(env.tmpDir, progress[2]+progress[4])
			try:
				os.remove(deletePath)
			except OSError:
				pass

def generate_thumbnail(fn, ext):
	origin_path = os.path.join(env.saveDir, fn + ext)
	thumb_path = os.path.join(env.saveDir, fn + '_thumb' + ext)
	cmd = ['convert', origin_path, '-resize', '200x200', thumb_path]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()

if action == 'Undo':
	newestProgress = db.get_newest_progress(sessionValue)
	db.undo(sessionValue, newestProgress)
	deletePath = os.path.join(env.tmpDir, newestProgress[2]+newestProgress[4])
	os.remove(deletePath)

	print "Status: 301"
	print "Location: /editor.cgi"
	print

elif action == 'Discard':
	discard(sessionValue)

	expireTimestamp = 0
	expireTime = time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expireTimestamp))
	cookieDict['session'] = sessionValue
	cookieDict['session']['expires'] = expireTime

	print "Content-Type: text/html"
	print cookieDict
	print
	print '<html><head><meta http-equiv="refresh" content="0; url=index.cgi"/></head></html>'

elif action == 'Finish':

	newestProgress = db.get_newest_progress(sessionValue)
	tmpPath = os.path.join(env.tmpDir, newestProgress[2] + newestProgress[4])
	savePath = os.path.join(env.saveDir, newestProgress[2] + newestProgress[4])
	shutil.move(tmpPath, savePath)

	generate_thumbnail(newestProgress[2], newestProgress[4])

	db.finish(newestProgress[0], nowTime, newestProgress[2], newestProgress[3], newestProgress[4])

	discard(sessionValue)

	expireTimestamp = 0
	expireTime = time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expireTimestamp))
	cookieDict['session'] = sessionValue
	cookieDict['session']['expires'] = expireTime

	print "Content-Type: text/html"
	print cookieDict
	print
	print '<html><head><meta http-equiv="refresh" content="0; url=success.cgi?fn=%s&ext=%s"/></head></html>' % (newestProgress[2], newestProgress[4])

