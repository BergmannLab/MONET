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

Integrate GeneCentric results into a single (incomplete) clustering
###############################################################################
"""

import sys
import os
import argparse
import io_functions as io

def generate_overlapping_clusters(gc_results_dir):
    clusters = []
    for file in os.listdir(gc_results_dir):
        filename = gc_results_dir + file
        fp = open(filename, 'r')
        while True:
            line1 = fp.readline()
            line2 = fp.readline()
            if not line1 or not line2: break
            cluster_1 = line1.split()[1:]
            cluster_2 = line2.split()[1:]
            if len(cluster_1) < 5 or len(cluster_2) < 5:
                clusters.append(cluster_1 + cluster_2)
            else:
                clusters.append(cluster_1)
                clusters.append(cluster_2)
        fp.close()
    return clusters

def filter_clusters(clusters):
    cur_clusters = sorted(clusters, key=lambda x: len(x), reverse=True)
    num_clusters = len(cur_clusters)
    output_clusters = []
    while num_clusters >= 2:
        cluster_1 = set(cur_clusters[0])
        overlap_indices = [0]
        for i in xrange(1, num_clusters):
            cluster_2 = set(cur_clusters[i])
            if (cluster_1 & cluster_2) != set():
                # if there is overlap, add its index to overlap_clusters
                overlap_indices.append(i)
        overlap_clusters = [c for i, c in enumerate(cur_clusters)
                              if i in overlap_indices]
        output_clusters.append(cluster_1)
        cur_clusters = [c for i, c in enumerate(cur_clusters)
                          if i not in overlap_indices]
        num_clusters = len(cur_clusters)
    return output_clusters

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gc_results_dir")
    opts = parser.parse_args()

    clusters = generate_overlapping_clusters(opts.gc_results_dir)
    filtered_clusters = filter_clusters(clusters)
    io.output_clusters(filtered_clusters, '')

if __name__ == '__main__':
    main()

