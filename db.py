import os
import sys
import MySQLdb
import random
import env

def add_tmp_progress(session_id, modified_time, new_name, original_name, extension):
	conn = MySQLdb.connect(host=env.dbHost, user=env.dbUser, passwd=env.dbPass, db=env.dbName)
	cursor = conn.cursor()

	query = 'INSERT INTO tmp_progress(session_id, modified_time, new_name, original_name, extension) VALUES (%s, %s, %s, %s, %s)'

	cursor.execute(query, [session_id, modified_time, new_name, original_name, extension])
	conn.commit()

	cursor.close()
	conn.close()

def finish(session_id, modified_time, new_name, original_name, extension):
	conn = MySQLdb.connect(host=env.dbHost, user=env.dbUser, passwd=env.dbPass, db=env.dbName)
	cursor = conn.cursor()

	query = 'INSERT INTO gallery(session_id, modified_time, new_name, original_name, extension) VALUES (%s, %s, %s, %s, %s)'

	cursor.execute(query, [session_id, modified_time, new_name, original_name, extension])
	conn.commit()

	cursor.close()
	conn.close()

def get_progress(session_id):
	conn = MySQLdb.connect(host=env.dbHost, user=env.dbUser, passwd=env.dbPass, db=env.dbName)
	cursor = conn.cursor()

	query = 'SELECT * FROM tmp_progress WHERE session_id=\'%s\'' % session_id
	cursor.execute(query)

	progress = cursor.fetchall()

	cursor.close()
	conn.close()

	if progress == None:
		return None
	if len(progress) == 0:
		return None
	sorted_progress = sorted(progress, key=lambda x:x[1], reverse=True)
	return sorted_progress

def get_newest_progress(session_id):
	progress = get_progress(session_id)
	if progress == None:
		return None
	else:
		return progress[0]

def undo(session_id, newest):
	conn = MySQLdb.connect(host=env.dbHost, user=env.dbUser, passwd=env.dbPass, db=env.dbName)
	cursor = conn.cursor()

	query = 'DELETE FROM tmp_progress WHERE new_name=\'%s\'' % newest[2]

	cursor.execute(query)
	conn.commit()

	cursor.close()
	conn.close()

def discard(session_id):
	conn = MySQLdb.connect(host=env.dbHost, user=env.dbUser, passwd=env.dbPass, db=env.dbName)
	cursor = conn.cursor()

	query = 'DELETE FROM tmp_progress WHERE session_id=\'%s\'' % session_id

	cursor.execute(query)
	conn.commit()

	cursor.close()
	conn.close()

def is_resumable(session_id):
	if session_id == None:
		return False

	progress = get_progress(session_id)
	if progress == None:
		return False
	else:
		return True

def get_number_of_photos():
	conn = MySQLdb.connect(host=env.dbHost, user=env.dbUser, passwd=env.dbPass, db=env.dbName)
	cursor = conn.cursor()

	query = 'SELECT COUNT(*) FROM gallery'

	cursor.execute(query)
	result = cursor.fetchone()
	num_of_rows = result[0]

	cursor.close()
	conn.close()
	return num_of_rows

def get_photo(page):
	conn = MySQLdb.connect(host=env.dbHost, user=env.dbUser, passwd=env.dbPass, db=env.dbName)
	cursor = conn.cursor()

	offset = (int(page) - 1) * 8
	query = 'SELECT * FROM gallery ORDER BY modified_time DESC LIMIT 8 OFFSET %s' % offset
	cursor.execute(query)

	photos = cursor.fetchall()

	cursor.close()
	conn.close()

	return photos

def finish_successful(fn, ext):
	if fn == None or ext == None:
		return False

	conn = MySQLdb.connect(host=env.dbHost, user=env.dbUser, passwd=env.dbPass, db=env.dbName)
	cursor = conn.cursor()

	query = 'SELECT * FROM gallery WHERE new_name=\'%s\' AND extension=\'%s\'' % (fn, ext)
	cursor.execute(query)

	imageRecord = cursor.fetchall()

	cursor.close()
	conn.close()

	if imageRecord == None:
		return False
	if len(imageRecord) == 0:
		return False
	else:
		return True

