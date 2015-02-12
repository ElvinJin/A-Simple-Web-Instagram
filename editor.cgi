#!/usr/bin/python

import cgi
import cgitb
import os
import shutil
import Cookie
import time
import random
import db
import env

cgitb.enable()
form = cgi.FieldStorage()

try: 
    cookieDict = Cookie.SimpleCookie(os.environ['HTTP_COOKIE'])
except KeyError: 
    cookieDict = Cookie.SimpleCookie()

try: 
    sessionValue = cookieDict['session'].value
except KeyError: 
    sessionValue = None

if sessionValue == None:
	print "Status: 301"
	print "Location: /index.cgi"
	print

progress = db.get_newest_progress(sessionValue)
if progress == None:
	print "Status: 301"
	print "Location: /index.cgi"
	print

expireTimestamp = time.time() + 30 * 24 * 60 * 60
expireTime = time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expireTimestamp))

cookieDict['session'] = sessionValue
cookieDict['session']['expires'] = expireTime

err = form.getvalue('err')
filename = progress[2]
fn = progress[3]
ext = progress[4]
original_fn = fn+ext

tmpPath = os.path.join(env.tmpDir, filename + ext)

print "Content-Type: text/html"
print cookieDict
print

print '<html><head>'
print '''<title>Edit</title>
		<!-- Bootstrap core CSS -->
    	<link href="css/bootstrap.min.css" rel="stylesheet">
    	<!-- Bootstrap theme -->
    	<link href="css/bootstrap-theme.min.css" rel="stylesheet">
    	<!-- Custom CSS -->
    	<link href="css/main.css" rel="stylesheet">'''
print '</head>'
print '<body><div class="container">'
print '<h3>File uploaded: %s</h3>' % original_fn

print '<div class="row"><img class="col-md-8" src="%s" />'% tmpPath
print '''<div class="inspector col-md-4">
		<div class="row panel panel-info">
            <div class="panel-heading">
            	<h3 class="panel-title">Filter</h3>
            </div>
            <div class="panel-body">'''
print 			'<form method="POST" action="filter_process.cgi">'
print '''			<div class="row">
				    <input class="btn btn-info filter-btn" type="submit" name="action" value="Border" />
				    <input class="btn btn-info filter-btn" type="submit" name="action" value="Lomo" />
				    <input class="btn btn-info filter-btn" type="submit" name="action" value="Lens Flare" />
				    <input class="btn btn-info filter-btn" type="submit" name="action" value="Black White" />
				    <input class="btn btn-info filter-btn" type="submit" name="action" value="Blur" />
				    </div>
			  	</form>
            </div>
        </div>
		<div class="row panel panel-info">
            <div class="panel-heading">
            	<h3 class="panel-title">Annotate</h3>
            </div>
            <div class="panel-body">'''
print 			'<form method="POST" action="filter_process.cgi">'
print '''			<div class="row">
			    		<input class="form-control panel-input-text" type="text" name="msg" placeholder="Message" />
		    		</div>'''
if err == "empty_msg":
	print 			'''<div class="alert alert-danger" role="alert">	
					  <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
					  <span class="sr-only">Error:</span>Message cannot be empty!
					</div>'''
print		    	'''<div class="row panel-selection">
			    		<label for="sel1">Font (Default "Times"):</label>
					      <select name="font" class="form-control" id="sel1">
					        <option>Please select</option>
					        <option>Times</option>
					        <option>Courier</option>
					        <option>Helvetica</option>
					      </select>
					</div>
		    		<div class="row panel-selection">
			    		<label for="sel1">Font size (Default "20px"):</label>
					      <select name="font-size" class="form-control" id="sel1">
					        <option>Please select</option>
					      	<option>10</option>
							<option>11</option>
							<option>12</option>
							<option>13</option>
							<option>14</option>
							<option>15</option>
							<option>16</option>
							<option>17</option>
							<option>18</option>
							<option>19</option>
							<option>20</option>
							<option>21</option>
							<option>22</option>
							<option>23</option>
							<option>24</option>
							<option>25</option>
							<option>26</option>
							<option>27</option>
							<option>28</option>
							<option>29</option>
							<option>30</option>
							<option>31</option>
							<option>32</option>
							<option>33</option>
							<option>34</option>
							<option>35</option>
							<option>36</option>
							<option>37</option>
							<option>38</option>
							<option>39</option>
							<option>40</option>
							<option>41</option>
							<option>42</option>
							<option>43</option>
							<option>44</option>
							<option>45</option>
							<option>46</option>
							<option>47</option>
							<option>48</option>
					      </select>
					</div>
		    		<div class="row">
					    <input class="btn btn-info filter-btn" type="submit" name="action" value="Annotate Top" />
					    <input class="btn btn-info filter-btn" type="submit" name="action" value="Annotate Bottom" />
				    </div>
			  	</form>
            </div>
        </div>
        <div class="page-header"></div>'''
        
print		'<form method="POST" action="edit_decision.cgi">'
print			'''<div class="row">
			    <input class="col-md-3 btn btn-warning dicision-btn" type="submit" name="action" value="Undo" />
			    <input class="col-md-3 btn btn-danger dicision-btn" type="submit" name="action" value="Discard" />
			    <input class="col-md-3 btn btn-success dicision-btn" type="submit" name="action" value="Finish" />
			    </div>
		  	</form>
        
	  	</div>'''
print '</div>'

print '</div></body></html>'