
tmpDir = os.getenv('OPENSHIFT_TMP_DIR') # Deploy
# tmpDir = 'openshift_tmp_dir' # Test

saveDir = os.getenv('OPENSHIFT_DATA_DIR') # Deploy
# saveDir = 'data' # Test

dbHost = os.getenv("OPENSHIFT_MYSQL_DB_HOST")
dbUser = os.getenv("OPENSHIFT_MYSQL_DB_USERNAME")
dbPass = os.getenv("OPENSHIFT_MYSQL_DB_PASSWORD")
dbName = os.getenv("OPENSHIFT_APP_NAME")

# dbHost = "127.0.0.1"
# dbUser = "root"
# dbPass = "root"
# dbName = "csci4140asg1"