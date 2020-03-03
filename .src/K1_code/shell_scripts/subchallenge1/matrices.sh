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

mkdir -p data/matrices

python network_scripts/adj_matrix.py data/networks/subchallenge1/1_ppi_anonym_v2.txt -n data/nodelists/1_nodelist.txt > data/matrices/1_matrix.txt
python network_scripts/adj_matrix.py data/networks/subchallenge1/2_ppi_anonym_v2.txt -n data/nodelists/2_nodelist.txt > data/matrices/2_matrix.txt
python network_scripts/adj_matrix.py data/networks/subchallenge1/4_coexpr_anonym_v2.txt -n data/nodelists/4_nodelist.txt > data/matrices/4_matrix.txt
python network_scripts/adj_matrix.py data/networks/subchallenge1/5_cancer_anonym_v2.txt -n data/nodelists/5_nodelist.txt > data/matrices/5_matrix.txt
python network_scripts/adj_matrix.py data/networks/subchallenge1/6_homology_anonym_v2.txt -n data/nodelists/6_nodelist.txt > data/matrices/6_matrix.txt
python augment_directed.py data/networks/subchallenge1/3_signal_anonym_directed_v3.txt -o data/matrices/3_augmented

mv data/matrices/3_augmented.nodelist data/nodelists/3_aug_nodelist.txt
mv data/matrices/3_augmented.aug data/matrices/3_aug_matrix.txt
