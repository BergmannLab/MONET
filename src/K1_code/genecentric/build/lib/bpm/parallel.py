"""
'parallel.py' is a set of functions that make parallelizing functions much 
easier. Namely, a 'pmap' function that will use the single-threaded version if 
parallelization isn't available.
"""
import math
import multiprocessing as mp
import sys

from bpm import conf

# The total number of "steps" to generate a set of BPMs
steps = 10000000

# Costs of various things to make progress bar a little more accurate
costs = { 'load_genes': 50,
        }

# A shared global variable used for visual progress
counter = mp.Value('i', 0)

def pmap(*args, **kargs):
    '''
    This is a convenient wrapper function that will parallelize a map function
    if the capability exists. It degrades to a regular map function if not.
    '''
    if conf.processes > 1:
        return mp.Pool(processes=conf.processes).map(*args, **kargs)
    else:
        return map(*args, **kargs)

def print_progress(final=False):
    '''
    This is a nice little progress bar that is reasonably accurate. It isn't
    perfect but should give a rough idea of how much longer the program needs
    to run.
    '''
    if not conf.progress:
        return

    spaces = 60

    if counter.value == steps:
        progress = spaces
        blanks = 0
        pnumber = 100
    else:
        percent = float(counter.value) / float(steps)
        progress = int(math.ceil(percent * spaces))
        blanks = spaces - progress
        pnumber = math.ceil(percent * 100)

    print >> sys.stderr, \
            '\r[%s%s] %d%%' % ('#' * progress, ' ' * blanks, pnumber),

    if final:
        print >> sys.stderr
    sys.stderr.flush()

def inc_counter(incby=1):
    '''
    Each unit this counter is increased by represents a "step" in the program.
    It is then used to show a progress bar.
    '''
    counter.value += incby

def get_counter():
    '''
    Simple accessor.
    '''
    return counter.value

