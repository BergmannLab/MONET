'''
Provides a function to read and parse a BPM file into a nice data structure.
'''
import csv
import os
import sys

def read(f):
    '''
    A BPM file reader function. Assumes 'f' is in the CSV file format that is
    the output from the 'mkbpms' program. (i.e., one module per line with the 
    module name in the first column followed by its genes in subsequent 
    columns.)

    The returned data structure is a list of tuples. Each tuple represents a
    BPM where the first element is a list of genes in the first module and
    the second element is a list of genes in the second module.

    i.e., [([Gene], [Gene])]
    '''
    if not os.access(f, os.R_OK):
        print >> sys.stderr, 'Cannot read %s' % f
        sys.exit(1)

    bpms = [] # a list of two-tuples

    reader = csv.reader(open(f), delimiter='\t')
    for mod1 in reader:
        mod2 = reader.next() 
        bpms.append((mod1[1:], mod2[1:]))

    return bpms

