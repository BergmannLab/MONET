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

import os
import sys

from distutils.core import setup

try:
    import argparse
except:
    print ''
    print 'Genecentric requires the "argparse" module which became ',
    print 'available in Python 2.7.'
    print 'You should be able to install it on older versions from PyPI.'
    sys.exit(1)

try:
    import json
except:
    print ''
    print 'Genecentric requires the "json" module which became ',
    print 'available in Python 2.6.'
    sys.exit(1)

setup(
    name = 'genecentric',
    author = 'Andrew Gallant',
    author_email = 'Andrew.Gallant@tufts.edu',
    version = '1.0.3',
    license = 'GPL',
    description = 'A utility to generate between-pathway modules (BPMs) and perform GO enrichment on them.',
    long_description = 'See README',
    url = 'http://bcb.cs.tufts.edu/genecentric',
    packages = ['bpm', 'bpm/cmdargs'],
    data_files = [
        ('share/genecentric/doc', ['README', 'LICENSE']),
        ('share/genecentric/data', ['data/essentials', 'data/yeast_emap.gi',
                                    'data/README']),
    ],
    scripts = ['genecentric-bpms', 'genecentric-fainfo',
               'genecentric-from-csv', 'genecentric-go']
)

