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

mkdir -p data/nodelists

python network_scripts/nodelist_from_el.py data/networks/subchallenge1/1_ppi_anonym_v2.txt > data/nodelists/1_nodelist.txt
python network_scripts/nodelist_from_el.py data/networks/subchallenge1/2_ppi_anonym_v2.txt > data/nodelists/2_nodelist.txt
python network_scripts/nodelist_from_el.py data/networks/subchallenge1/4_coexpr_anonym_v2.txt > data/nodelists/4_nodelist.txt
python network_scripts/nodelist_from_el.py data/networks/subchallenge1/5_cancer_anonym_v2.txt > data/nodelists/5_nodelist.txt
python network_scripts/nodelist_from_el.py data/networks/subchallenge1/6_homology_anonym_v2.txt > data/nodelists/6_nodelist.txt
