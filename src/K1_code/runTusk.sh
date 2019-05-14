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
#
# Script to run Team Tusk clustering method for user input network,
# which should be located at data/input_network.txt
###############################################################################

echo K1: Running Team Tusk\'s code from the 2017 DREAM challenge on disease module identification

cd /K1_code/

# get number of clusters to use, default to 100
NUM_CLUSTERS=${1:-100}

rm -rf ./data/DSD
rm -rf ./data/cluster_results
rm -rf ./data/final_clusters
mkdir -p ./data/DSD
mkdir -p ./data/cluster_results
mkdir -p ./data/final_clusters

# run DSD and write distance matrix/nodelist to data/DSD
echo "- run DSD and write distance matrix/nodelist"
python ./dsd_gen.py ./data/input_network.txt -o ./data/DSD/network

# get correct location of distance matrix/nodelist
if [ -f ./data/DSD/network.dsd ]; then
    DSD_FILE=./data/DSD/network.dsd
    NODELIST_FILE=./data/DSD/network.nodelist
else
    DSD_FILE=./data/DSD/network_0.dsd
    NODELIST_FILE=./data/DSD/network_0.nodelist
fi

# run clustering on distance matrix, then split large clusters recursively
echo "- run clustering on distance matrix"
python ./clustering/generate_clusters.py $DSD_FILE -n $NODELIST_FILE -a 1 -p $NUM_CLUSTERS > ./data/cluster_results/network_clusters.txt
echo "- split large clusters recursively"
python ./clustering/split_clusters.py $DSD_FILE ./data/cluster_results/network_clusters.txt -n $NODELIST_FILE > ./data/cluster_results/network_clusters_split.txt

# copy to final clustering file
cp ./data/cluster_results/network_clusters_split.txt ./data/final_clusters/clusters.txt
echo "- DONE"

# docker generates output files owned by root: make them read/writable
chmod 777 -R ./data
