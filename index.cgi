#!/usr/bin/python

print 'Content-type: text/html'
print

print '<html><head>'
print '''<title>Elvin\'s Web Instagram</title>
		<!-- Bootstrap core CSS -->
    	<link href="css/bootstrap.min.css" rel="stylesheet">
    	<!-- Bootstrap theme -->
    	<link href="css/bootstrap-theme.min.css" rel="stylesheet">'''
print '</head>'

print """<body><form enctype="multipart/form-data" action="upload.cgi" method="POST">
    Choose an image (.jpg .gif .png): <br />
    <input type="file" name="pic" accept="image/gif, image/jpeg, image/png" /><br />
    <input type="submit" value="Upload" />
</form></body>"""
print "</html>"