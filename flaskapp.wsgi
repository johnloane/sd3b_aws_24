#!/usr/bin/python
import sys
import logging
import os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/FlaskApp/")
os.environ['TEST'] = 'test'
def application(environ, start_response):
	for key in['TEST']:
		os.environ[key] = environ.get(key, '')
	from FlaskApp import app as _application
	_application.secret_key='secret'
	return _application(environ, start_response)
