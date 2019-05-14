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
# This script evaluated performance on the experimental benchmark set up in
# "Directed, weighted and overlapping benchmark graphs for community detection
# algorithms", written by Andrea Lancichinetti and Santo Fortunato
###############################################################################


import glob
import sklearn.metrics.cluster.supervised as sc
import pandas as pd
import csv
from generate_benchnmarks import Grid
import os
    
def score_benchmark(benchmark_network, benchmark_solution, numb_nodes):
    def import_dream_dmi_output(file, numb_nodes):
        communities = [-1] * (numb_nodes + 1)
        with open(file, newline='') as f:    
            for community in list(csv.reader(f, delimiter='\t')):
                community_label = int(community.pop(0)) # extract first element as label
                community.pop(0) # discard second element: it is always 0.5
                for node in community:
                    communities[int(node)] = community_label
        communities.pop(0) # discard first element: it is always None
        imported_nodes = sum(x != -1 for x in communities)
        if(imported_nodes != numb_nodes):
            diff = str(imported_nodes - numb_nodes)
            print('WARING: ' + diff + 'nodes were not assigned to any community\n' + file)
        return communities
    def import_solution(file):
        solution = pd.read_csv(file, sep='\t', header=None)
        communities = solution.iloc[:,1].tolist()
        return communities
    to_be_tested = import_dream_dmi_output(benchmark_network, numb_nodes)
    solution = import_solution(benchmark_solution)
    return(sc.normalized_mutual_info_score(to_be_tested,solution))

def run():
    grid = Grid()
    methods = ['R1', 'M1', 'K1', 'louvain']
    # Run Evaluation ##################################################################################################
    for N in grid.N:
        for k in grid.k:
            for t1 in grid.t1:
                for beta in grid.beta:
                    score = 6.0
                    for mut in grid.mut:
                        maxk = 2*k # fixed
                        muw = 0.1 # fixed
                        minc = 10 # fixed
                        maxc = 100 # fixed
                        params = ' -N ' + str(N) + \
                        ' -k ' + str(k) + \
                        ' -mut ' + str(mut) + \
                        ' -beta ' + str(beta) + \
                        ' -t1 ' + str(t1) + \
                        ' -maxk ' + str(maxk) + \
                        ' -muw ' + str(muw) + \
                        ' -minc ' + str(minc) + \
                        ' -maxc ' + str(maxc)
                        params_label = params.replace(' ', '_').replace('-', '')
                        benchmark_output= '../output/' + params_label + '/'
                        for method in methods:
                            try:
                                benchmark_network = glob.glob(benchmark_output + '*' + method + '*result*.txt')[0]
                                benchmark_solution = '../input/' + params_label + '/solution.txt'
                                score = score_benchmark(benchmark_network, benchmark_solution, N)
                            except Exception as e:
                                score = -1
                            next_score = len(grid.scores)
                            grid.scores.loc[next_score]=[N, k, mut, beta, t1, method, score]
    
    os.system('rm -rf ../graphs/ && mkdir ../graphs/')
    grid.scores.to_csv("../graphs/grid.tsv", sep='\t')

if __name__ == '__main__':
    print("\n---------------------------EVALUATING DreamDMI BENCHMARKS-------------------------\n")
    run()
    print("\n-------------------------DONE EVALUATING DreamDMI BENCHMARKS-----------------------\n")
