import sys
import os

# user must set these values
PYTHON_ROOT = '/var/www/html/sw/epd-7.3-2-rh5-x86_64'
PYTHON_BIN = os.path.join(PYTHON_ROOT, 'bin')
PYTHON_SITE_PACKAGES = os.path.join(PYTHON_ROOT, 'lib/python2.7/site-packages')
APP_ROOT = '/var/www/html/mitranscriptome/mitranscriptome'

###############################################

old_os_path = os.environ['PATH']
os.environ['PATH'] = os.path.dirname(PYTHON_BIN) + os.pathsep + old_os_path
base = os.path.dirname(os.path.dirname(PYTHON_BIN))
prev_sys_path = list(sys.path)
import site
site.addsitedir(PYTHON_SITE_PACKAGES)
sys.real_prefix = sys.prefix
sys.prefix = base
# Move the added items to the front of the path:
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

# prepend website python packages to python path
sys.path.insert(0, APP_ROOT)

# load application module
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

