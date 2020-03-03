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

Quick script to augment directed graph with low-weight edges, so
cDSD can be run (without the graph being disconnected).
###############################################################################
"""

import sys
import argparse
import numpy as np
import capDSD.PPIparser as ppip

def augment_directed(filename):
    """ Augment a directed graph, by adding low-weight backedges.

    Backedges are added to prevent graph from becoming disconnected, but the
    weight is set to be insignificant (1/100th of minimum edge weight in
    original graph).
    """
    (d, dnames) = ppip.parsePPI(filename, directed=True, conf=True)
    size = len(dnames)
    md = np.ma.masked_equal(d, 0.0, copy=False)
    min_weight = md.min() / 100.0
    augmented = np.zeros((size, size))
    dedges = np.nonzero(d)
    for edge in range(len(dedges[1])):
        i_d, j_d = dedges[0][edge], dedges[1][edge]
        if d[i_d][j_d] and d[j_d][i_d]:
            # If edge is bidirectional, add both directions as normal
            augmented[i_d][j_d] = d[i_d][j_d]
            augmented[j_d][i_d] = d[j_d][i_d]
        elif d[i_d][j_d]:
            # If edge is unidirectional, add a low-weight edge in the
            # reverse direction
            augmented[i_d][j_d] = d[i_d][j_d]
            augmented[j_d][i_d] = min_weight
        else: pass # If edge doesn't exist, do nothing

    return (augmented, dnames)


def write_result_to_file(result_matrix, output_file='', format_str='%.3f'):
    """ Write the augmented result matrix to a file """
    filename = output_file if output_file else sys.stdout
    np.savetxt(filename, result_matrix, fmt=format_str)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("network_file", help="Network input file, in edge\
                                              list format")
    parser.add_argument("-o", "--output_prefix", nargs="?", default="",
                        help="Optionally specify an output prefix. Output is to\
                              stdout if no file is specified.")
    opts = parser.parse_args()
    (augmented_matrix, node_list) = augment_directed(opts.network_file)
    matrix_file = ("{}.aug".format(opts.output_prefix) if opts.output_prefix
                                                       else '')
    node_file = ("{}.nodelist".format(opts.output_prefix) if opts.output_prefix
                                                          else '')
    sorted_nodes = zip(*sorted([(k, v) for k, v in node_list.iteritems()],
                          key=lambda x: x[1]))[0]
    write_result_to_file(augmented_matrix, matrix_file)
    write_result_to_file(np.array(sorted_nodes), node_file, '%s')


if __name__ == '__main__':
    main()
