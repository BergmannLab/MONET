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
import sys

def print_imap(target, i_map):
    print "not implemented at the moment"

def print_adjacency(target, adj):
    temp = np.array(adj != 0, dtype = int)
    np.savetxt(target,adj,delimiter="",fmt="%.1d")

def read_adjacency(target):
    f = open(target,'r')
    a = []
    for l in f.readlines():
        a.append(map(int,list(l.rstrip())))

    a = np.array(a)
        
    #for i in range(np.size(a[0])):
        #if not np.sum(a[i,:])+np.sum(a[:,i]): print str(i), np.sum(a[i,:])+np.sum(a[:,i])
        
    return a

def print_transition(target, transition):
    np.savetxt(target,transition,delimiter="\t")

def print_i_map(target, i_map):
    f = open(target, 'w')
    for (a,b),c in i_map.items():
        a,b,c = str(a), str(b), str(c)
        f.write("\t".join([a,b,c,'\n']))
    f.close()

def read_dsd(target):
    f = open(target, 'r')
    l = f.readline()
    l = l.rstrip().split('\t')[1:]
    n = len(l)
    
    names = {}
    for i in range(n):
        names[l[i]] = i
        
    scores = np.empty(n, dtype=object)
    for i in range(n):
        l = f.readline().rstrip().split('\t')[1:]
        scores[i] = np.array(l).astype('float')
    return (names, scores)
        

def print_dsd(target, scores, names):
    sorted_names = sorted(names.iteritems(), key = operator.itemgetter(1))

    n = len(sorted_names)

    f = open(target,'w')

    s = "\t"
    for i in range(n):
        s+=sorted_names[i][0]+"\t"
    f.write(s[:-1]+"\n")
    for i in range(n):
        s = sorted_names[i][0]
        for j in range(n):
            s+="\t"+str(scores[i][j])
        f.write(s+"\n")
    f.close()

def print_trimat(target, scores):
    f = open(target,'w')
    n = np.size(scores[0])
    for i in range(n):
        l = ""
        for j in range(i+1,n):
            l += "{:0.8f}".format(scores[i][j])+"\t"
        f.write(l+"\n")
    f.close()

def print_names(target, names):
    sorted_names = sorted(names.iteritems(), key = operator.itemgetter(1))

    n = len(sorted_names)

    f = open(target,'w')

    for i in range(n):
        f.write(sorted_names[i][0]+"\n")
    f.close()

def read_names(target):
    names = {}
    counter = 0
    f = open(target, 'r')
    for n in f.readlines():
        if n.rstrip not in names:
            names[n.rstrip()] = counter
            counter += 1
        else:
            pass
    return names


if __name__ == "__main__":
    print read_adjacency(sys.argv[1])
