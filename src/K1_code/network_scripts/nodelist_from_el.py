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
###############################################################################
"""

import sys
import argparse

def nodelist_from_edges(input_file):
    node_list = set()
    try:
        input_fp = open(input_file, 'r')
    except IOError:
        sys.exit("Could not open file: {}".format(input_file))

    for line in input_fp.readlines():
        l = line.rstrip().split()
        node_list.add(l[0])
        node_list.add(l[1])

    input_fp.close()
    return sorted(map(int, list(node_list)))
    # return list(node_list)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input file containing network")
    opts = parser.parse_args()
    node_list = nodelist_from_edges(opts.input_file)
    for node in node_list:
        print node

if __name__ == '__main__':
    main()
