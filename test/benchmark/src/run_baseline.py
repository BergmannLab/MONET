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
# This script generates a series of benchmark graphs using an implementation of
# the algorithm described in the paper "Directed, weighted and overlapping
# benchmark graphs for community detection algorithms", written by Andrea
# Lancichinetti and Santo Fortunato (pre-compiled in weighted_directed_nets)
###############################################################################

import argparse
import igraph

def run(input_dir, output_dir):
    # read input network
    input_network = open(input_dir + "network.txt",'r')
    network = igraph.read(input_network, format="ncol", directed=False, names=True)
    #run louvain baseline
    louvain_communities = network.community_multilevel()
    #write output
    output_file = output_dir + "baseline_louvain__result-modules__network.txt"
    open(output_file, 'w').close()
    with open(output_file, 'a') as f:
        # for each communinty
        for community_label in range(0,louvain_communities._len):
            f.write(str(community_label) + '\t0.5')
            c = louvain_communities.subgraph(community_label)
            # write all the nodes in the current community
            for node in c.vs:
                f.write('\t' + node['name'])
            f.write('\n')


if __name__ == '__main__':
    print("\n-----------------------------RUNNINNG BASELINE: Louvain---------------------------\n")
    parser = argparse.ArgumentParser()
    parser.add_argument('--benchmark_home', required=True)
    parser.add_argument('--experiment_dir', required=True)
    args = parser.parse_args()
    input_dir=args.benchmark_home + '/input/' + args.experiment_dir
    output_dir=args.benchmark_home + '/output/' + args.experiment_dir
    print("experiment: " + args.experiment_dir)
    run(input_dir, output_dir)
    print("\n--------------------------DONE RUNNINNG BASELINE: Louvain-------------------------\n")

