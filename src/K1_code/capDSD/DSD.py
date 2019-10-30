#!/usr/sup/bin/python2.7
""" Copyright 2018 Bergmann's Lab UNIL <mattia.tomasoni@unil.ch>

This file is part of DREAM DMI Tool.

   DREAM DMI Tool is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   DREAM DMI Tool is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with DREAM DMI Tool. If not, see <https://www.gnu.org/licenses/>.

###############################################################################
Mattia Tomasoni - UNIL, CBG
2017 DREAM challenge on Disease Module Identification
https://www.synapse.org/modulechallenge
###############################################################################
"""

from pathway import *
from PPIparser import *
from PPIPparser import *
from dsdcore import *
from dsdio import *
from directed_augment import *

import sys
import re
import numpy as np
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read in a PPI and potentially PPIPs and run DSD")

    parser.add_argument("infile", help="PPI input file")
    parser.add_argument("outfile", help="DSD output file, will be named outfile.dsd")
    parser.add_argument("-p", "--ppip", help="directory containing PPI pathway files")
    parser.add_argument("-f", "--filter", default = "", help="filter to only allow nodes starting with the argument")
    parser.add_argument("-r", "--pathprob", default = "0.7", help="probability of remaining on a path given that you are already on it")
    parser.add_argument("-t", "--trimatrix", action='store_true', default=False, help="Output a triangular matrix file named outfile.trimatrix")
    parser.add_argument("-n", "--names", action='store_true', default=False, help="Output a names file named outfile.names")
    parser.add_argument("-a", "--adjacency", action='store_true', default=False, help ="Output an adjacency file named outfile.adjacency")
    parser.add_argument("-m", "--matrix", action='store_true', default=False, help = "Output the transition matrix in a file named outfile.matrix")
    parser.add_argument("-s", "--steps", default = "7", help="number of steps to take in the random walk")
    parser.add_argument("-d", "--directed", action='store_true', default=False, help="Treat all ppi edges as directed.  The default is to treat ppi edges as undirected, and ppip edges as directed.")
    parser.add_argument("-c", "--confidence", action='store_true', default=False, help="Use confidence values in the ppi, if any, as edge weights")
    parser.add_argument("-q", "--quitearly", action='store_true', default=False, help="Quit before after generating the transition matrix.  Useful for just generating names, adjacency, or transition matrix")
    parser.add_argument("-aug", "--augmented", default = "", help="augment undirected infile with directed ppi network")
    parser.add_argument("-i", "--namesin", default = None, help="Use a preset and preordered list of names when reading the PPI")
    parser.add_argument("-mult", "--multfactor", default = "25", help = "factor to multiply weights into a path. if 0, it is just the base PPI with pathway edges at confidence 1")
    parser.add_argument("-pathmode", "--pathmode", default="3", help = "1: consider all relations directed.  2: consider all relations undirected.  3: (default) consider activation, inhibition, phosphorilation, dephosphorilation, ubiqitination directed")

    opts = parser.parse_args()

    print "loading ppi..."
    (adj, names) = parsePPI(opts.infile, directed = opts.directed, fil = re.compile(opts.filter), conf=opts.confidence, names = opts.namesin)

    n = np.size(adj[0])

    print "read in ppi with "+str(n)+" nodes"

    i_map = {}
    if opts.ppip is not None:
        potentials = os.listdir(opts.ppip)
        ppips = []
        size = n
        
        print "initializing pathways..."

        # get a list of pathway files in target directory
        for p in potentials:
            t = p.split(".")
            if t[-1] == "ppip":
                ppips.append(os.path.join(opts.ppip,p))
        
        # for the ith pathway, augment the adjacency matrix with the edges from the pathway and
        # copy the adjacency matrix for the pathway into pathways[i]

        pathways = np.zeros((len(ppips),n,n),dtype='int8')

        for i in range(len(ppips)):
            print "parsing "+ppips[i]+"..."
            (i_map, size) = parsePPIP(ppips[i], adj, names, pathways, i, i_map, size, mode = int(opts.pathmode)) #note: adj and pathways are also modified

        print str(np.size(pathways[:,0,0]))+" pathways processed"

    if opts.adjacency:
        print_adjacency(opts.outfile+".adjacency",adj)
  
    if opts.names:
        print_names(opts.outfile+".names",names)

    transition = np.copy(adj)

    if opts.ppip is not None and not opts.multfactor == "0":
        print "integrating pathways..."
        transition = merge_pathways(transition, pathways, i_map, r = float(opts.pathprob), m = float(opts.multfactor))
        i_map_inv = {v:k for k, v in i_map.items()} 

    pathways = None
    print "building transition matrix..."

    transition = build_transition_matrix(transition)

    # note that this isn't particularly useful if pathway data is being used,
    # since the map is lost
    if opts.matrix:
        print transition
        print_transition(opts.outfile+".matrix",transition)
        if i_map:
            print i_map
            print_imap(opts.outfile+".matrix.imap",i_map) #doesn't do anything at the moment

    if opts.quitearly:
        exit()

    print "calculating hescotts..."
    hescotts = calc_hescotts(transition, int(opts.steps), n = n)
    
    if opts.ppip is not None and not opts.multfactor == "0":
        print "merging hescotts..."
        hescotts = merge_hescotts(hescotts, i_map_inv, n)

    print "calculating DSD..."
    dsd = calc_dsd(hescotts)

    print "printing to "+opts.outfile+".dsd..."
    print_dsd(opts.outfile+".dsd",dsd,names)

    if opts.trimatrix:
        print_trimat(opts.outfile+".trimatrix",dsd)
