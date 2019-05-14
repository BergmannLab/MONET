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

import sys
import xml.parsers.expat as expat
import os

types = []
global_counts = []
toaddtype = []

def readKGML(target):
    ids = {}
    links = []
    counts = []

    def start_element(name, attrs):
        global toaddtype
        
        if name == "entry":
            uid = str(attrs['id'])
            names = str(attrs['name'])
            ids[uid] = names.split(" ")
        if name == "relation":
            toaddtype = []
            try:
                e1 = str(attrs['entry1'])
                e2 = str(attrs['entry2'])
                c = -1
                for i in ids[e1]:
                    for j in ids[e2]:
                        links.append([i.split(":")[1],j.split(":")[1],""])
                        toaddtype.append(c)
                        c -= 1
            except:
                pass
        if name == "subtype":
            print attrs
            t = str(attrs['name'])
            if t not in types: types.append(t)
            counts.append(t)
            if toaddtype:
                for i in toaddtype:
                    links[i].append(str(attrs['name']))

            
    p = expat.ParserCreate()
    p.StartElementHandler = start_element
    f = open(target,'r')
    p.ParseFile(f)
    f.close()
    print target
    for type in types:
         print type + ": " + str(counts.count(type))
    global_counts.extend(counts)
    return links

def loadBasePPI(target):
    f = open(target,"r")
    ret = {}
    for l in f.readlines():
        l = l.rstrip().split("\t")
        a,b,t = l[0],l[1],l[2]
        if a not in ret.keys(): ret[a] = {b:[t]}
        elif b not in ret[a].keys(): ret[a][b] = [t]
        elif t not in ret[a][b]: #Y U Turn into none type? 
            ret[a][b] = ret[a][b]+[t]
            ret[a][b].sort()
        if b not in ret.keys(): ret[b] = {a:[t]}
        elif a not in ret[b].keys(): ret[b][a] = [t]
        elif t not in ret[b][a]: 
            ret[b][a] = ret[b][a]+[t]
            ret[a][b].sort()
    return ret

if __name__ == "__main__":

    targetDir = sys.argv[1]

    if len(sys.argv) >= 3:
        destDir = sys.argv[2]
    else:
        destDir = targetDir

    targets = os.listdir(targetDir)
    
    pathways = {}

    # get individual pathways
    for target in targets:
        t = target.split(".")
        if t[-1] == "xml":
            #print "Loading "+t[0]+"..."
            pathways[t[0]] = readKGML(os.path.join(targetDir,target))
    print "Total"
    for type in types:
        print type + ": " + str(global_counts.count(type))

    # add links to other pathways
    for p in pathways.keys():
        new = []
        for link1 in pathways[p]:
            if link1[1] in pathways.keys():
                for link2 in pathways[link1[1]]:
                    if link2[0] == p:
                        new.append([link1[0], link2[1]]+link1[2:])
                        break
        for i in new: pathways[p].append(i)
 
    #print "Loading BioGrid..."
    #biogrid = loadBasePPI("biogrid.sce.ppi")
    #print "Finished Loading BioGrid"

    for path in pathways.keys():
        #inbg, total = 0.0,0.0
        #print "Processing "+path+"..."
        n = open(os.path.join(destDir,path+".ppip"),"w")
        for link in pathways[path]:
            a,b,c = link[0],link[1],link[2]
            if a[0] == "Y" and b[0] == "Y":
                #total += 1.0
                #if a in biogrid.keys() and b in biogrid[a].keys():
                    #try:
                        #t = "".join(biogrid[a][b])
                        #inbg += 1.0
                    #except:
                        #print "Error with BioGrid at "+a+","+b+". Defaulting to 'X'"
                        #t = "X"
                #else: t = "X"
                #n.write("\t".join([a,b,t])+"\n")
                n.write("\t".join(link)+"\n")
        n.close()
        #print path+" completed. "+str(100.0*inbg/max([total,1]))+"% of links in BioGrid"
