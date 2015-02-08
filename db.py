import os
import sys
import MySQLdb
import random

dbHost = os.getenv("OPENSHIFT_MYSQL_DB_HOST")
dbUser = os.getenv("OPENSHIFT_MYSQL_DB_USERNAME")
dbPass = os.getenv("OPENSHIFT_MYSQL_DB_PASSWORD")
dbName = os.getenv("OPENSHIFT_APP_NAME")
conn = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)