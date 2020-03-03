import sys
import time

from bpm import conf

init = time.time()

def echotime(msg):
    print msg, time.time() - init, 'seconds'

def echo(msg, newline='\n'):
    if conf.verbose:
        print '%s%s' % (msg, newline),
        sys.stdout.flush()

def progress(msg):
    echo('\r%s' % msg, newline='')

