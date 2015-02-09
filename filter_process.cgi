#!/usr/bin/python

import cgi
import cgitb
import os
import random
import string
import subprocess
import db
import time

cgitb.enable()
form = cgi.FieldStorage()

sessionValue = form.getvalue('sid')
nowTime = time.time()

progress = db.get_newest_progress(sessionValue)
if progress == None:
	print "Status: 301"
	print "Location: /index.cgi"
	print

filename = progress[2]
fn = progress[3]
ext = progress[4]
original_fn = fn+ext

tmpDir = os.getenv('OPENSHIFT_TMP_DIR') # Deploy
# tmpDir = 'openshift_tmp_dir' # Test
tmpPath1 = os.path.join(tmpDir, filename + ext)

randomFileName = ''.join(random.choice(string.ascii_lowercase) for i in xrange(1,10))
tmpPath2 = os.path.join(tmpDir, randomFileName + ext)

action = form['action'].value

def get_image_dimension(origin):
	cmd = ['identify', origin]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()
	dimension = out.split()[2].split('x')

	return (dimension[0], dimension[1])

def convert_border(origin, destination):
	cmd = ['convert', origin, '-bordercolor', 'black', '-border', '15', destination]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()

def convert_lomo(origin, destination):
	cmd = ['convert', origin, '-channel', 'R', '-level', '33%', '-channel', 'G', '-level', '33%', destination]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()

def convert_lens_flare(origin, destination):
	(width, height) = get_image_dimension(origin)

	cmd = ['convert', 'assets/lensflare.png', '-resize', width+'x', 'tmp.png']
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()

	cmd = ['composite', '-compose', 'screen', '-gravity', 'northwest', 'tmp.png', origin, destination]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()

	os.remove('tmp.png')

def convert_black_and_white(origin, destination):
	(width, height) = get_image_dimension(origin)

	cmd = ['convert', origin, '-type', 'grayscale', 'item']
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()

	cmd = ['convert', 'assets/bwgrad.png', '-resize', width+'x'+height+'!', 'tmp.png']
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()

	cmd = ['composite', '-compose', 'softlight', '-gravity', 'center', 'tmp.png', 'item', destination]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()

	os.remove('item')
	os.remove('tmp.png')

def convert_blur(origin, destination):
	(width, height) = get_image_dimension(origin)
	blur_level = min(float(width), float(height))/300.0
	cmd = ['convert', origin, '-blur', '%fx%f'%(blur_level,blur_level), destination]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, err) = p.communicate()

def add_annotate(origin, destination, position, message, font, font_size):
	if font == "Times":
		font = "Times-Roman"
	if position == 'top':
		cmd = ['convert', origin, '-background', 'black', '-fill', 'white', '-pointsize', font_size, '-font', font, 'label:%s'%message, '+swap', '-gravity', 'center', '-append', destination]
		p = subprocess.Popen(cmd)
		(out, err) = p.communicate()
	else:
		cmd = ['convert', origin, '-background', 'black', '-fill', 'white', '-font', font, '-pointsize', font_size, 'label:%s'%message, '-gravity', 'center', '-append', destination]
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(out, err) = p.communicate()

if action == 'Border':
	convert_border(tmpPath1, tmpPath2)
	db.add_tmp_progress(sessionValue, nowTime, randomFileName, fn, ext)
elif action == 'Lomo':
	convert_lomo(tmpPath1, tmpPath2)
	db.add_tmp_progress(sessionValue, nowTime, randomFileName, fn, ext)
elif action == 'Lens Flare':
	convert_lens_flare(tmpPath1, tmpPath2)
	db.add_tmp_progress(sessionValue, nowTime, randomFileName, fn, ext)
elif action == 'Black White':
	convert_black_and_white(tmpPath1, tmpPath2)
	db.add_tmp_progress(sessionValue, nowTime, randomFileName, fn, ext)
elif action == 'Blur':
	convert_blur(tmpPath1, tmpPath2)
	db.add_tmp_progress(sessionValue, nowTime, randomFileName, fn, ext)
elif action == 'Annotate Top':
	msg = form.getvalue('msg')
	if (not msg) or msg == '':
		print "Content-Type: text/html"
		print "Status: 302"
		print "Location: /editor.cgi?fn=%s&original_fn=%s&err=empty_msg" % (filename, original_fn)
		print
		return

	font = form.getvalue('font')
	if (not font) or font == "Please select":
	   font = "Times"

	font_size = form.getvalue('font-size')
	if (not font_size) or font_size == "Please select":
	   font_size = "20"

	add_annotate(tmpPath1, tmpPath2, "top", msg, font, font_size)
	db.add_tmp_progress(sessionValue, nowTime, randomFileName, fn, ext)
elif action == 'Annotate Bottom':
	msg = form.getvalue('msg')
	if (not msg) or msg == '':
		print "Content-Type: text/html"
		print "Status: 302"
		print "Location: /editor.cgi?fn=%s&original_fn=%s&err=empty_msg" % (filename, original_fn)
		print
		return

	font = form.getvalue('font')
	if (not font) or font == "Please select":
	   font = "Times"

	font_size = form.getvalue('font-size')
	if (not font_size) or font_size == "Please select":
	   font_size = "20"

	add_annotate(tmpPath1, tmpPath2, "bottom", msg, font, font_size)
	db.add_tmp_progress(sessionValue, nowTime, randomFileName, fn, ext)

print "Content-Type: text/html"
print "Status: 302"
print "Location: /editor.cgi"
print
