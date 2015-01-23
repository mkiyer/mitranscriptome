'''
MiTranscriptome web server

@author: mkiyer
@author: yniknafs

@version: 0.1.0
'''
class Config(object):
    # number of processes to use
    processes = 4
    # logging mode
    DEBUG = False
    # location of server data
    DATA_DIR = '/var/www/html/documents'
    
class DevelopmentConfig(Config):
    DEBUG = True

class MatthewConfig(Config):
    DEBUG = True
    DATA_DIR = '/Users/mkiyer/Documents/mitranscriptome/web_data'

class YasharConfig(Config):
    DEBUG = True
    DATA_DIR = '/mctp/projects/mitranscriptome/web/documents'
