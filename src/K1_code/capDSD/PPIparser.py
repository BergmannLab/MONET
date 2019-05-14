#!/usr/bin/python
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

import numpy as np
import collections
import re
import sys
import dsdio

def parsePPI(filename, directed = False, conf = False, fil = None, names = None):
    """
    filename - the name of input file to be parsed.  Should be tab-delimited
        with the col1 as the first interactor and col2 as the second

    directed - if false, adj[i,j] => adj[j,i]

    fil - only add an edge if both nodes meet some re.  Uses re.match, so
        checks only from the beginning.  E.g., filter = re.compile('Y') to
        allow only yeast

    returns adj, a np array with adj[i,j] indicating an edge between i and j

    returns names, an dictionary mapping node name to node index
    """

    conf_index = 0
    f = open(filename, 'r')
    l = f.readline().rstrip().split()
    for i in range(2,len(l)):
        try:
            float(l[i])
            conf_index = i
            break
        except ValueError:
            break
    
    f = open(filename, 'r')
    if names is None:
        names = {}
        n = 0
        for line in f:
            line = line.rstrip().split()
            if len(line) < 2: 
                continue
            for i in [0,1]:
                temp = True if fil is None else fil.match(line[i]) is not None
                if line[i] not in names and temp:
                    names[line[i]] = n
                    n = n + 1
        f.close()
    else:
        names = dsdio.read_names(names)
        n = len(names.keys())
    adj = np.zeros((n, n))

    #counter = 0
    f = open(filename, 'r')
    for line in f:
        line = line.rstrip().split()
        if len(line) < 2 or line[0] not in names or line[1] not in names:
            continue
 
        i, j = names[line[0]], names[line[1]]
        #if not adj[i,j]: counter += 1
        if conf and conf_index:
            adj[i,j] = float(line[conf_index])
        else:
            adj[i,j] = 1
        if not directed:
            adj[j,i] = adj[i,j]

    #print counter
    # print adj
    return (adj, names)

def printPPI(filename, adj, names, directed = False, conf = False):
    inames = {v:k for k,v in names.items()}
    f = open(filename, 'w')
    size = np.size(adj[0])
    for i in range(size):
        r = range(size) if directed else range(i,size)
        e = False
        for j in r:
            if adj[i][j]:
                l = [inames[i], inames[j]] if not conf else [inames[i], inames[j], str(adj[i][j])]
                f.write("\t".join(l)+"\n")

if __name__ == "__main__":
    (adj,names) =  parsePPI(sys.argv[1])
    print len(names.keys())
