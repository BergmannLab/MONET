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

Merge networks 1, 2, and 4 into a single combined edgelist, using
the weighting criteria described in the writeup.
###############################################################################
"""

import sys
import argparse

def edge_map_from_input(input_file):
    edge_map = {}
    try:
        input_fp = open(input_file, 'r')
    except IOError:
        sys.exit("Could not open file: {}".format(input_file))

    for idx, file in enumerate(input_fp.readlines()):
        try:
            fp = open(file.rstrip(), 'r')
        except IOError:
            sys.exit("Could not open file: {}".format(file))
        for line in fp.readlines():
            l = line.rstrip().split()
            edge_tup = (l[0], l[1])
            reverse_edge = (l[1], l[0])
            cur_value = float(l[2]) # just use the given weight
            if edge_tup in edge_map:
                edge_map[edge_tup] = min(0.95, (max(edge_map[edge_tup], cur_value) + 0.05))
            elif reverse_edge in edge_map:
                edge_map[reverse_edge] = min(0.95, (max(edge_map[reverse_edge], cur_value) + 0.05))
            else:
                edge_map[edge_tup] = cur_value
        fp.close()

    input_fp.close()
    return edge_map

def output_edge_map(edge_map):
    for ns, w in edge_map.iteritems():
        print '{}\t{}\t{}'.format(ns[0], ns[1], w)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input file containing networks to\
                                            be merged")
    opts = parser.parse_args()

    edge_map = edge_map_from_input(opts.input_file)
    output_edge_map(edge_map)

if __name__ == '__main__':
    main()
