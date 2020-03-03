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

import pandas as pd
import os
    
class Grid(object):
    N = [300, 500, 1000, 2000, 3000, 5000, 7000, 8000, 10000, 15000]
    k =[15, 20, 25]
    mut = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    beta = [1, 2]
    t1 = [2, 3]
    scores = pd.DataFrame(columns=['N', 'k', 'mut', 'beta', 't1', 'METHOD', 'SCORE'])
    resources = pd.DataFrame(columns=['method', 'time', 'max_RAM', 'mean_RAM'])

    
def run():
    for N in Grid.N:
        for k in Grid.k:
            for mut in Grid.mut:
                for beta in Grid.beta:
                    for t1 in Grid.t1:
                        # Generate Benchmark ##########################################################################
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
                        generate_benchmark_command = './weighted_directed_nets/benchmark' + params
                        os.system(generate_benchmark_command)
                        benchmark_input = '../input/' + params_label + '/'
                        os.system('rm -rf ' + benchmark_input + ' && mkdir ' + benchmark_input)
                        benchmark_output= '../output/' + params_label + '/'
                        os.system('rm -rf ' + benchmark_output + ' && mkdir ' + benchmark_output)
                        network = benchmark_input + 'network.txt'
                        move_benchmark_network = 'mv ./network.dat ' + network
                        solution = benchmark_input + 'solution.txt'
                        move_benchmark_solution = 'mv ./community.dat ' + solution
                        stats = benchmark_input + 'statistics.txt'
                        move_benchmark_stats = 'mv ./statistics.dat ' + stats
                        os.system(move_benchmark_network)
                        os.system(move_benchmark_solution)
                        os.system(move_benchmark_stats)
                        # Generate monet run files ################################################################
                        method = 'R1'
                        run_monet_R1 = 'monet' + \
                        ' --input=./network.txt' + \
                        ' --output=../' + benchmark_output + \
                        ' --method=' + method + ' --container=docker --b=1.7 --c=400 --i=2 ' + \
                        ' --filter=quantile --threshold=1 --post=discard' + \
                        ' --smallest=' + str(minc) + ' --largest=' + str(maxc) + ' --b2=1.7 --c2=500 --i2=2'
                        generate_R1_script =  benchmark_input + '/run_monet_R1.sh'
                        os.system('echo ' + run_monet_R1 + '> ' + generate_R1_script)
                        method = 'M1'
                        run_monet_M1 = 'monet' + \
                        ' --input=./network.txt' + \
                        ' --output=../' + benchmark_output + \
                        ' --method=' + method + ' --container=docker'
                        generate_M1_script =  benchmark_input + '/run_monet_M1.sh'
                        os.system('echo ' + run_monet_M1 + '> ' + generate_M1_script)
                        method = 'K1'
                        run_monet_K1 = 'monet' + \
                        ' --input=./network.txt' + \
                        ' --output=../' + benchmark_output + \
                        ' --method=' + method + ' --container=docker'
                        generate_K1_script =  benchmark_input + '/run_monet_K1.sh'
                        os.system('echo ' + run_monet_K1 + '> ' + generate_K1_script)
    

if __name__ == '__main__':
    print("\n---------------------------GENERATING DreamDMI BENCHMARKS-------------------------\n")
    run()
    print("\n-------------------------DONE GENERATING DreamDMI BENCHMARKS-----------------------\n")
