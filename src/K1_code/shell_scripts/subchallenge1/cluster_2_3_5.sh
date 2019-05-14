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

python clustering/generate_clusters.py data/DSD/2_0.dsd -n data/DSD/2_0.nodelist -a 1 -p 200 > data/cluster_results/2_clusters_s200.txt
python clustering/gc_scripts/gc_overlap.py data/gc_results/2_gc_clusters.txt data/cluster_results/2_clusters_s200.txt > data/gc_results/2_gc_overlap.txt
python clustering/gc_scripts/overlap_clusters.py data/gc_results/2_gc_overlap.txt data/cluster_results/2_clusters_s200.txt > data/cluster_results/2_gc_overlap_s200.txt
python clustering/split_clusters.py data/DSD/2_0.dsd data/cluster_results/2_gc_overlap_s200.txt -n data/DSD/2_0.nodelist > data/cluster_results/2_gc_overlap_s200_split.txt

python clustering/generate_clusters.py data/DSD/3_aug_0.dsd -n data/DSD/3_aug_0.nodelist -a 1 -p 200 > data/cluster_results/3_clusters_s200.txt
python clustering/gc_scripts/gc_and_other.py data/gc_results/3_gc_clusters.txt data/cluster_results/3_clusters_s200.txt > data/cluster_results/3_gc_10_s200.txt
python clustering/split_clusters.py data/DSD/3_aug_0.dsd data/cluster_results/3_gc_10_s200.txt -n data/DSD/3_aug_0.nodelist > data/cluster_results/3_gc_10_s200_split.txt

python clustering/generate_clusters.py data/DSD/5_0.dsd -n data/DSD/5_0.nodelist -a 1 -p 200 > data/cluster_results/5_clusters_s200.txt
python clustering/gc_scripts/gc_overlap.py data/gc_results/5_gc_clusters.txt data/cluster_results/5_clusters_s200.txt > data/gc_results/5_gc_overlap.txt
python clustering/gc_scripts/overlap_clusters.py data/gc_results/5_gc_overlap.txt data/cluster_results/5_clusters_s200.txt > data/cluster_results/5_gc_overlap_s200.txt
python clustering/split_clusters.py data/DSD/5_0.dsd data/cluster_results/5_gc_overlap_s200.txt -n data/DSD/5_0.nodelist > data/cluster_results/5_gc_overlap_s200_split.txt

mkdir -p data/final_clusters

cp data/cluster_results/2_gc_overlap_s200_split.txt data/final_clusters/sc1_2.txt
cp data/cluster_results/3_gc_10_s200_split.txt data/final_clusters/sc1_3.txt
cp data/cluster_results/5_gc_overlap_s200_split.txt data/final_clusters/sc1_5.txt
