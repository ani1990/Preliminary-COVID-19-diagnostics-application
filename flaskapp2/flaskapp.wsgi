#activate_this = '/home/ubuntu/flaskapp/venv/bin/activate_this.py'
#with open(activate_this) as f:
#	exec(f.read(), dict(__file__=activate_this))


import os
import sys


#site.addsitedir('/home/ubuntu/.local/lib/python3.6/site-packages/')
#site.addsitedir('/home/ubuntu/flaskapp2/env/lib/python3.6/site-packages')
sys.path.insert(0, '/var/www/html/flaskapp2')
from flaskapp import app as application
