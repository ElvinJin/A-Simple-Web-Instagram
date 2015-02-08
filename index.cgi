#!/usr/bin/python

import cgi
import os
import Cookie
import time
import random
# import db

try: 
    cookieDict = Cookie.SimpleCookie(os.environ['HTTP_COOKIE'])
except KeyError: 
    cookieDict = Cookie.SimpleCookie()

try: 
    oldSession = cookieDict['session'].value
except KeyError: 
    oldSession = None

expireTimestamp = time.time() + 1 * 24 * 60 * 60
expireTime = time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expireTimestamp))

if (oldSession == None): 
    sessionValue = random.randint(0, 100000)
else:
    sessionValue = oldSession

cookieDict['session'] = sessionValue
cookieDict['session']['expires'] = expireTime

print 'Content-type: text/html'
print cookieDict
print

print 'Cookie is set! \nNew session value = %s (Expire on %s)' % (sessionValue, expireTime)
if (oldSession != None): 
    print 'Old sesion exist. Value: %s' % (oldSession)
else: 
    print 'No old session exist. '

print "expireTimestamp: " + str(expireTimestamp)
print "expireTime:      " + str(expireTime)
print '<html><head>'
print '''<title>Elvin\'s Web Instagram</title>
		<!-- Bootstrap core CSS -->
    	<link href="css/bootstrap.min.css" rel="stylesheet">
    	<!-- Bootstrap theme -->
    	<link href="css/bootstrap-theme.min.css" rel="stylesheet">
    	<!-- Custom CSS -->
    	<link href="css/main.css" rel="stylesheet">'''
print '</head>'

print '<body><div class="container">'

form = cgi.FieldStorage()
err = form.getvalue('err')
if err == '1':
	print '''<div class="alert alert-danger" role="alert">
			  <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
			  <span class="sr-only">Error:</span>
			  No file uploaded
			</div>'''
elif err == '2': 
	print '''<div class="alert alert-danger" role="alert">
			  <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
			  <span class="sr-only">Error:</span>
			  No file selected
			</div>'''
elif err == '3':
	print '''<div class="alert alert-danger" role="alert">
			  <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
			  <span class="sr-only">Error:</span>
			  File extension doesn't match your file format
			</div>'''

print '''<div class="header row">
    	<h3 class="text-muted col-md-4" id="web-name">Elvin's Web Instagram</h3>
    	<button type="button" class="btn btn-info" id="resume">Resume</button>
    	</div>'''
print '<div class="gallery row">'
for x in xrange(0,8):
	print '''<div class="col-md-3">
				<div class="thumbnail"></div>
			</div>'''
print '</div>'
print '''<form enctype="multipart/form-data" action="upload.cgi" method="POST">
		<div class="row" id="image-selection">
			<div class="col-lg-6 col-sm-6 col-12">
		        <h4>Choose an image (.jpg .gif .png): </h4>
			    <input type="file" name="pic" accept="image/gif, image/jpeg, image/png"/>
		    </div>
		</div>
	    <button type="submit" class="btn btn-primary" id="upload-btn">Upload</button>
		</form>'''
print '</div></body>'
print "</html>"