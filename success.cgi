#!/usr/bin/python

import cgi
import os
import db
import env

form = cgi.FieldStorage()

fn = form.getvalue('fn', None)
ext = form.getvalue('ext', None)

if not db.finish_successful(fn, ext):
	print "Status: 301"
	print "Location: /index.cgi"
	print

print "Content-Type: text/html"
print

print '<html><head>'
print '''<title>Edit</title>
		<!-- Bootstrap core CSS -->
    	<link href="css/bootstrap.min.css" rel="stylesheet">
    	<!-- Bootstrap theme -->
    	<link href="css/bootstrap-theme.min.css" rel="stylesheet">
    	<!-- Custom CSS -->
    	<link href="css/main.css" rel="stylesheet">'''
print '</head>'
print '<body><div class="container">'
print '<div class="row" id="success_title">'
print '<div class="col-xs-3"><h3>Upload Successfully</h3></div>'
print '''<div class="col-xs-3"><a href="/index.cgi">
			<button type="submit" class="btn btn-info" id="go-back">Go to Homepage</button>
		</a></div>'''
print '</div>'

print '<div class="row"><img class="col-xs-12" src="/data/%s%s" /></div>'% (fn,ext)
print '</div></body></html>'