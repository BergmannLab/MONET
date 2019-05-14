#!/usr/sup/bin/python2.7
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

from dsdio import read_adjacency, read_names
from PPIparser import printPPI
import sys

"""
Converts the adjacency matrix + names list to the "source\ttarget\tweight\n" format
"""

if __name__ == "__main__":
    print sys.argv
    printPPI(sys.argv[1], read_adjacency(sys.argv[2]), read_names(sys.argv[3]))
