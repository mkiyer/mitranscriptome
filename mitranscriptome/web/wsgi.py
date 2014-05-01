
# user must set these values
PYTHON_ENV = '/var/www/html/venv/bin/activate_this.py'
PACKAGES = ['/var/www/html/mitranscriptome/mitranscriptome']

###############################################

# load enthought python distribution
execfile(PYTHON_ENV, dict(__file__=PYTHON_ENV))

# prepend website python packages to python path
import sys
for pkg in PACKAGES:
    sys.path.insert(0, pkg)

from web import app as application

#def application(environ, start_response):
#    status = '200 OK'
#    output = 'Hello World!'
#
#    response_headers = [('Content-type', 'text/plain'),
#                        ('Content-Length', str(len(output)))]
#    start_response(status, response_headers)
#
#    return [output]