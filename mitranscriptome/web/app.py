'''
MiTranscriptome web server

@author: mkiyer
@author: yniknafs

@version: 0.0.1
'''
import sys

def application(environ, start_response):
    status = '200 OK'
    output = 'Hello World!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    print >> sys.stderr, 'sys.prefix = %s' % repr(sys.prefix)
    print >> sys.stderr, 'sys.path = %s' % repr(sys.path)

    return [output]

# from flask import Flask
# app = Flask(__name__)
# 
# @app.route('/')
# def hello_world():
#     return 'Hello World A!'
# 
# if __name__ == '__main__':
#     app.run()