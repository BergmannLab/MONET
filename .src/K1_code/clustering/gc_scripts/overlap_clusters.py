"""Copyright 2018 Bergmann's Lab UNIL <mattia.tomasoni@unil.ch> 

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

Generate "overlap clusters" from elements that are clustered the same
in a set of given clusterings
###############################################################################
"""

import sys
import argparse

def read_clusterings(filenames):
    cluster_map = {}
    num_clusterings = len(filenames)
    for cl_num, fname in enumerate(filenames):
        # filepath = cluster_dir + fname
        filepath = fname
        try: fp = open(filepath, 'r')
        except IOError:
            sys.exit('Could not open file: {}'.format(filepath))
        for l_num, l in enumerate(fp.readlines()):
            for node in l.rstrip().split()[2:]:
                if node not in cluster_map:
                    cluster_map[node] = [-1] * num_clusterings
                cluster_map[node][cl_num] = l_num
        fp.close()
    return cluster_map

def generate_coassociation_map(cluster_map, node_list):
    co_map = {}
    for node, v in cluster_map.iteritems():
        if -1 in v or '-1' in v:
            continue
        cl_key = tuple(v)
        if cl_key not in co_map:
            co_map[cl_key] = [node]
        else:
            co_map[cl_key].append(node)
    return co_map

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gc_clusters")
    parser.add_argument("original_clusters")
    opts = parser.parse_args()
    cluster_map = read_clusterings([opts.gc_clusters, opts.original_clusters])
    node_list = cluster_map.keys()
    co_map = generate_coassociation_map(cluster_map, node_list)

    for idx, (key, cluster) in enumerate(co_map.iteritems()):
        cluster_text = '\t'.join(str(i) for i in cluster)
        print '{}\t1.0\t{}'.format(idx+1, cluster_text)

if __name__ == '__main__':
    main()
