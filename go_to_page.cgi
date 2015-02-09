#!/usr/bin/python

import cgi
import cgitb

cgitb.enable()
form = cgi.FieldStorage()

pageToGo = form.getvalue('page', 1)
print "Content-Type: text/html"
print "Status: 301"
print "Location: /index.cgi?page=%s" % pageToGo
print