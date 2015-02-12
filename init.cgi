#!/usr/bin/python

import db
import env
import os

for fn in os.listdir(env.tmpDir):
	path = os.path.join(env.tmpDir, fn)
	try:
		os.remove(path)
	except Exception, e:
		print e

for fn in os.listdir(env.saveDir):
	path = os.path.join(env.saveDir, fn)
	try:
		os.remove(path)
	except Exception, e:
		print e

tables = db.get_all_table_name()

for table in tables:
	db.drop_table(table)

db.create_table('gallery')
db.create_table('tmp_progress')

print "Status: 301"
print "Location: /init-done.html"
print