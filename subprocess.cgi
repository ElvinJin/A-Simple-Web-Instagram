#!/usr/bin/python

import cgi
import cgitb
import os
import subprocess

print 'Content-Type: text/html'
print

cgitb.enable()

print '<html><body>'

cmd = ['ls', '-al']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out, err) = p.communicate()

print '''<table>
<tr><td>cmd</td><td>%s</td></tr>
<tr><td>stdout</td><td>%s</td></tr>
<tr><td>stderr</td><td>%s</td></tr>
</table>''' % (cmd, out.replace('\n', '<br />'), err.replace('\n', '<br />'))


cmd = ['/usr/local/bin/identify', './openshift_data_dir/photo1.jpg']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out, err) = p.communicate()

print '''<table>
<tr><td>cmd</td><td>%s</td></tr>
<tr><td>stdout</td><td>%s</td></tr>
<tr><td>stderr</td><td>%s</td></tr>
</table>''' % (cmd, out.replace('\n', '<br />'), err.replace('\n', '<br />'))

print '</body></html>'
