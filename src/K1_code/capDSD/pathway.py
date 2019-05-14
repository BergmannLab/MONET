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
from dsdcore import *

def extend(array,rc):
    n = np.size(array[0])
    array = np.append(array, np.zeros((rc,n)), 0)
    array = np.append(array, np.zeros((n+rc,rc)), 1)
    return array

"""
parameters:
adjacency - an n x n array.  adjacency[i,j] != 0 indicates an edge between nodes i and j exists, 
    with weight adjacency[i][j]. adjacency[i][i] must be nonzero

pathways - an i x n x n array.  pathways[k,i,j] = 1 indicates that the edge between nodes i and j
   is part of pathway k. pathway[k][i][i] must be zero

r - P(Remain on pathway | already on pathway)

i_map - maps (original node, path) to the new index of the temporary node

"""
def merge_pathways(adjacency, pathways, i_map, r = .5, m = 1):

    n = np.size(adjacency[0])
    size = n+len(i_map.keys())
    transition = np.copy(adjacency)
    
    # copy adjacency matrix and extend for the path nodes
    transition = extend(transition, len(i_map.keys()))
    
    for key in i_map.keys():
        (original, path) = key
        pnode = i_map[key]
        # copy all path edges to point to the special path node
        for node in range(n):
            if pathways[path,node,original]: 
                transition[node,pnode] = m*adjacency[node,original]

        path_edges = np.nonzero(pathways[path,original,:])[0]

        # copy all edges from original 
        transition[pnode,:n] = adjacency[original,:n]
        
        # If an edge is in the path pnode is part of, remove the edge from pnode
        # to the original node.  We will be replacing it with and edge from
        # pnode to the other node's path node later.
        for edge in path_edges:
            transition[pnode][edge] = 0

        # set edges to the special path node to the proper weight to get the
        # desired probabilty r of taking them
        total_weight = np.sum(transition[pnode])

        # if r is 1 and there are path edges, remove all edges to original nodes
        if r == 1: #and path_edges.size:
            transition[pnode,:n] = np.zeros(n)
            total_weight = 0

        # if there aren't any edges of any type, add an edge back to the original node.  This should
        # never actually happen
        if not total_weight and not path_edges.size:
            transition[pnode][original] = 1
            continue

        if r == 1:
            for edge in path_edges:
                transition[pnode][i_map[(edge,path)]] = 1
        else:
            for edge in path_edges:
                transition[pnode][i_map[(edge,path)]] = (r*total_weight/(1-r))/np.size(path_edges) #weight path edges from the node s.t. P(staying on path) = r
    #print transition
    return transition

"""
For an usused method where we simply sum the weights for all the pathways and the original
adjacency matrix
"""
def merge_pathways_simple(adjacency, pathways, i_map, r = .5):
    print pathways
    transition = adjacency+pathways.sum(0)
    print transition
    return transition

"""
H(a,b) = sum(H(a_0, b_i),i)
"""
def merge_hescotts(hescotts, inv_map, n):
    ret = np.empty((n,n))
    for i in range(n):
        ret[i] = merge_hescott_vector(hescotts[i], inv_map, n)
    return ret

def merge_hescott_vector(hescotts, inv_map, n):
    ret = np.zeros(n)
    for i in range(np.size(hescotts)):
        if i < n: ret[i] += hescotts[i]
        else: ret[inv_map[i][0]] += hescotts[i]
    return ret
