# prepend to system path
#import sys

#CANOPY_DIR = '/mitranscriptome/sw/canopy'
#PROJECT_DIR = '/mitranscriptome/www/mitranscriptome'

#sys.path.insert(0, PROJECT_DIR)

#print >>sys.stderr, 'TEST TEST TEST'

#from web import app as application

def application(environ, start_response):
    status = '200 OK'
    output = 'Hello World!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]