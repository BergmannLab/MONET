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

Functions for network input/output
###############################################################################
"""

import sys
import numpy as np

def build_nx_graph_from_matrix(input_file, directed=False):
    """ Build a NetworkX graph from a text file in adjacency matrix format. """
    import networkx as nx

    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    matrix = np.loadtxt(input_file)
    G = nx.from_numpy_matrix(matrix)
    return G

def build_nx_graph_from_edgelist(input_file, directed=False):
    """ Build a NetworkX graph from a text file in edge list format. """
    import networkx as nx

    try:
        graph_fp = open(input_file, 'r')
    except IOError:
        sys.exit("Could not open file: {}".format(input_file))

    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    edge_list = []

    for line in graph_fp.readlines():
        split_line = map(str.strip, line.split())
        if len(split_line) > 2:
            edge_list.append((int(split_line[0]), int(split_line[1]), float(split_line[2])))
        else:
            edge_list.append((int(split_line[0]), int(split_line[1]), float(1)))

    G.add_weighted_edges_from(edge_list)
    graph_fp.close()

    return G

def build_ig_graph_from_matrix(input_file, is_directed=False, node_list=[]):
    """ Build an iGraph graph from a text file in adjacency matrix format. """
    import igraph as ig

    graph_mode = ig.ADJ_DIRECTED if is_directed else ig.ADJ_UNDIRECTED
    matrix = np.loadtxt(input_file)
    G = ig.Graph.Weighted_Adjacency(matrix.tolist(), mode=graph_mode)
    if node_list:
        G.vs['name'] = node_list
    return G

def build_ig_graph_from_edgelist(input_file, is_directed=False):
    """ Build an iGraph graph from a text file in edge list format.

    NOTE: We could just use ig.Graph.Read_Ncol here, but that doesn't
    necessarily preserve node order. This function does preserve node
    order (assuming all of the nodes have integer labels), at the cost
    of a bit more verbosity.
    """
    import igraph as ig

    try:
        graph_fp = open(input_file, 'r')
    except IOError:
        sys.exit("Could not open file: {}".format(input_file))

    G = ig.Graph(directed=is_directed)
    edge_list = []
    weights = []

    for line in graph_fp.readlines():
        split_line = map(str.strip, line.split())
        if len(split_line) > 2:
            edge_list.append((int(split_line[0]), int(split_line[1])))
            weights.append(float(split_line[2]))
        else:
            edge_list.append((int(split_line[0]), int(split_line[1])))
            weights.append(float(1))

    n = int(max(max(node1, node2) for node1, node2 in edge_list))
    G.add_vertices(n+1)
    G.add_edges(edge_list)
    G.es["weight"] = weights

    graph_fp.close()

    return G

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

def read_clusters(cluster_file):
    """ Read clusters from a file.

    Returns a list of lists, each sublist representing a cluster.
    """
    try:
        fp = open(cluster_file, 'r')
    except IOError:
        sys.exit('Could not open file: {}'.format(cluster_file))

    clusters = [line.rstrip().split()[2:] for line in fp.readlines()]
    fp.close()
    return clusters

def output_clusters(clusters, output_file):
    """ Output clusters in the format specified by the Dream challenge. """
    if output_file:
        output_fp = open(output_file, 'w')
    else:
        output_fp = None
    for idx, cluster in enumerate(clusters):
        cluster_text = '\t'.join(str(i) for i in cluster)
        line = '{}\t1.0\t{}\n'.format(idx+1, cluster_text)
        if output_file:
            output_fp.write(line)
        else:
            sys.stdout.write(line)
    if output_file:
        output_fp.close()


