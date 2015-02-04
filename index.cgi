#!/usr/bin/python

print 'Content-type: text/html'
print

print "<html>"
print """<body><form enctype="multipart/form-data" action="upload.cgi" method="POST">
    Choose an image (.jpg .gif .png): <br />
    <input type="file" name="pic" accept="image/gif, image/jpeg, image/png" /><br />
    <input type="submit" value="Upload" />
</form></body>"""
print "</html>"