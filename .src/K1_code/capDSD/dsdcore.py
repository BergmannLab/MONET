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
import operator

def build_transition_matrix(adjacency_graph):
    n = np.size(adjacency_graph[0])
    
    transition = np.zeros((n,n))
    
    for i in range(n):
        s = np.sum(adjacency_graph[i])
        if s:
            transition[i] = np.divide(adjacency_graph[i], s)
        else:
            transition[i][i] = 1
    return transition

"""
#I am an idiot
def walk_from(transition, start, iters):
    expected = np.zeros(np.size(transition[0]))
    expected[start] = 1.0
    for i in range(iters):
        expected = np.dot(expected,transition)
    return expected

def calc_hescotts(transition, iters,v=True,n=None):
    if n is None:
        n = np.size(transition[0])
    m = np.size(transition[0])
    hescotts = np.empty((n,m))
    for i in xrange(0,n):
        if v: print "Calculating hescotts for "+str(i)+"..."
        hescotts[i] = walk_from(transition, i, iters)
    return hescotts
"""

def calc_hescotts(transition, iters, v=True, n=None):
    if n is None:
        n = np.size(transition[0])
    m = np.size(transition[0])
    hescotts = np.zeros((n,m))
    for i in range(n): hescotts[i,i] = 1
    for i in range(iters):
        if v: print "Calculating hescotts for step "+str(i+1)+"..."
        hescotts = np.dot(hescotts, transition)
        for i in range(n): hescotts[i,i]+=1
    return hescotts                                

def calc_dsd(hescotts):
    n = np.size(hescotts[:,0])
    dsd = np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            d = np.linalg.norm((hescotts[i,:]-hescotts[j,:]), ord=1)
            dsd[i][j] = d
            dsd[j][i] = d
    return dsd

def add_self_edges(adjacency_graph, base_weight=1):    
    n = np.size(adjacency_graph[0])
    ident = np.identity(n)*base_weight
    return np.add(adjacency_graph,ident)

    
