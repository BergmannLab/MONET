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

Script for converting a text file in edge list format to a text file
in adjacency matrix format.
###############################################################################
"""

import sys
import argparse
import networkx as nx
import numpy as np

def get_node_list(node_file):
    node_list = []
    try:
        fp = open(node_file, 'r')
    except IOError:
        sys.exit('Could not open file: {}'.format(node_file))

    # read the first (i.e. largest) connected component
    cur_line = fp.readline()
    while cur_line and not cur_line.isspace():
        if cur_line and not cur_line.startswith('Component'):
            node_list.append(cur_line.rstrip())
        cur_line = fp.readline()

    fp.close()
    return node_list

def build_graph_from_file(edge_file, directed=False):
    """ Build a graph from a text file in edge file format. """

    try:
        graph_fp = open(edge_file, 'r')
    except IOError:
        sys.exit("Could not open file: {}".format(edge_file))

    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    edge_list = []

    for line in graph_fp.readlines():
        split_line = map(str.strip, line.split())
        if len(split_line) > 2:
            edge_list.append((split_line[0], split_line[1], float(split_line[2])))
        else:
            edge_list.append((split_line[0], split_line[1], float(1)))

    G.add_weighted_edges_from(edge_list)
    graph_fp.close()

    return G

def write_result_to_file(result_matrix, output_file=''):
    """ Write an adjacency matrix to a file. """
    filename = output_file if output_file else sys.stdout
    np.savetxt(filename, result_matrix, fmt='%.3f')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("edge_list", help="Original graph input file, in edge\
                                           list format")
    parser.add_argument("-d", "--directed", action="store_true",
                        help="Flag specifying if the input edge list represents\
                              a directed graph. Defaults to false.")
    parser.add_argument("-n", "--node_list", nargs="?",
                        help="Optionally specify a list of the nodes in\
                              the DSD file. Default is all the nodes in the\
                              graph.")
    parser.add_argument("-o", "--output_file", nargs="?", default="",
                        help="Optionally specify an output file. Output is to\
                              stdout if no file is specified.")
    opts = parser.parse_args()

    if opts.directed:
        G = build_graph_from_file(opts.edge_list, True)
    else:
        G = build_graph_from_file(opts.edge_list)

    node_list = (get_node_list(opts.node_list) if opts.node_list
                                               else range(nx.number_of_nodes(G)))
    write_result_to_file(nx.to_numpy_matrix(G, nodelist=node_list), opts.output_file)


if __name__ == '__main__':
    main()

