'''
'funcassociateinfo.py' sets up the command line arguments for the 
'genecentric-fainfo' program.
'''
import sys

import bpm

import argparse

parser = argparse.ArgumentParser(
    description='Query Funcassociate for information to use with \'go-enrich\'',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
aa = parser.add_argument
aa('command', type=str, choices=['species', 'namespaces'],
   metavar='QUERY_COMMAND',
   help='The \'species\' command will ask Funcassociate for a list of '
        'available species to perform GO enrichment with. The \'namespaces\' '
        'command, with a corresponding species name, will ask Funcassociate '
        'for a list of available namespaces to use with the species '
        'specified.')
aa('species', type=str, nargs='?', default=None, metavar='QUERY_SPECIES',
   help='The species to be used when querying for available namespaces. '
        'This should not be used with the \'species\' command.')

aa('-v', '--verbose', dest='verbose', action='store_true',
   help='If set, more output will be shown.')

conf = parser.parse_args()

if conf.command == 'namespaces' and conf.species is None:
    print >> sys.stderr, \
             'You must provide a species when using the \'namespace\' command.'
    sys.exit(1)

# Set the global conf variable
bpm.conf = conf

