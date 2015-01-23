import os
import sys

# prepend website python packages to python path
APP_ROOT = '/var/www/html/mitranscriptome/mitranscriptome'
sys.path.insert(0, APP_ROOT)

def application(environ, start_response):
    # pass WSGI environment variables to os.environ
    vars = ['MITRANSCRIPTOME_CONFIG']
    for var in vars:
        os.environ[var] = environ.get(var, 'config.Config')

    # load application module
    from web.app import app as _application

    return _application(environ, start_response)
