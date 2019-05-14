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

Output clusters in a graph, similar to draw_clusters.py but outputs a
text file rather than an image
###############################################################################
"""

import sys
import argparse
import io_functions as io
import clustering_algs_ig as cl

# default to using spectral clustering
DEFAULT_ALG = 1

# options for clustering algorithm
SPECTRAL = 1
THRESHOLD = 2
HIERARCHICAL = 3

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("network_file", help="Original network input file")
    parser.add_argument("dsd_file", help="Distance (i.e. DSD) matrix for network")
    parser.add_argument("-a", "--algorithm", nargs="?", default=DEFAULT_ALG,
                        help="The clustering algorithm to use - 1 for spectral,\
                              2 for threshold clustering, and 3 for simple\
                              shortest-path divisive hierarchical clustering.\
                              Defaults to spectral clustering.")
    parser.add_argument("-d", "--directed", action="store_true",
                        help="Flag specifying if the input represents\
                              a directed graph. Defaults to false.")
    parser.add_argument("-n", "--node_list", nargs="?",
                        help="Optionally specify a list of the nodes in\
                              the DSD file. Default is all the nodes in the\
                              graph.")
    parser.add_argument("-o", "--output_file", nargs="?", default="",
                        help="Optionally specify an output file. Output is to\
                              stdout if no file is specified.")
    parser.add_argument("-p", "--parameter", nargs="?", default='',
                        help="Specify a parameter (i.e. number of clusters,\
                              distance threshold) to be used with clustering\
                              algorithm. If none is provided, a sensible\
                              default is used.")
    opts = parser.parse_args()

    G = io.build_ig_graph_from_matrix(opts.dsd_file, opts.directed)

    nodes = io.get_node_list(opts.node_list) if opts.node_list else []

    opts.algorithm = int(opts.algorithm)
    if opts.algorithm == SPECTRAL:
        import numpy as np
        k_val = int(opts.parameter) if opts.parameter else 100
        mat = G.get_adjacency(attribute='weight')
        del G
        dist_matrix = np.array(mat.data)
        del mat
        clusters = cl.spectral_clustering(dist_matrix, n_clusters=k_val,
                                          node_map=nodes)
    elif opts.algorithm == THRESHOLD:
        filter_weight = float(opts.parameter) if opts.parameter else 5.0
        clusters = cl.threshold_clustering(G, threshold=filter_weight,
                                           node_map=nodes)
    elif opts.algorithm == HIERARCHICAL:
        sys.exit('Hierarchical clustering is not implemented, please choose\
                  another algorithm')
    else:
        sys.exit('Please pick a valid clustering algorithm')

    io.output_clusters(clusters, opts.output_file)


if __name__ == '__main__':
    main()


