#!/usr/bin/env Rscript
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

getwd()
library(igraph)
source("./mlrmcl_r4_v2.R") 

# PARAMETERS:
args = commandArgs(trailingOnly=TRUE)
# filename: input file
filename=args[1]
# b: balance parameter
b=as.numeric(args[2])
# c: size of the coarsened graph
c=as.numeric(args[3])
# i: inflation parameter
i=as.numeric(args[4])
# filter: preprocessing strategy
filter=args[5]
# threshold: the quantile threshold for preprocessing
threshold=as.numeric(args[6])
# inteWeight: whether perform the weight transforming in preprocessing
interWeight=args[7]
# weighted: whether the graph is treated as weighted graph (redundant since all graph are treated as weighted)
weighted=as.logical(args[8])
# dir: the directory for output files
dir=args[9]
# post: strategy for postprocessing
post=args[10]
# smallest: clusters smaller than this value is discarded
smallest=as.numeric(args[11])
# largest:  clusters larger than this value is discarded (after reclustering)
largest=as.numeric(args[12])
# b2, c2, i2: the recluster parameters if post="recluster"
b2=as.numeric(args[13])
c2=as.numeric(args[14])
i2=as.numeric(args[15])


# RUN METHOD
graph<-main(filename,b,c,i,filter,threshold,interWeight,weighted,dir,post,smallest,largest,b2,c2,i2)
