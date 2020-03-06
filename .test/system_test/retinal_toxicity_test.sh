#! /bin/sh -
# Copyright 2018 Bergmann's Lab UNIL <mattia.tomasoni@unil.ch>
#
# This file is part of MONET.
#
#    DREAM DMI Tool is free software: you can redistribute it and/or modify
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
#
# Test connected to issue https://github.com/BergmannLab/MONET/issues/15
###############################################################################

output=/tmp/retinal_toxicity_test/
rm -rf $output
mkdir $output

# R1 - CAUSALITY
monet --input=./input/retinal_toxicity_BIANA.txt --output=$output --method=R1 --container=docker

# M1 - ALEPH
monet --input=./input/retinal_toxicity_BIANA.txt --output=$output --method=M1 --container=docker

# K1 - TUSK
monet --input=./input/retinal_toxicity_BIANA.txt --nclusters=10 --output=$output --method=K1 --container=docker
