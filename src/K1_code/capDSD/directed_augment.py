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

override_ud controls behavior when the edge exists both in the undirected graph, 
and in the directed graph as a directed edge.  If true, the edge in the new
graph will be the directed edge, otherwise it will be undirected
###############################################################################
"""

from PPIparser import parsePPI, printPPI
import numpy as np
import sys
import re
from dsdio import *

def augment_undirected(undirected_name, directed_name, conf = False, fil = None, override_ud = True):
    (ud,udnames) = parsePPI(undirected_name, directed = False, conf = True, fil = fil)
    print ud
    (d,dnames) = parsePPI(directed_name, directed = True, conf=conf,fil=fil)
    dnames_inv = {v:k for k, v in dnames.items()}
    
    augnames = udnames.copy()
    size = len(udnames)
    print size
    #code for if we were going to keep nodes not in base PPI
    #for i in dnames:
        #if i not in udnames: 
            #augnames[i] = size
            #size += 1

    # set a weight for the backedges in directed edges.  Exists to prevent graph from 
    # becoming disconnected, but is set to be insignificant (1/100th of minimum
    # edge weight in PPIs)
    mud = np.ma.masked_equal(ud,0.0,copy=False)
    md = np.ma.masked_equal(d,0.0,copy=False)
    min_weight = min([mud.min(),md.min()])/100.0

    augmented = np.zeros((size,size))
    for i in range(len(udnames)):
        augmented[i][:len(udnames)] = ud[i]

    ud, udnames = np.copy(augmented), augnames

    dedges = np.nonzero(d)
    c1 = 0
    c2 = 0
    c3 = 0
    for edge in range(len(dedges[1])):
        i_d,j_d = dedges[0][edge],dedges[1][edge]
        iname,jname = dnames_inv[i_d], dnames_inv[j_d]
        if iname not in augnames or jname not in augnames:
            continue
        i_ud,j_ud = augnames[iname], augnames[jname]
        if d[i_d][j_d] and d[j_d][i_d] and ud[i_ud][j_ud]:
            c1 += 1
            # edge is bidirectional in directed graph and exists
            # in undirected graph.  Do nothing if not
            # overriding, else set weights to directed graph
            if override_ud:
                augmented[i_ud][j_ud] = d[i_d][j_d]
                augmented[j_ud][i_ud] = d[j_d][i_d]
            else: pass
        elif ud[i_ud][j_ud]:
            c2 += 1
            # edge is directional in directed graph and exists
            # in undirected graph.  Either pass or overwrite.
            if override_ud:
                augmented[i_ud][j_ud] = d[i_d][j_d]
                augmented[j_ud][i_ud] = min_weight
            else: pass
        else: 
            c3 += 1
            # edge is not in undirected graph
            # Add the edge
            augmented[i_ud][j_ud] = d[i_d][j_d] if d[i_d][j_d] else min_weight
            augmented[j_ud][i_ud] = d[j_d][i_d] if d[j_d][i_d] else min_weight 
    """
    print udnames
    print ud
    print dnames
    print d
    print augnames
    print augmented
    """
    print c1, c2, c3

    return (augmented, augnames)

    """
    augmented = np.copy(ud)

    dcounter = 0

    print len(np.nonzero(d)[0])/2

    udedges = np.nonzero(ud)
    for i in range(len(udedges[0])):
        i,j = udedges[0][i],udedges[1][i]
        if i < j: continue
        iname, jname = udnames_inv[i], udnames_inv[j]
        if iname in dnames and jname in dnames:
            i2, j2 = dnames[iname], dnames[jname]
            if d[i2][j2] and d[j2][i2]:
                augmented[i][j] = 1
                augmented[j][i] = 1 
            elif d[i2][j2]:                 
                augmented[i][j] = 1
                dcounter += 1
                if override_ud: augmented[j][i] = 0
                else: dcounter -= 1
            elif d[j2][i2]: 
                augmented[j][i] = 1
                dcounter += 1
                if override_ud: augmented[i][j] = 0
                else: dcounter -= 1
            else: pass #no edge in directed graph, default to undirected

    print dcounter, len(udedges[0])
    return (augmented, udnames)
    """
if __name__ == "__main__":
    (graph, names) = augment_undirected(sys.argv[1], sys.argv[2], override_ud = True)
    print graph
    printPPI(sys.argv[3], graph, names, directed = True, conf = True)

