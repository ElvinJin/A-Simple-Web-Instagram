#!/usr/bin/python

print 'Content-type: text/html'
print

print '<html><head>'
print '''<title>Elvin\'s Web Instagram</title>
		<!-- Bootstrap core CSS -->
    	<link href="css/bootstrap.min.css" rel="stylesheet">
    	<!-- Bootstrap theme -->
    	<link href="css/bootstrap-theme.min.css" rel="stylesheet">
    	<!-- Custom theme -->
    	<link href="css/main.css" rel="stylesheet">'''
print '</head>'

print """<body><div class="container">

    <div class="header">
    	<h3 class="text-muted ">Elvin's Web Instagram</h3>
    	<button type="button" class="btn btn-info">Resume</button>
    </div>
	<form enctype="multipart/form-data" action="upload.cgi" method="POST">
		<div class="row">
			<div class="col-lg-6 col-sm-6 col-12">
		        <h4>Choose an image (.jpg .gif .png): </h4>
			    <input type="file" name="pic" accept="image/gif, image/jpeg, image/png"/>
		    </div>
		</div>
	    <button type="submit" class="btn btn-primary">Upload</button>
	</form>
</div></body>"""
print "</html>"