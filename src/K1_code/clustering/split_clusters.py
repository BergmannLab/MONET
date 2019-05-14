#!/usr/bin/env python
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

Script for splitting large clusters in a clustering into smaller clusters,
by progressively running spectral clustering with 2 cluster centers (i.e.
finding an approximate min cut)
###############################################################################
"""

import sys
import argparse
import io_functions as io
import clustering_algs_ig as cl
import numpy as np

MAX_CL_SIZE = 100
MAX_STEP = 10

def names_to_ids(G, cluster):
    # map from vertex name to vertex ID in G
    return [v.index for v in G.vs if v["name"] in cluster]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dsd_file", help="Distance (i.e. DSD) matrix for network")
    parser.add_argument("cluster_file", help="Clustering results file")
    parser.add_argument("-n", "--node_list", nargs="?",
                        help="Optionally specify a list of the nodes in\
                              the DSD file. Default is all the nodes in the\
                              graph.")
    opts = parser.parse_args()

    node_list = io.get_node_list(opts.node_list)
    clusters = io.read_clusters(opts.cluster_file)
    G = io.build_ig_graph_from_matrix(opts.dsd_file, False, node_list)

    clusters_to_process, final_clusters = [], []
    for cluster in clusters:
        if len(cluster) > MAX_CL_SIZE:
            clusters_to_process.append(cluster)
        else:
            final_clusters.append(cluster)

    # if all nodes have been clustered, stop looping, otherwise continue to
    # recurse on each large cluster
    step = 1
    while clusters_to_process:
        processing = clusters_to_process
        clusters_to_process = []

        for cluster in processing:
            id_cluster = names_to_ids(G, cluster)
            SG = G.subgraph(cluster)

            cluster_size = len(cluster)
            num_clusters = (int(cluster_size / float(100)) if cluster_size > 200
                                                           else 2)
            mat = SG.get_adjacency(attribute='weight')
            dist_matrix = np.array(mat.data)
            del mat
            clusters = cl.spectral_clustering(dist_matrix, num_clusters)
            del dist_matrix
            for cluster in clusters:
                if len(cluster) > MAX_CL_SIZE:
                    clusters_to_process.append([SG.vs[i]['name'] for i in cluster])
                else:
                    final_clusters.append([SG.vs[i]['name'] for i in cluster])
        step += 1

    io.output_clusters(final_clusters, '')

if __name__ == '__main__':
    main()

