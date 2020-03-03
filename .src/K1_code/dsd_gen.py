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

Script for running Python version of DSD on Dream networks
###############################################################################
"""

import sys
import argparse
import numpy as np
import igraph as ig
import capDSD.dsdcore as dsdc
import clustering.io_functions as io

# same number of steps as in capDSD paper
NUM_STEPS = 7

def cDSD(distance_matrix, steps=7):
    """ Calculate pairwise cDSD for the given distance matrix.

    Returns a numpy array containing distances between each pair of
    nodes in the initial distance matrix.
    """
    assert(distance_matrix.shape[0] == distance_matrix.shape[1])
    n = distance_matrix.shape[0]
    transition = np.copy(distance_matrix)
    transition = dsdc.build_transition_matrix(transition)
    hescotts = dsdc.calc_hescotts(transition, steps, n=n, v=False)
    return dsdc.calc_dsd(hescotts)

def write_result_to_file(result_matrix, output_file='', fmt_type='%.3f'):
    """ Write the result of cDSD to a file """
    filename = output_file if output_file else sys.stdout
    np.savetxt(filename, result_matrix, fmt=fmt_type)

def get_matrix_components(distance_matrix, node_list, is_directed=False):
    graph_mode = ig.ADJ_DIRECTED if is_directed else ig.ADJ_UNDIRECTED
    G = ig.Graph.Weighted_Adjacency(distance_matrix.tolist(), mode=graph_mode)
    G.vs['name'] = node_list

    # divide the graph into connected components, and return an adjacency
    # matrix for each of them
    components = G.clusters(mode='weak').subgraphs()
    matrices = []
    for cl in components:
        component_matrix = np.array(cl.get_adjacency(attribute='weight').data)
        matrices.append((component_matrix, cl.vs['name']))
    return matrices


def edgelist_to_numpy(input_file, is_directed=False):
    G = ig.Graph.Read_Ncol(input_file, directed=is_directed)
    if 'weight' not in G.es.attributes():
        G.es['weight'] = [1.0] * G.ecount()

    # divide the graph into connected components, and return an adjacency
    # matrix for each of them
    components = G.clusters(mode='weak').subgraphs()
    matrices = []
    # return a (matrix, nodelist) pair, since the order of named nodes is
    # especially important to keep track of
    for cl in components:
        component_matrix = np.array(cl.get_adjacency(attribute='weight').data)
        node_list = cl.vs['name']
        matrices.append((component_matrix, node_list))
    return matrices


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("network_file", help="Network input file, in adjacency\
                                              matrix or edgelist format")
    parser.add_argument("-d", "--directed", action="store_true",
                        help="Flag specifying if the input represents\
                              a directed graph. Defaults to false.")
    parser.add_argument("-n", "--nodelist_file", nargs="?", default="",
                        help="Flag allowing the user to provide a list of\
                              nodes, corresponding to an adjacency matrix\
                              representing the network. If no node list is\
                              provided, the input network will be interpreted\
                              in edgelist format, and a node list will be\
                              constructed automatically from the edges.")
    parser.add_argument("-o", "--output_prefix", nargs="?", default="",
                        help="Optionally specify an output prefix. Output is to\
                              stdout if no prefix name is specified.")

    opts = parser.parse_args()

    # first, construct numpy matrices for each of the components of the
    # input network
    if opts.nodelist_file:
        adj_matrix = np.loadtxt(opts.network_file)
        node_list = np.loadtxt(opts.nodelist_file, dtype='str')
        matrix_list = get_matrix_components(adj_matrix,
                                            node_list,
                                            is_directed=opts.directed)
    else:
        matrix_list = edgelist_to_numpy(opts.network_file,
                                        is_directed=opts.directed)

    # if there is a single connected component, calculate its DSD matrix and
    # write it. otherwise, calculate DSD matrices and output them for each
    # connnected component independently
    for idx, (adj_matrix, nodelist) in enumerate(matrix_list):
        dsd_matrix = cDSD(adj_matrix, steps=NUM_STEPS)
        if opts.output_prefix:
            output_filename = ("{}_{}.dsd".format(opts.output_prefix, idx)
                               if len(matrix_list) > 1
                               else "{}.dsd".format(opts.output_prefix))
            nodelist_filename = ("{}_{}.nodelist".format(opts.output_prefix, idx)
                               if len(matrix_list) > 1
                               else "{}.nodelist".format(opts.output_prefix))
        else:
            output_filename = ''
            nodelist_filename = ''
        write_result_to_file(dsd_matrix, output_filename)
        if nodelist:
            write_result_to_file(np.array(nodelist), nodelist_filename, '%s')


if __name__ == '__main__':
    main()

