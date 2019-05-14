import os
import sys

def assert_read_access(f):
    if not os.access(f, os.R_OK):
        print >> sys.stderr, 'Could not read %s.' % f
        sys.exit(1)

