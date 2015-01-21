'''
Created on Dec 22, 2014
@author yniknafs
'''

import sys
import logging
import subprocess
import os


def replacer(line, searcher, replacer):    
    return line.replace(searcher, replacer)
    
def main():
    logging.basicConfig(level=logging.DEBUG,
                      format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    GIT_FETCH = 'git fetch --all'
    GIT_RESET = 'git reset --hard origin/master'
    SERVER_RESET = 'service httpd restart'
    
    logging.debug('Fetching...')
    subprocess.call(GIT_FETCH, shell=True, cwd='/root/mitranscriptome')
    subprocess.call(GIT_RESET, shell=True, cwd='/root/mitranscriptome')
    logging.debug('Reseting server...')
    subprocess.call(SERVER_RESET, shell=True, cwd='/root/mitranscriptome')
    
      
    APP_FILE = '/root/mitranscriptome/web/app.py'
    


    
def main():
    logging.basicConfig(level=logging.DEBUG,
                      format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
      
    APP_FILE = '/root/mitranscriptome/web'
    TMP_FILE = 'server_bool_reset.tmp'    

    with open(TMP_FILE, 'w') as f:
        for line in open(APP_FILE):
            line = line.replace('\n', '')
            line = replacer(line, 'YNIKNAFS = True','YNIKNAFS = False')
            line = replacer(line, 'MKIYER = True','MKIYER = False')
            line = replacer(line, 'SERVER = False','SERVER = True')
            print >>f, line

    os.rename(TMP_FILE, APP_FILE)
    
    
    
    return 0

if __name__ == '__main__': 
    sys.exit(main())

