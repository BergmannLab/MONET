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

Generate "overlap clusters" from a standard network clustering and a
GeneCentric clustering.
###############################################################################
"""

import sys
import argparse
import io_functions as io

def get_cluster_nodes(cluster_file):
    cluster_nodes = []
    try:
        fp = open(cluster_file, 'r')
    except IOError:
        sys.exit('Could not open file: {}'.format(cluster_file))

    for line in fp.readlines():
        l = line.rstrip().split()
        for node in l[2:]:
            cluster_nodes.append(node)

    fp.close()
    return cluster_nodes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gc_file", help='GeneCentric cluster file')
    parser.add_argument("cluster_file",
                        help="File containing cluster filepaths")
    opts = parser.parse_args()

    cluster_nodes = get_cluster_nodes(opts.cluster_file)
    gc_nodes = get_cluster_nodes(opts.gc_file)
    gc_clusters = io.read_clusters(opts.gc_file)
    difference_nodes = list(set(cluster_nodes) - set(gc_nodes))
    gc_clusters.append(difference_nodes)
    io.output_clusters(gc_clusters, '')


if __name__ == '__main__':
    main()
