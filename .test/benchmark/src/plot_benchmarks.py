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


import pandas as pd
from generate_benchnmarks import Grid
import matplotlib.pyplot as plt
import os
from cProfile import label
import numpy as np
from scipy import interpolate
import statsmodels.stats.api as sms

def run():
    grid5 = Grid().scores = pd.read_csv("../graphs/__score/grid5.tsv", sep='\t')
    grid6 = Grid().scores = pd.read_csv("../graphs/__score/grid6.tsv", sep='\t')
    grid7 = Grid().scores = pd.read_csv("../graphs/__score/grid7.tsv", sep='\t')
    grid8 = Grid().scores = pd.read_csv("../graphs/__score/grid8.tsv", sep='\t')
    grid9 = Grid().scores = pd.read_csv("../graphs/__score/grid9.tsv", sep='\t')
    grid10 = Grid().scores = pd.read_csv("../graphs/__score/grid10.tsv", sep='\t')
    grid11 = Grid().scores = pd.read_csv("../graphs/__score/grid11.tsv", sep='\t')
    grid12 = Grid().scores = pd.read_csv("../graphs/__score/grid12.tsv", sep='\t')
    grid13 = Grid().scores = pd.read_csv("../graphs/__score/grid13.tsv", sep='\t')
    grid14 = Grid().scores = pd.read_csv("../graphs/__score/grid14.tsv", sep='\t')
    grid15 = Grid().scores = pd.read_csv("../graphs/__score/grid15.tsv", sep='\t')
    grid16 = Grid().scores = pd.read_csv("../graphs/__score/grid16.tsv", sep='\t')
    grid17 = Grid().scores = pd.read_csv("../graphs/__score/grid17.tsv", sep='\t')
    grid18 = Grid().scores = pd.read_csv("../graphs/__score/grid18.tsv", sep='\t')
    grid19 = Grid().scores = pd.read_csv("../graphs/__score/grid19.tsv", sep='\t')
    grid20 = Grid().scores = pd.read_csv("../graphs/__score/grid20.tsv", sep='\t')
    grid21 = Grid().scores = pd.read_csv("../graphs/__score/grid21.tsv", sep='\t')
    grid22 = Grid().scores = pd.read_csv("../graphs/__score/grid22.tsv", sep='\t')
    grid23 = Grid().scores = pd.read_csv("../graphs/__score/grid23.tsv", sep='\t')
    grid24 = Grid().scores = pd.read_csv("../graphs/__score/grid24.tsv", sep='\t')

    grid = Grid()
    grid.scores = pd.concat([
        grid5, grid6, grid7, grid8, grid9, grid10, grid11, grid12,
        grid13, grid14, grid15, grid16, grid17, grid18, grid19, grid20, grid21, grid22, grid23, grid24])

    resource_meter13 = Grid().resources = pd.read_csv("../graphs/__resource_usage/benchmark_resource_usage13.tsv", sep='\t')
    resource_meter14 = Grid().resources = pd.read_csv("../graphs/__resource_usage/benchmark_resource_usage14.tsv", sep='\t')
    resource_meter15 = Grid().resources = pd.read_csv("../graphs/__resource_usage/benchmark_resource_usage15.tsv", sep='\t')
    resource_meter16 = Grid().resources = pd.read_csv("../graphs/__resource_usage/benchmark_resource_usage16.tsv", sep='\t')
    resource_meter17 = Grid().resources = pd.read_csv("../graphs/__resource_usage/benchmark_resource_usage17.tsv", sep='\t')
    resource_meter18 = Grid().resources = pd.read_csv("../graphs/__resource_usage/benchmark_resource_usage18.tsv", sep='\t')
    resource_meter19 = Grid().resources = pd.read_csv("../graphs/__resource_usage/benchmark_resource_usage19.tsv", sep='\t')
    resource_meter20 = Grid().resources = pd.read_csv("../graphs/__resource_usage/benchmark_resource_usage20.tsv", sep='\t')
    resource_meter21 = Grid().resources = pd.read_csv("../graphs/__resource_usage/benchmark_resource_usage21.tsv", sep='\t')
    resource_meter22 = Grid().resources = pd.read_csv("../graphs/__resource_usage/benchmark_resource_usage22.tsv", sep='\t')
    resource_meter23 = Grid().resources = pd.read_csv("../graphs/__resource_usage/benchmark_resource_usage23.tsv", sep='\t')
    resource_meter24 = Grid().resources = pd.read_csv("../graphs/__resource_usage/benchmark_resource_usage24.tsv", sep='\t')


    methods = ['R1', 'M1', 'K1', 'louvain']

    ###################################################################################################################
    # SUMMARY PLOT RESOURCES time vs N  ###############################################################################
    ###################################################################################################################
    out_folder = '../graphs/'
    my_dpi = 300
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    #ax.set_xlim([0, 0.65])
    #ax.set_ylim([0.65, 1.02])
    title = 'Run-time vs network size'
    ax.set_title(title)
    ax.set_xlabel('number of nodes')
    ax.set_ylabel('seconds')
    x = [300, 500, 1000, 2000, 3000, 5000, 7000, 8000, 10000, 12000, 13000, 15000]

    #R1
    color = 'b'; label = 'R1'; marker = '>';
    method_condition = (resource_meter13['method'] == label)
    resource_meter_300 =resource_meter13[method_condition]['time']
    ci_300 = sms.DescrStatsW(resource_meter_300).tconfint_mean()
    
    resource_meter_500 = resource_meter14[method_condition]['time']
    ci_500 = sms.DescrStatsW(resource_meter_500).tconfint_mean()
    
    resource_meter_1k = resource_meter15[method_condition]['time']
    ci_1k = sms.DescrStatsW(resource_meter_1k).tconfint_mean()
    
    resource_meter_2k = resource_meter16[method_condition]['time']
    ci_2k = sms.DescrStatsW(resource_meter_2k).tconfint_mean()
    
    resource_meter_3k = resource_meter17[method_condition]['time']
    ci_3k = sms.DescrStatsW(resource_meter_3k).tconfint_mean()
    
    resource_meter_5k = resource_meter18[method_condition]['time']
    ci_5k = sms.DescrStatsW(resource_meter_5k).tconfint_mean()
    
    resource_meter_7k = resource_meter19[method_condition]['time']
    ci_7k = sms.DescrStatsW(resource_meter_7k).tconfint_mean()
    
    resource_meter_8k = resource_meter20[method_condition]['time']
    ci_8k = sms.DescrStatsW(resource_meter_8k).tconfint_mean()
    
    resource_meter_10k = resource_meter21[method_condition]['time']
    ci_10k = sms.DescrStatsW(resource_meter_10k).tconfint_mean()
    
    resource_meter_12k = resource_meter23[method_condition]['time']
    ci_12k = sms.DescrStatsW(resource_meter_12k).tconfint_mean()
    
    resource_meter_13k = resource_meter24[method_condition]['time']
    ci_13k = sms.DescrStatsW(resource_meter_13k).tconfint_mean()
    
    resource_meter_15k = resource_meter22[method_condition]['time']
    ci_15k = sms.DescrStatsW(resource_meter_15k).tconfint_mean()
    
    y = [np.mean(ci_300),np.mean(ci_500),np.mean(ci_1k),np.mean(ci_2k),np.mean(ci_3k),np.mean(ci_5k),np.mean(ci_7k),np.mean(ci_8k),np.mean(ci_10k),np.mean(ci_12k),np.mean(ci_13k),np.mean(ci_15k)]
    plt.scatter(x, y, color=color, label=label, marker=marker, alpha=0.3)


    #M1
    color = 'g'; label = 'M1'; marker = '<';
    method_condition = (resource_meter13['method'] == label)
    resource_meter_300 =resource_meter13[method_condition]['time']
    ci_300 = sms.DescrStatsW(resource_meter_300).tconfint_mean()
    
    resource_meter_500 = resource_meter14[method_condition]['time']
    ci_500 = sms.DescrStatsW(resource_meter_500).tconfint_mean()
    
    resource_meter_1k = resource_meter15[method_condition]['time']
    ci_1k = sms.DescrStatsW(resource_meter_1k).tconfint_mean()
    
    resource_meter_2k = resource_meter16[method_condition]['time']
    ci_2k = sms.DescrStatsW(resource_meter_2k).tconfint_mean()
    
    resource_meter_3k = resource_meter17[method_condition]['time']
    ci_3k = sms.DescrStatsW(resource_meter_3k).tconfint_mean()
    
    resource_meter_5k = resource_meter18[method_condition]['time']
    ci_5k = sms.DescrStatsW(resource_meter_5k).tconfint_mean()
    
    resource_meter_7k = resource_meter19[method_condition]['time']
    ci_7k = sms.DescrStatsW(resource_meter_7k).tconfint_mean()
    
    resource_meter_8k = resource_meter20[method_condition]['time']
    ci_8k = sms.DescrStatsW(resource_meter_8k).tconfint_mean()
    
    resource_meter_10k = resource_meter21[method_condition]['time']
    ci_10k = sms.DescrStatsW(resource_meter_10k).tconfint_mean()
    
    resource_meter_12k = resource_meter23[method_condition]['time']
    ci_12k = sms.DescrStatsW(resource_meter_12k).tconfint_mean()
    
    resource_meter_13k = resource_meter24[method_condition]['time']
    ci_13k = sms.DescrStatsW(resource_meter_13k).tconfint_mean()
    
    resource_meter_15k = resource_meter22[method_condition]['time']
    ci_15k = sms.DescrStatsW(resource_meter_15k).tconfint_mean()
    
    y = [np.mean(ci_300),np.mean(ci_500),np.mean(ci_1k),np.mean(ci_2k),np.mean(ci_3k),np.mean(ci_5k),np.mean(ci_7k),np.mean(ci_8k),np.mean(ci_10k),np.mean(ci_12k),np.mean(ci_13k),np.mean(ci_15k)]
    plt.scatter(x, y, color=color, label=label, marker=marker, alpha=0.3)

    #K1
    color = 'r'; label = 'K1'; marker = '^';
    method_condition = (resource_meter13['method'] == label)
    resource_meter_300 =resource_meter13[method_condition]['time']
    ci_300 = sms.DescrStatsW(resource_meter_300).tconfint_mean()
    
    resource_meter_500 = resource_meter14[method_condition]['time']
    ci_500 = sms.DescrStatsW(resource_meter_500).tconfint_mean()
    
    resource_meter_1k = resource_meter15[method_condition]['time']
    ci_1k = sms.DescrStatsW(resource_meter_1k).tconfint_mean()
    
    resource_meter_2k = resource_meter16[method_condition]['time']
    ci_2k = sms.DescrStatsW(resource_meter_2k).tconfint_mean()
    
    resource_meter_3k = resource_meter17[method_condition]['time']
    ci_3k = sms.DescrStatsW(resource_meter_3k).tconfint_mean()
    
    resource_meter_5k = resource_meter18[method_condition]['time']
    ci_5k = sms.DescrStatsW(resource_meter_5k).tconfint_mean()
    
    resource_meter_7k = resource_meter19[method_condition]['time']
    ci_7k = sms.DescrStatsW(resource_meter_7k).tconfint_mean()
    
    resource_meter_8k = resource_meter20[method_condition]['time']
    ci_8k = sms.DescrStatsW(resource_meter_8k).tconfint_mean()
    
    resource_meter_10k = resource_meter21[method_condition]['time']
    ci_10k = sms.DescrStatsW(resource_meter_10k).tconfint_mean()
    
    resource_meter_12k = resource_meter23[method_condition]['time']
    ci_12k = sms.DescrStatsW(resource_meter_12k).tconfint_mean()
    
    resource_meter_13k = resource_meter24[method_condition]['time']
    ci_13k = sms.DescrStatsW(resource_meter_13k).tconfint_mean()
    
    resource_meter_15k = resource_meter22[method_condition]['time']
    ci_15k = sms.DescrStatsW(resource_meter_15k).tconfint_mean()
    
    y = [np.mean(ci_300),np.mean(ci_500),np.mean(ci_1k),np.mean(ci_2k),np.mean(ci_3k),np.mean(ci_5k),np.mean(ci_7k),np.mean(ci_8k),np.mean(ci_10k),np.mean(ci_12k),np.mean(ci_13k),np.mean(ci_15k)]
    plt.scatter(x, y, color=color, label=label, marker=marker, alpha=0.3)

    #louvain
    color='gray'; label='louvain'; marker='o';
    method_condition = (resource_meter13['method'] == 'L')
    resource_meter_300 =resource_meter13[method_condition]['time']
    ci_300 = sms.DescrStatsW(resource_meter_300).tconfint_mean()
    resource_meter_500 = resource_meter14[method_condition]['time']
    
    ci_500 = sms.DescrStatsW(resource_meter_500).tconfint_mean()
    resource_meter_1k = resource_meter15[method_condition]['time']
    
    ci_1k = sms.DescrStatsW(resource_meter_1k).tconfint_mean()
    resource_meter_2k = resource_meter16[method_condition]['time']
    
    ci_2k = sms.DescrStatsW(resource_meter_2k).tconfint_mean()
    resource_meter_3k = resource_meter17[method_condition]['time']
    
    ci_3k = sms.DescrStatsW(resource_meter_3k).tconfint_mean()
    resource_meter_5k = resource_meter18[method_condition]['time']
    
    ci_5k = sms.DescrStatsW(resource_meter_5k).tconfint_mean()
    resource_meter_7k = resource_meter19[method_condition]['time']
    
    ci_7k = sms.DescrStatsW(resource_meter_7k).tconfint_mean()
    resource_meter_8k = resource_meter20[method_condition]['time']
    
    ci_8k = sms.DescrStatsW(resource_meter_8k).tconfint_mean()
    resource_meter_10k = resource_meter21[method_condition]['time']
    
    ci_10k = sms.DescrStatsW(resource_meter_10k).tconfint_mean()
    resource_meter_15k = resource_meter22[method_condition]['time']
    
    resource_meter_12k = resource_meter23[method_condition]['time']
    ci_12k = sms.DescrStatsW(resource_meter_12k).tconfint_mean()
    
    resource_meter_13k = resource_meter24[method_condition]['time']
    ci_13k = sms.DescrStatsW(resource_meter_13k).tconfint_mean()
    
    resource_meter_15k = resource_meter22[method_condition]['time']
    ci_15k = sms.DescrStatsW(resource_meter_15k).tconfint_mean()

    y = [np.mean(ci_300),np.mean(ci_500),np.mean(ci_1k),np.mean(ci_2k),np.mean(ci_3k),np.mean(ci_5k),np.mean(ci_7k),np.mean(ci_8k),np.mean(ci_10k),np.mean(ci_12k),np.mean(ci_13k),np.mean(ci_15k)]
    plt.scatter(x, y, color=color, label=label, marker=marker, alpha=0.3)

    ax.legend(loc='best')
    fig.savefig(out_folder + 'time_vs_N.png', dpi=my_dpi)
    plt.close()

    ###################################################################################################################
    # SUMMARY PLOT RESOURCES max RAM vs N  ############################################################################
    ###################################################################################################################
    out_folder = '../graphs/'
    my_dpi = 300
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    #ax.set_xlim([0, 0.65])
    #ax.set_ylim([0.65, 1.02])
    title = 'RAM usage (max) vs network size'
    ax.set_title(title)
    ax.set_xlabel('number of nodes')
    ax.set_ylabel('MB')
    x = [300, 500, 1000, 2000, 3000, 5000, 7000, 8000, 10000, 12000, 13000, 15000]
    resource_condition = 'max_RAM'
    
    #R1
    color = 'b'; label = 'R1'; marker = '>';
    method_condition = (resource_meter13['method'] == label)
    
    resource_meter_300 =resource_meter13[method_condition][resource_condition]
    ci_300 = sms.DescrStatsW(resource_meter_300).tconfint_mean()
    
    resource_meter_500 = resource_meter14[method_condition][resource_condition]
    ci_500 = sms.DescrStatsW(resource_meter_500).tconfint_mean()
    
    resource_meter_1k = resource_meter15[method_condition][resource_condition]
    ci_1k = sms.DescrStatsW(resource_meter_1k).tconfint_mean()
    
    resource_meter_2k = resource_meter16[method_condition][resource_condition]
    ci_2k = sms.DescrStatsW(resource_meter_2k).tconfint_mean()
    
    resource_meter_3k = resource_meter17[method_condition][resource_condition]
    ci_3k = sms.DescrStatsW(resource_meter_3k).tconfint_mean()
    
    resource_meter_5k = resource_meter18[method_condition][resource_condition]
    ci_5k = sms.DescrStatsW(resource_meter_5k).tconfint_mean()
    
    resource_meter_7k = resource_meter19[method_condition][resource_condition]
    ci_7k = sms.DescrStatsW(resource_meter_7k).tconfint_mean()
    
    resource_meter_8k = resource_meter20[method_condition][resource_condition]
    ci_8k = sms.DescrStatsW(resource_meter_8k).tconfint_mean()
    
    resource_meter_10k = resource_meter21[method_condition][resource_condition]
    ci_10k = sms.DescrStatsW(resource_meter_10k).tconfint_mean()
    
    resource_meter_12k = resource_meter23[method_condition][resource_condition]
    ci_12k = sms.DescrStatsW(resource_meter_12k).tconfint_mean()
    
    resource_meter_13k = resource_meter24[method_condition][resource_condition]
    ci_13k = sms.DescrStatsW(resource_meter_13k).tconfint_mean()
    
    resource_meter_15k = resource_meter22[method_condition][resource_condition]
    ci_15k = sms.DescrStatsW(resource_meter_15k).tconfint_mean()
    
    y = [np.mean(ci_300),np.mean(ci_500),np.mean(ci_1k),np.mean(ci_2k),np.mean(ci_3k),np.mean(ci_5k),np.mean(ci_7k),np.mean(ci_8k),np.mean(ci_10k),np.mean(ci_12k),np.mean(ci_13k),np.mean(ci_15k)]
    plt.scatter(x, y, color=color, label=label, marker=marker, alpha=0.3)

    #M1
    color = 'g'; label = 'M1'; marker = '<';
    method_condition = (resource_meter13['method'] == label)

    resource_meter_300 =resource_meter13[method_condition][resource_condition]
    ci_300 = sms.DescrStatsW(resource_meter_300).tconfint_mean()
    
    resource_meter_500 = resource_meter14[method_condition][resource_condition]
    ci_500 = sms.DescrStatsW(resource_meter_500).tconfint_mean()
    
    resource_meter_1k = resource_meter15[method_condition][resource_condition]
    ci_1k = sms.DescrStatsW(resource_meter_1k).tconfint_mean()
    
    resource_meter_2k = resource_meter16[method_condition][resource_condition]
    ci_2k = sms.DescrStatsW(resource_meter_2k).tconfint_mean()
    
    resource_meter_3k = resource_meter17[method_condition][resource_condition]
    ci_3k = sms.DescrStatsW(resource_meter_3k).tconfint_mean()
    
    resource_meter_5k = resource_meter18[method_condition][resource_condition]
    ci_5k = sms.DescrStatsW(resource_meter_5k).tconfint_mean()
    
    resource_meter_7k = resource_meter19[method_condition][resource_condition]
    ci_7k = sms.DescrStatsW(resource_meter_7k).tconfint_mean()
    
    resource_meter_8k = resource_meter20[method_condition][resource_condition]
    ci_8k = sms.DescrStatsW(resource_meter_8k).tconfint_mean()
    
    resource_meter_10k = resource_meter21[method_condition][resource_condition]
    ci_10k = sms.DescrStatsW(resource_meter_10k).tconfint_mean()
    
    resource_meter_12k = resource_meter23[method_condition][resource_condition]
    ci_12k = sms.DescrStatsW(resource_meter_12k).tconfint_mean()
    
    resource_meter_13k = resource_meter24[method_condition][resource_condition]
    ci_13k = sms.DescrStatsW(resource_meter_13k).tconfint_mean()
    
    resource_meter_15k = resource_meter22[method_condition][resource_condition]
    ci_15k = sms.DescrStatsW(resource_meter_15k).tconfint_mean()
    
    y = [np.mean(ci_300),np.mean(ci_500),np.mean(ci_1k),np.mean(ci_2k),np.mean(ci_3k),np.mean(ci_5k),np.mean(ci_7k),np.mean(ci_8k),np.mean(ci_10k),np.mean(ci_12k),np.mean(ci_13k),np.mean(ci_15k)]
    plt.scatter(x, y, color=color, label=label, marker=marker, alpha=0.3)

    #K1
    color = 'r'; label = 'K1'; marker = '^';
    method_condition = (resource_meter13['method'] == label)

    resource_meter_300 =resource_meter13[method_condition][resource_condition]
    ci_300 = sms.DescrStatsW(resource_meter_300).tconfint_mean()
    
    resource_meter_500 = resource_meter14[method_condition][resource_condition]
    ci_500 = sms.DescrStatsW(resource_meter_500).tconfint_mean()
    
    resource_meter_1k = resource_meter15[method_condition][resource_condition]
    ci_1k = sms.DescrStatsW(resource_meter_1k).tconfint_mean()
    
    resource_meter_2k = resource_meter16[method_condition][resource_condition]
    ci_2k = sms.DescrStatsW(resource_meter_2k).tconfint_mean()
    
    resource_meter_3k = resource_meter17[method_condition][resource_condition]
    ci_3k = sms.DescrStatsW(resource_meter_3k).tconfint_mean()
    
    resource_meter_5k = resource_meter18[method_condition][resource_condition]
    ci_5k = sms.DescrStatsW(resource_meter_5k).tconfint_mean()
    
    resource_meter_7k = resource_meter19[method_condition][resource_condition]
    ci_7k = sms.DescrStatsW(resource_meter_7k).tconfint_mean()
    
    resource_meter_8k = resource_meter20[method_condition][resource_condition]
    ci_8k = sms.DescrStatsW(resource_meter_8k).tconfint_mean()
    
    resource_meter_10k = resource_meter21[method_condition][resource_condition]
    ci_10k = sms.DescrStatsW(resource_meter_10k).tconfint_mean()
    
    resource_meter_12k = resource_meter23[method_condition][resource_condition]
    ci_12k = sms.DescrStatsW(resource_meter_12k).tconfint_mean()
    
    resource_meter_13k = resource_meter24[method_condition][resource_condition]
    ci_13k = sms.DescrStatsW(resource_meter_13k).tconfint_mean()
    
    resource_meter_15k = resource_meter22[method_condition][resource_condition]
    ci_15k = sms.DescrStatsW(resource_meter_15k).tconfint_mean()
    
    y = [np.mean(ci_300),np.mean(ci_500),np.mean(ci_1k),np.mean(ci_2k),np.mean(ci_3k),np.mean(ci_5k),np.mean(ci_7k),np.mean(ci_8k),np.mean(ci_10k),np.mean(ci_12k),np.mean(ci_13k),np.mean(ci_15k)]
    plt.scatter(x, y, color=color, label=label, marker=marker, alpha=0.3)


    #louvain
    color='gray'; label='louvain'; marker='o';
    method_condition = (resource_meter13['method'] == 'L')


    resource_meter_300 =resource_meter13[method_condition][resource_condition]
    ci_300 = sms.DescrStatsW(resource_meter_300).tconfint_mean()
    
    resource_meter_500 = resource_meter14[method_condition][resource_condition]
    ci_500 = sms.DescrStatsW(resource_meter_500).tconfint_mean()
    
    resource_meter_1k = resource_meter15[method_condition][resource_condition]
    ci_1k = sms.DescrStatsW(resource_meter_1k).tconfint_mean()
    
    resource_meter_2k = resource_meter16[method_condition][resource_condition]
    ci_2k = sms.DescrStatsW(resource_meter_2k).tconfint_mean()
    
    resource_meter_3k = resource_meter17[method_condition][resource_condition]
    ci_3k = sms.DescrStatsW(resource_meter_3k).tconfint_mean()
    
    resource_meter_5k = resource_meter18[method_condition][resource_condition]
    ci_5k = sms.DescrStatsW(resource_meter_5k).tconfint_mean()
    
    resource_meter_7k = resource_meter19[method_condition][resource_condition]
    ci_7k = sms.DescrStatsW(resource_meter_7k).tconfint_mean()
    
    resource_meter_8k = resource_meter20[method_condition][resource_condition]
    ci_8k = sms.DescrStatsW(resource_meter_8k).tconfint_mean()
    
    resource_meter_10k = resource_meter21[method_condition][resource_condition]
    ci_10k = sms.DescrStatsW(resource_meter_10k).tconfint_mean()
    
    resource_meter_12k = resource_meter23[method_condition][resource_condition]
    ci_12k = sms.DescrStatsW(resource_meter_12k).tconfint_mean()
    
    resource_meter_13k = resource_meter24[method_condition][resource_condition]
    ci_13k = sms.DescrStatsW(resource_meter_13k).tconfint_mean()
    
    resource_meter_15k = resource_meter22[method_condition][resource_condition]
    ci_15k = sms.DescrStatsW(resource_meter_15k).tconfint_mean()
    
    y = [np.mean(ci_300),np.mean(ci_500),np.mean(ci_1k),np.mean(ci_2k),np.mean(ci_3k),np.mean(ci_5k),np.mean(ci_7k),np.mean(ci_8k),np.mean(ci_10k),np.mean(ci_12k),np.mean(ci_13k),np.mean(ci_15k)]
    plt.scatter(x, y, color=color, label=label, marker=marker, alpha=0.3)

    ax.legend(loc='best')
    fig.savefig(out_folder + 'RAM_vs_N.png', dpi=my_dpi)
    plt.close()

    ###################################################################################################################
    # SUMMARY PLOT NMI vs mu  #########################################################################################
    ###################################################################################################################
    out_folder = '../graphs/'
    my_dpi = 300
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.set_xlim([0, 0.65])
    ax.set_ylim([0.85, 1.01])
    title = 'Clustering performance (NMI) vs mixing parameter'
    ax.set_title(title)
    ax.set_xlabel('fraction of intra-community edges')
    ax.set_ylabel('Clustering performance (Normalized Mutual Information)')
    for method in methods:
        N_condition_5k = (grid.scores['N'] == 5000)
        N_condition_7k = (grid.scores['N'] == 7000)
        N_condition_8k = (grid.scores['N'] == 8000)
        N_condition_10k = (grid.scores['N'] == 10000)
        # going beyond 10k does not change the trend. takes a long time when trying to extend the range to higher mu
        #N_condition_12k = (grid.scores['N'] == 12000)
        #N_condition_13k = (grid.scores['N'] == 13000)
        #N_condition_15k = (grid.scores['N'] == 15000)

        method_condition = (grid.scores['METHOD'] == method)
        data = grid.scores[method_condition & (N_condition_5k | N_condition_7k | N_condition_8k | N_condition_10k)]
        if(method == 'K1'): color = 'r'; label = 'K1'; marker = '^'; 
        if(method == 'M1'): color = 'g'; label = 'M1'; marker = '<';
        if(method == 'R1'): color = 'b'; label = 'R1'; marker = '>';
        if(method=='louvain'): color='gray'; label='louvain'; marker='o';
                        
        # average over multiple runs: determine confidence interval
        x = data['mut']
        y = data['SCORE']
        mut_01_condition = (x == 0.1); y_01 = y[mut_01_condition]
        mut_02_condition = (x == 0.2); y_02 = y[mut_02_condition]
        mut_03_condition = (x == 0.3); y_03 = y[mut_03_condition]
        mut_04_condition = (x == 0.4); y_04 = y[mut_04_condition]
        mut_05_condition = (x == 0.5); y_05 = y[mut_05_condition]
        mut_06_condition = (x == 0.6); y_06 = y[mut_06_condition]
        ci_01 = sms.DescrStatsW(y_01).tconfint_mean()
        ci_02 = sms.DescrStatsW(y_02).tconfint_mean()
        ci_03 = sms.DescrStatsW(y_03).tconfint_mean()
        ci_04 = sms.DescrStatsW(y_04).tconfint_mean()
        ci_05 = sms.DescrStatsW(y_05).tconfint_mean()
        ci_06 = sms.DescrStatsW(y_06).tconfint_mean()
        # plot average of confidence interval
        y_avg = [np.mean(ci_01), np.mean(ci_02), np.mean(ci_03), np.mean(ci_04), np.mean(ci_05), np.mean(ci_06)]
        x_avg = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        plt.scatter(x_avg, y_avg, color=color, label=label, marker=marker, alpha=0.3)
    ax.legend(loc='best')
    fig.savefig(out_folder + 'NMI_vs_mu.png', dpi=my_dpi)
    plt.close()


    ###################################################################################################################
    # SUMMARY PLOT NMI vs N  ###########################################################################################
    ###################################################################################################################
    out_folder = '../graphs/'
    my_dpi = 300
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    #ax.set_xlim([0, 0.65])
    ax.set_ylim([0.65, 1.02])
    title = 'Clustering performance (NMI) vs network size'
    ax.set_title(title)
    ax.set_xlabel('number of nodes')
    ax.set_ylabel('Clustering performance (Normalized Mutual Information)')
    for method in methods:
        method_condition = (grid.scores['METHOD'] == method)
        data = grid.scores[method_condition]
        if(method == 'K1'): color = 'r'; label = 'K1'; marker = '^'; 
        if(method == 'M1'): color = 'g'; label = 'M1'; marker = '<';
        if(method == 'R1'): color = 'b'; label = 'R1'; marker = '>';
        if(method=='louvain'): color='gray'; label='louvain'; marker='o';
                        
        # average over multiple runs: determine confidence interval
        x = data['N']
        y = data['SCORE']
        N_condition_300 = (x == 300); y_300 = y[N_condition_300]
        N_condition_500 = (x == 500); y_500 = y[N_condition_500]
        N_condition_1k = (x == 1000); y_1k = y[N_condition_1k]
        N_condition_2k = (x == 2000); y_2k = y[N_condition_2k]
        N_condition_3k = (x == 3000); y_3k = y[N_condition_3k]
        N_condition_5k = (x == 5000); y_5k = y[N_condition_5k]
        N_condition_7k = (x == 7000); y_7k = y[N_condition_7k]
        N_condition_8k = (x == 8000); y_8k = y[N_condition_8k]
        N_condition_10k = (x == 10000); y_10k = y[N_condition_10k]
        N_condition_12k = (x == 12000); y_12k = y[N_condition_12k]
        N_condition_13k = (x == 13000); y_13k = y[N_condition_13k]
        N_condition_15k = (x == 15000); y_15k = y[N_condition_15k]


        ci_300 = sms.DescrStatsW(y_300).tconfint_mean()
        ci_500 = sms.DescrStatsW(y_500).tconfint_mean()
        ci_1k = sms.DescrStatsW(y_1k).tconfint_mean()
        ci_2k = sms.DescrStatsW(y_2k).tconfint_mean()
        ci_3k = sms.DescrStatsW(y_3k).tconfint_mean()
        ci_5k = sms.DescrStatsW(y_5k).tconfint_mean()
        ci_7k = sms.DescrStatsW(y_7k).tconfint_mean()
        ci_8k = sms.DescrStatsW(y_8k).tconfint_mean()
        ci_10k = sms.DescrStatsW(y_10k).tconfint_mean()
        ci_12k = sms.DescrStatsW(y_12k).tconfint_mean()
        ci_13k = sms.DescrStatsW(y_13k).tconfint_mean()
        ci_15k = sms.DescrStatsW(y_15k).tconfint_mean()


        # plot average of confidence interval
        y_avg = [np.mean(ci_300), np.mean(ci_500), np.mean(ci_1k), np.mean(ci_2k), np.mean(ci_3k), np.mean(ci_5k), np.mean(ci_7k), np.mean(ci_8k), np.mean(ci_10k), np.mean(ci_12k),np.mean(ci_13k),np.mean(ci_15k)]
        x_avg = [300, 500, 1000, 2000, 3000, 5000, 7000, 8000, 10000, 12000, 13000, 15000]
        plt.scatter(x_avg, y_avg, color=color, label=label, marker=marker, alpha=0.3)
    ax.legend(loc='best')
    fig.savefig(out_folder + 'NMI_vs_N.png', dpi=my_dpi)
    plt.close()


    ###################################################################################################################
    # DETAILED PLOTS (as a function of all parameters)   ##############################################################
    ###################################################################################################################
    for N in grid.N:
        out_folder_N = '../graphs/_N' + str(N) + '/'
        os.system('rm -rf ' + out_folder_N + ' && mkdir ' + out_folder_N)
        for t1 in grid.t1:
            out_folder_t1 = out_folder_N + '_t1' + str(t1) + '/'
            os.system('rm -rf ' + out_folder_t1 + ' && mkdir ' + out_folder_t1)
            for beta in grid.beta:
                out_folder_beta = out_folder_t1 + '_beta' + str(beta) + '/'
                os.system('rm -rf ' + out_folder_beta + ' && mkdir ' + out_folder_beta)
                for k in grid.k:
                    #fig = plt.figure(figsize=(5,5))
                    my_dpi=300
                    fig = plt.figure(figsize=(4, 4))
                    ax = fig.add_subplot(111)
                    ax.set_xlim([0,0.65])
                    ax.set_ylim([-0.05,1.05])
                    '''
                    if N==5000:
                        ax.set_xlim([0.05,0.65])
                        ax.set_ylim([0.95,1.002])
                    else:
                        ax.set_xlim([0.05,0.65])
                        ax.set_ylim([0.75,1.02])
                    '''
                    title = 'N: ' + str(N) + ', γ: ' + str(t1) + ', β:' + str(beta) + ', k: ' + str(k)
                    ax.set_title(title)
                    ax.set_xlabel('μ')
                    ax.set_ylabel('NMI')
                    for method in methods:
                        N_condition = (grid.scores['N'] == N)
                        t1_condition = (grid.scores['t1'] == t1)
                        beta_condition = (grid.scores['beta'] == beta)
                        method_condition = (grid.scores['METHOD'] == method)
                        k_condition = (grid.scores['k'] == k)
                        data = grid.scores[N_condition & t1_condition & beta_condition & method_condition & k_condition]
                        if(method=='K1'): color='r'; label='K1'; marker='^'; 
                        if(method=='M1'): color='g'; label='M1'; marker='<';
                        if(method=='R1'): color='b'; label='R1'; marker='>';
                        if(method=='louvain'): color='gray'; label='louvain'; marker='o';

                        # average over multiple runs: determine confidence interval
                        x = data['mut']
                        y = data['SCORE']
                        mut_01_condition = (x == 0.1); y_01 = y[mut_01_condition]
                        mut_02_condition = (x == 0.2); y_02 = y[mut_02_condition]
                        mut_03_condition = (x == 0.3); y_03 = y[mut_03_condition]
                        mut_04_condition = (x == 0.4); y_04 = y[mut_04_condition]
                        mut_05_condition = (x == 0.5); y_05 = y[mut_05_condition]
                        mut_06_condition = (x == 0.6); y_06 = y[mut_06_condition]
                        ci_01 = sms.DescrStatsW(y_01).tconfint_mean()
                        ci_02 = sms.DescrStatsW(y_02).tconfint_mean()
                        ci_03 = sms.DescrStatsW(y_03).tconfint_mean()
                        ci_04 = sms.DescrStatsW(y_04).tconfint_mean()
                        ci_05 = sms.DescrStatsW(y_05).tconfint_mean()
                        ci_06 = sms.DescrStatsW(y_06).tconfint_mean()
                        # plot average of confidence interval
                        y_avg = [np.mean(ci_01), np.mean(ci_02), np.mean(ci_03), np.mean(ci_04), np.mean(ci_05), np.mean(ci_06)]
                        x_avg = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
                        plt.scatter(x_avg, y_avg, color=color, label=label, marker=marker, alpha=0.3)
                        '''
                        # plot average as a smooth curve
                        xsmooth = np.linspace(x.min(),x.max(),300)
                        f_avg = interpolate.interp1d(x_avg, y_avg, kind='cubic')
                        ysmooth_avg = f_avg(xsmooth)
                        plt.plot(xsmooth, ysmooth_avg,color=color) #label=label)
                        # plot confidence intervals
                        y_lower = [np.mean([min(y_01),y_avg[0]]),np.mean([min(y_02),y_avg[1]]),np.mean([min(y_03),y_avg[2]]),np.mean([min(y_04),y_avg[3]]),np.mean([min(y_05),y_avg[4]]),np.mean([min(y_06),y_avg[5]])] #y_lower = [ci_01[0],ci_02[0],ci_03[0],ci_04[0],ci_05[0],ci_06[0]]
                        f_lower = interpolate.interp1d(x_avg, y_lower, kind='cubic')
                        ysmooth_lower = f_lower(xsmooth)
                        y_upper = [np.mean([max(y_01), y_avg[0]]),
                            np.mean([max(y_02), y_avg[1]]),
                            np.mean([max(y_03),y_avg[2]]),
                            np.mean([max(y_04), y_avg[3]]),
                            np.mean([max(y_05), y_avg[4]]),
                            np.mean([max(y_06),y_avg[5]])]#y_upper = [ci_01[1],ci_02[1],ci_03[1],ci_04[1],ci_05[1],ci_06[1]]
                        f_upper = interpolate.interp1d(x_avg, y_upper, kind='cubic')
                        ysmooth_upper = f_upper(xsmooth)
                        plt.fill_between(xsmooth, ysmooth_lower, ysmooth_upper, alpha=0.3, facecolor=color'
                        '''
                    ax.legend(loc='best')
                    fig.savefig(out_folder_beta + 'k_' + str(k) + '.png', dpi=my_dpi)
                    plt.close()
                    
                    
    ###################################################################################################################
    # DETAILED PLOTS (one for each N folder)   ########################################################################
    ###################################################################################################################
    for N in grid.N:
        out_folder_N = '../graphs/_N' + str(N) + '/'
        my_dpi = 300
        fig = plt.figure(figsize=(4, 4))
        ax = fig.add_subplot(111)
        ax.set_xlim([0, 0.65])
        ax.set_ylim([-0.05, 1.05])
        '''
        if N==5000:
            ax.set_xlim([0.05,0.65])
            ax.set_ylim([0.95,1.002])
        else:
            ax.set_xlim([0.05,0.65])
            ax.set_ylim([0.75,1.02])
        '''
        title = 'N: ' + str(N)
        ax.set_title(title)
        ax.set_xlabel('μ')
        ax.set_ylabel('NMI')
        for method in methods:
            N_condition = (grid.scores['N'] == N)
            method_condition = (grid.scores['METHOD'] == method)
            data = grid.scores[N_condition & method_condition]
            if(method == 'K1'): color = 'r'; label = 'K1'; marker = '^'; 
            if(method == 'M1'): color = 'g'; label = 'M1'; marker = '<';
            if(method == 'R1'): color = 'b'; label = 'R1'; marker = '>';
            if(method=='louvain'): color='gray'; label='louvain'; marker='o';
                        
            # average over multiple runs: determine confidence interval
            x = data['mut']
            y = data['SCORE']
            mut_01_condition = (x == 0.1); y_01 = y[mut_01_condition]
            mut_02_condition = (x == 0.2); y_02 = y[mut_02_condition]
            mut_03_condition = (x == 0.3); y_03 = y[mut_03_condition]
            mut_04_condition = (x == 0.4); y_04 = y[mut_04_condition]
            mut_05_condition = (x == 0.5); y_05 = y[mut_05_condition]
            mut_06_condition = (x == 0.6); y_06 = y[mut_06_condition]
            ci_01 = sms.DescrStatsW(y_01).tconfint_mean()
            ci_02 = sms.DescrStatsW(y_02).tconfint_mean()
            ci_03 = sms.DescrStatsW(y_03).tconfint_mean()
            ci_04 = sms.DescrStatsW(y_04).tconfint_mean()
            ci_05 = sms.DescrStatsW(y_05).tconfint_mean()
            ci_06 = sms.DescrStatsW(y_06).tconfint_mean()
            # plot average of confidence interval
            y_avg = [np.mean(ci_01), np.mean(ci_02), np.mean(ci_03), np.mean(ci_04), np.mean(ci_05), np.mean(ci_06)]
            x_avg = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
            plt.scatter(x_avg, y_avg, color=color, label=label, marker=marker, alpha=0.3)
        ax.legend(loc='best')
        fig.savefig(out_folder_N + str(N) +'.png', dpi=my_dpi)
        plt.close()




if __name__ == '__main__':
    print("\n---------------------------PLOTTING DreamDMI BENCHMARKS-------------------------\n")
    run()
    print("\n-------------------------DONE PLOTTING DreamDMI BENCHMARKS-----------------------\n")
