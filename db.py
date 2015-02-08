import os
import sys
import MySQLdb
import random

dbHost = os.getenv("OPENSHIFT_MYSQL_DB_HOST")
dbUser = os.getenv("OPENSHIFT_MYSQL_DB_USERNAME")
dbPass = os.getenv("OPENSHIFT_MYSQL_DB_PASSWORD")
dbName = os.getenv("OPENSHIFT_APP_NAME")

dbHost = "127.0.0.1"
dbUser = "root"
dbPass = "root"
dbName = "csci4140asg1"

def add_tmp_progress(session_id, modified_time, new_name, original_name, extension):
	conn = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
	cursor = conn.cursor()

	query = 'INSERT INTO tmp_progress(session_id, modified_time, new_name, original_name, extension) VALUES (%s, %s, %s, %s, %s)'

	cursor.execute(query, [session_id, modified_time, new_name, original_name, extension])
	conn.commit()

	cursor.close()
	conn.close()

def finish(session_id, modified_time, new_name, original_name, extension):
	conn = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
	cursor = conn.cursor()

	query = 'INSERT INTO tmp_progress(session_id, modified_time, new_name, original_name, extension) VALUES (%s, %s, %s, %s, %s)'

	cursor.execute(query, [session_id, modified_time, new_name, original_name, extension])
	conn.commit()

	cursor.close()
	conn.close()

def get_progress(session_id):
	conn = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
	cursor = conn.cursor()

	query = 'SELECT * FROM tmp_progress WHERE session_id=\'%s\'' % session_id
	cursor.execute(query)

	progress = cursor.fetchall()

	cursor.close()
	conn.close()

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
	conn = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
	cursor = conn.cursor()

	query = 'DELETE FROM tmp_progress WHERE new_name=\'%s\'' % newest[2]

	cursor.execute(query)
	conn.commit()

	cursor.close()
	conn.close()

def discard(session_id):
	conn = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
	cursor = conn.cursor()

	query = 'DELETE FROM tmp_progress WHERE session_id=\'%s\'' % session_id

	cursor.execute(query)
	conn.commit()

	cursor.close()
	conn.close()

def is_resumable(session_id):
	progress = get_progress(session_id)
	if progress == None:
		return False
	else:
		return True
