#!/bin/bash
# Copyright 2018 Bergmann's Lab UNIL <mattia.tomasoni@unil.ch>
#
# This file is part of MONET.
#
#    MONET is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MONET is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MONET. If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################
# Mattia Tomasoni - UNIL, CBG
# 2017 DREAM challenge on Disease Module Identification
# https://www.synapse.org/modulechallenge
###############################################################################

echo M1: Running Team Aleph\'s code from the DREAM challenge on disease module identification

# load parameters from file
. /M1_code/runAleph_parameters.txt

# run method
cd /M1_code/sub-challenge1
python3 ./aleph_urv_method.py  "$linksdir"  "$avgk"  "$smallest"  "$largest"

# docker generates output files owned by root: make them read/writable
chmod 777 -R /M1_code/sub-challenge1/*

