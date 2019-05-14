'''
'bpms.py' sets up the command line arguments for the 'genecentric-bpms'
program.

It can do quite a few things in parallel (like generating random bipartitions),
so this module also does some preprocessing to setup sane defaults for
parallelization.
'''
import argparse
import multiprocessing as mp

import bpm
from bpm.cmdargs import assert_read_access

try:
    __cpus = mp.cpu_count()
except NotImplementedError:
    __cpus = 1

parser = argparse.ArgumentParser(
    description='BPM generator',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
aa = parser.add_argument
aa('geneinter', type=str,
   metavar='INPUT_GENETIC_INTERACTION_FILE', help='Location of the GI file.')
aa('bpm', type=str,
   metavar='OUTPUT_BPM_FILE', help='Where the BPM output will be written.')
aa('-e', '--ignore-list', dest='ignore', type=str, default=None,
   metavar='IGNORE_FILE',
   help='The location of an ignore gene list file. (One gene per line.) '
        'Any genes in this file will be excluded from the set of genes used '
        'to generate BPMs.')
aa('-c', '--gene-ratio', dest='C', type=float, default=0.90,
   metavar='RATIO', help='Gene ratio threshold')
aa('-j', '--jaccard', dest='jaccard', type=float, default=0.66,
   metavar='JACCARD_INDEX', help='Jaccard Index threshold')
aa('-m', '--num-bipartitions', dest='M', type=int, default=250,
   metavar='NUMBER_BIPARTITIONS', help='Number of bipartitions to generate')
aa('--emap', dest='emap_defaults', action='store_true',
   help='If set, EMAP default parameters will be used. This overrides all '
        'other parameters.')
aa('--squaring', dest='squaring', action='store_true',
   help='If set, genetic interaction scores will be squared. '
        'Squaring typically speeds convergence.')
aa('--minimum-size', dest='min_size', type=int, default=3,
   metavar='MIN_SIZE', 
   help='Minimum size of BPM. Smaller BPMs are pruned. '
        'Set to 0 to disable.')
aa('--maximum-size', dest='max_size', type=int, default=25,
   metavar='MAX_SIZE', 
   help='Maximum size of BPM. Bigger BPMs are pruned. '
        'Set to 0 to disable.')
aa('-p', '--processes', dest='processes', type=int, default=__cpus,
   metavar='PROCESSES',
   help='The number of processes to run concurrently. If set to '
        '1, the multiprocessing module will not be used.')
aa('--no-jaccard', dest='pruning', action='store_false',
   help='If set, no pruning will occur. Note that --minimum-size and '
        '--maximum-size will still have an effect. Set those to 0 to '
        'disable that pruning.')
aa('--no-progress', dest='progress', action='store_false',
   help='If set, the progress bar will not be shown.')
aa('-v', '--verbose', dest='verbose', action='store_true',
   help='If set, more output will be shown.')

conf = parser.parse_args()

# BS
if conf.emap_defaults:
    conf.C = 0.9
    conf.jaccard = 0.66
    conf.M = 250
    conf.squaring = True
    conf.min_size = 3
    conf.max_size = 25
    conf.pruning = True

# Protect the user from themselves.
# If the provided number of processes is larger than the detected number of
# CPUs, forcefully lower it to the number of CPUs.
if conf.processes > __cpus:
    conf.processes = __cpus

# Do some error checking on file inputs...
assert_read_access(conf.geneinter)
if conf.ignore: # ignore list is optional
    assert_read_access(conf.ignore)

# Set the global conf variable
bpm.conf = conf

