'''
Created on Dec 22, 2014
@author yniknafs
'''

import sys
import logging
import subprocess





    
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
    
    
    return 0

if __name__ == '__main__': 
    sys.exit(main())

