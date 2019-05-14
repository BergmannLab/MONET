'''
'graph.py' sets up the command line arguments for the 'genecentric-bpms-graph'
program.
'''
import argparse

import bpm
from bpm.cmdargs import assert_read_access

parser = argparse.ArgumentParser(
    description='Graph BPMs',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
aa = parser.add_argument
aa('geneinter', type=str,
   metavar='INPUT_GENETIC_INTERACTION_FILE', help='Location of the GI file.')
aa('bpm', type=str,
   metavar='INPUT_BPM_FILE', help='Location of the BPM file to graph.')
aa('output_dir', type=str,
   metavar='OUTPUT_DIRECTORY', help='Where the graph files will be written.')
aa('-e', '--ignore-list', dest='ignore', type=str, default=None,
   metavar='IGNORE_FILE',
   help='The location of an ignore gene list file. (One gene per line.) '
        'Any genes in this file will be excluded from the set of genes used '
        'to generate BPMs.')
aa('--no-squaring', dest='squaring', action='store_false',
   help='If set, genetic interaction scores will not be squared. '
        'Squaring typically speeds convergence.')
aa('-v', '--verbose', dest='verbose', action='store_true',
   help='If set, more output will be shown.')

conf = parser.parse_args()

# Set the global conf variable
bpm.conf = conf

