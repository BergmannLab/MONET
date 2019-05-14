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

mkdir -p data/cluster_results

python clustering/generate_clusters.py data/DSD/1_0.dsd -n data/DSD/1_0.nodelist -a 1 -p 1000 > data/cluster_results/1_clusters_s1000.txt
python clustering/generate_clusters.py data/DSD/4.dsd -n data/DSD/4.nodelist -a 1 -p 100 > data/cluster_results/4_clusters_s100.txt
python clustering/generate_clusters.py data/DSD/6_0.dsd -n data/DSD/6_0.nodelist -a 1 -p 100 > data/cluster_results/6_clusters_s100.txt

python clustering/split_clusters.py data/DSD/1_0.dsd data/cluster_results/1_clusters_s1000.txt -n data/DSD/1_0.nodelist > data/cluster_results/1_clusters_s1000_split.txt
python clustering/split_clusters.py data/DSD/4.dsd data/cluster_results/4_clusters_s100.txt -n data/DSD/4.nodelist > data/cluster_results/4_clusters_s100_split.txt
python clustering/split_clusters.py data/DSD/6_0.dsd data/cluster_results/6_clusters_s100.txt -n data/DSD/6_0.nodelist > data/cluster_results/6_clusters_s100_split.txt

mkdir -p data/final_clusters

cp data/cluster_results/1_clusters_s1000_split.txt data/final_clusters/sc1_1.txt
cp data/cluster_results/4_clusters_s100_split.txt data/final_clusters/sc1_4.txt
cp data/cluster_results/6_clusters_s100_split.txt data/final_clusters/sc1_6.txt
