#!/usr/bin/python

import cgi
import os
import Cookie
import time
import random
import db

form = cgi.FieldStorage()

saveDir = os.getenv('OPENSHIFT_DATA_DIR') # Deploy
# saveDir = 'data' # Test

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

num_of_rows = db.get_number_of_photos()
num_of_pages = (num_of_rows + 7) / 8
if num_of_pages == 0:
	num_of_pages = 1

try:
	current_page = int(form.getvalue('page', 1))
except ValueError:
	current_page = 1
	
if current_page < 1 or current_page > num_of_pages:
	print "Content-Type: text/html"
	print "Status: 301"
	print "Location: /index.cgi"
	print

print 'Content-type: text/html'
print cookieDict
print

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

print '''<div class="row">
    	<h3 class="text-muted col-xs-4" id="web-name">Elvin's Web Instagram</h3>'''
print '<div class="col-xs-2">'
if db.is_resumable(sessionValue):
	print '''<form action="editor.cgi" method="POST">
			<button type="submit" class="btn btn-info" id="resume">Resume</button>
			</form>'''
else:
	print '<button type="button" class="btn btn-info" id="resume" disabled>Resume</button>'
print '</div></div>'

photos = db.get_photo(current_page)

print '<div class="gallery row">'
if len(photos) == 0:
	print '<div class="row text-center" id="no-photo-sign"><h1>No photo in the gallery yet</h1></div>'
else:
	for photo in photos:
		alt_txt = photo[3] + photo[4]
		ext = photo[4]
		filename = photo[2]
		imagePath = os.path.join('data', filename + ext)
		thumbPath = os.path.join('data', filename + '_thumb' + ext)
		print '<div class="col-xs-3 photo-space"><a href="%s" target="_blank">' % imagePath
		print '<img class="thumbnail" alt="%s" src="%s">' % (alt_txt, thumbPath)
		print '</a></div>'
print '</div>'

print '<div class="row text-center"><ul class="pagination">'
if current_page == 1:
	print '<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
else:
	pre_page = current_page - 1
	print '<li><a href="/index.cgi?page=%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' % pre_page

if num_of_pages <= 5:
	for x in xrange(1,num_of_pages+1):
		if x == current_page:
			print '<li class="active"><a href="/index.cgi?page=%s">%s <span class="sr-only">(current)</span></a></li>' % (x, x)
		else:
			print '<li><a href="/index.cgi?page=%s">%s <span class="sr-only">(current)</span></a></li>' % (x, x)
else:
	start = current_page - 2
	while start < 1:
		++start
	for x in xrange(0, 5):
		index = start+x
		if index == current_page:
			print '<li class="active"><a href="/index.cgi?page=%s">%s <span class="sr-only">(current)</span></a></li>' % (index, index)
		else:
			print '<li><a href="/index.cgi?page=%s">%s <span class="sr-only">(current)</span></a></li>' % (index, index)


if current_page == num_of_pages:
	print '<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>'
else:
	next_page = current_page + 1
	print '<li><a href="/index.cgi?page=%s" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>' % next_page
		    
print '</ul></div>'
print '<div class="row text-center"><form action="go_to_page.cgi" method="POST">'
print 'Page %s of %s | Go to page <input type="number" name="page" min="1" max="%s">' % (current_page, num_of_pages, num_of_pages)
print '<button type="submit" class="btn btn-sm btn-primary">Go</button></form></div>'
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