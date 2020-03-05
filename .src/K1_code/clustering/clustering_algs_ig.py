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

Implementations of some graph clustering algorithms
###############################################################################
"""

import igraph as ig
import numpy as np
import sklearn.cluster as sc

def threshold_clustering(G, threshold, node_map=[], objects=False):
    """ Calculate threshold clusters for the given similarity scores.

    Args:
        G (ig.Graph)      - the input network
        threshold (float) - the weight above which to remove edges

    Returns:
        clusters (list) - a list of lists of nodes, each sublist represents
                          a cluster
    """
    edges = []
    for edge in G.es:
        edges.append((edge.tuple[0], edge.tuple[1], edge['weight']))
    edges_to_remove = [(n1, n2) for n1, n2, w in edges if w > threshold]
    G.delete_edges(edges_to_remove)

    # hopefully the graph is disconnected now, so filter nodes into bins
    if objects: return G.clusters().subgraphs()
    else:
        clusters = [c for c in G.clusters()]
        if node_map:
            return [[node_map[n] for n in cl] for cl in clusters]
        else: return clusters


def spectral_clustering(dist_matrix, n_clusters=8, node_map=[]):
    """ Cluster the given similarity matrix using spectral clustering.

    Assumes the given similarity network is connected.

    Args:
        G (ig.Graph)     - the input network
        n_clusters (int) - number of clusters to look for

    Returns:
        clusters (list) - a list of lists of nodes, each sublist represents
                          a cluster
    """

    if n_clusters >= dist_matrix.shape[0]:
        raise ValueError('Please re-run setting --ncluster < number of nodes in the input file')

    # apply RBF kernel to generate similarity matrix from distance
    # matrix (i.e. lower DSD => higher similarity)
    sim_matrix = np.exp(-(dist_matrix) / (2 *(dist_matrix.std()) ** 2))
    del dist_matrix

    # now do the clustering, scikit-learn implements this
    # return a list of lists representing the clusters
    node_assignments = list(sc.spectral_clustering(sim_matrix, n_clusters,
                                                   random_state=1))
    clusters = []
    for n in xrange(n_clusters):
        clusters.append([i for i, m in enumerate(node_assignments) if m == n])
    if node_map:
        return [[node_map[n] for n in cl] for cl in clusters]
    else: return clusters


def hierarchical_clustering(G, threshold=1.0):
    """ Hierarchical clustering using shortest path distances.

    For use as a baseline comparison against our DSD-based methods.
    """
    # TODO: not yet implemented using igraph
    pass

