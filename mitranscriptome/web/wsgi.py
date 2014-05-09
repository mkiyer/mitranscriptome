# prepend website python packages to python path
import sys
APP_ROOT = '/var/www/html/mitranscriptome/mitranscriptome'
sys.path.insert(0, APP_ROOT)
# load application module
from web.app import app as application


