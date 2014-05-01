# prepend to system path
import sys
PROJECT_DIR = '/mitranscriptome/www/mitranscriptome'
sys.path.insert(0, PROJECT_DIR)

print >>sys.stderr, 'TEST TEST TEST'

from web import app as application