#!/bin/bash
# Copyright 2018 Bergmann's Lab UNIL <mattia.tomasoni@unil.ch>
#
# This file is part of DREAM DMI Tool.
#
#    DREAM DMI Tool is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    DREAM DMI Tool is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with DREAM DMI Tool. If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################
# Mattia Tomasoni - UNIL, CBG
# 2017 DREAM challenge on Disease Module Identification
# https://www.synapse.org/modulechallenge
###############################################################################

echo R1: Running Team Causality\'s code from the 2017 DREAM challenge on disease module identification

# load parameters from file
. /R1_code/runCausality_parameters.txt

# run method
cd /R1_code/sub-challenge1
Rscript --vanilla ./Final.R "$filename" "$b" "$c" "$i" "$filter" "$threshold" "$interWeight" "$weighted" "$dir" "$post" "$smallest" "$largest" "$b2" "$c2" "$i2"

# docker generates output files owned by root: make them read/writable
chmod 777 -R /R1_code/sub-challenge1*
