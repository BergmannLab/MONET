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

mkdir -p data/components
mkdir -p data/gc_results
mkdir -p data/components/network_2
mkdir -p data/components/network_3
mkdir -p data/components/network_5
mkdir -p data/gc_results/network_2
mkdir -p data/gc_results/network_3
mkdir -p data/gc_results/network_5

python clustering/generate_clusters.py data/DSD/2_0.dsd -n data/DSD/2_0.nodelist -a 1 -p 10 > data/cluster_results/2_clusters_s10.txt
python clustering/generate_clusters.py data/DSD/2_0.dsd -n data/DSD/2_0.nodelist -a 1 -p 20 > data/cluster_results/2_clusters_s20.txt
python clustering/generate_clusters.py data/DSD/5_0.dsd -n data/DSD/5_0.nodelist -a 1 -p 10 > data/cluster_results/5_clusters_s10.txt
python clustering/generate_clusters.py data/DSD/5_0.dsd -n data/DSD/5_0.nodelist -a 1 -p 20 > data/cluster_results/5_clusters_s20.txt

python clustering/gc_scripts/clusters_to_sgs.py data/matrices/2_matrix.txt data/cluster_results/2_clusters_s10.txt -n data/nodelists/2_nodelist.txt -o data/components/network_2/2_s10_
python clustering/gc_scripts/clusters_to_sgs.py data/matrices/2_matrix.txt data/cluster_results/2_clusters_s20.txt -n data/nodelists/2_nodelist.txt -o data/components/network_2/2_s20_

python clustering/gc_scripts/clusters_to_sgs.py data/matrices/5_matrix.txt data/cluster_results/5_clusters_s10.txt -n data/nodelists/5_nodelist.txt -o data/components/network_5/5_s10_
python clustering/gc_scripts/clusters_to_sgs.py data/matrices/5_matrix.txt data/cluster_results/5_clusters_s20.txt -n data/nodelists/5_nodelist.txt -o data/components/network_5/5_s20_

python genecentric/genecentric-bpms data/components/network_2/2_s10_0.txt data/gc_results/network_2/2_s10_0.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s10_1.txt data/gc_results/network_2/2_s10_1.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s10_2.txt data/gc_results/network_2/2_s10_2.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s10_3.txt data/gc_results/network_2/2_s10_3.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s10_4.txt data/gc_results/network_2/2_s10_4.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s10_5.txt data/gc_results/network_2/2_s10_5.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s10_6.txt data/gc_results/network_2/2_s10_6.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s10_7.txt data/gc_results/network_2/2_s10_7.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s10_8.txt data/gc_results/network_2/2_s10_8.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s10_9.txt data/gc_results/network_2/2_s10_9.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_0.txt data/gc_results/network_2/2_s20_0.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_1.txt data/gc_results/network_2/2_s20_1.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_2.txt data/gc_results/network_2/2_s20_2.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_3.txt data/gc_results/network_2/2_s20_3.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_4.txt data/gc_results/network_2/2_s20_4.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_5.txt data/gc_results/network_2/2_s20_5.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_6.txt data/gc_results/network_2/2_s20_6.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_7.txt data/gc_results/network_2/2_s20_7.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_8.txt data/gc_results/network_2/2_s20_8.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_9.txt data/gc_results/network_2/2_s20_9.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_10.txt data/gc_results/network_2/2_s20_10.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_11.txt data/gc_results/network_2/2_s20_11.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_12.txt data/gc_results/network_2/2_s20_12.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_13.txt data/gc_results/network_2/2_s20_13.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_14.txt data/gc_results/network_2/2_s20_14.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_15.txt data/gc_results/network_2/2_s20_15.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_16.txt data/gc_results/network_2/2_s20_16.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_17.txt data/gc_results/network_2/2_s20_17.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_18.txt data/gc_results/network_2/2_s20_18.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_2/2_s20_19.txt data/gc_results/network_2/2_s20_19.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring

python genecentric/genecentric-bpms data/networks/subchallenge1/3_signal_anonym_directed_v3.txt data/gc_results/network_3/3_all.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring

python genecentric/genecentric-bpms data/components/network_5/5_s10_0.txt data/gc_results/network_5/5_s10_0.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s10_1.txt data/gc_results/network_5/5_s10_1.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s10_2.txt data/gc_results/network_5/5_s10_2.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s10_3.txt data/gc_results/network_5/5_s10_3.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s10_4.txt data/gc_results/network_5/5_s10_4.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s10_5.txt data/gc_results/network_5/5_s10_5.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s10_6.txt data/gc_results/network_5/5_s10_6.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s10_7.txt data/gc_results/network_5/5_s10_7.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s10_8.txt data/gc_results/network_5/5_s10_8.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s10_9.txt data/gc_results/network_5/5_s10_9.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_0.txt data/gc_results/network_5/5_s20_0.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_1.txt data/gc_results/network_5/5_s20_1.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_2.txt data/gc_results/network_5/5_s20_2.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_3.txt data/gc_results/network_5/5_s20_3.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_4.txt data/gc_results/network_5/5_s20_4.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_5.txt data/gc_results/network_5/5_s20_5.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_6.txt data/gc_results/network_5/5_s20_6.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_7.txt data/gc_results/network_5/5_s20_7.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_8.txt data/gc_results/network_5/5_s20_8.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_9.txt data/gc_results/network_5/5_s20_9.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_10.txt data/gc_results/network_5/5_s20_10.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_11.txt data/gc_results/network_5/5_s20_11.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_12.txt data/gc_results/network_5/5_s20_12.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_13.txt data/gc_results/network_5/5_s20_13.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_14.txt data/gc_results/network_5/5_s20_14.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_15.txt data/gc_results/network_5/5_s20_15.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_16.txt data/gc_results/network_5/5_s20_16.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_17.txt data/gc_results/network_5/5_s20_17.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_18.txt data/gc_results/network_5/5_s20_18.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring
python genecentric/genecentric-bpms data/components/network_5/5_s20_19.txt data/gc_results/network_5/5_s20_19.bpm -p 4 --minimum-size 3 --maximum-size 100 --squaring

python clustering/gc_scripts/integrate_gc.py data/gc_results/network_2/ > data/gc_results/2_gc_clusters.txt
python clustering/gc_scripts/integrate_gc.py data/gc_results/network_3/ > data/gc_results/3_gc_clusters.txt
python clustering/gc_scripts/integrate_gc.py data/gc_results/network_5/ > data/gc_results/5_gc_clusters.txt
