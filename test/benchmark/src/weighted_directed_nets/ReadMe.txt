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

This program is an implementation of the algorithm described in the paper "Directed, weighted and overlapping benchmark graphs for community detection algorithms", written by Andrea Lancichinetti and Santo Fortunato. In particular, this program is to produce directed weighted networks with overlapping nodes. 
Each feedback is very welcome. If you have found a bug or have problems, or want to give advises, please contact us:

andrea.lancichinetti@isi.it
fortunato@isi.it


Turin, 21 August 2009
---------------------------------------------------------------





-------------------- How to compile -----------------------------------
In order to compile, type:

make

-------------------- How to run the program —————————————

To run the program, type:

./benchmark [FLAG] [P]


[FLAG]		[P]

-N		number of nodes
-k		average degree
-maxk		maximum degree
-mut		mixing parameter for the topology
-muw		mixing parameter for the weights
-beta		exponent for the weight distribution
-t1		minus exponent for the degree sequence
-t2		minus exponent for the community size distribution
-minc		minimum for the community sizes
-maxc		maximum for the community sizes
-on		number of overlapping nodes
-om		number of memberships of the overlapping nodes
----------------------

The degree you can set is the in-degree. The out-degree distribution will be chosen but the program close to a delta function. The topological mixing parameter is the same for both the in-degree and the out-degree, but the latter one might be modified to satisfy the constraints necessary to close the network.

In this program you can assign the number of overlapping nodes (option -on) and assign the number of memberships for them (option -om). The other nodes will have only one membership. For instance, typing 

./benchmark [flags...] -N 1000 -on 20 -om 2

will produce a network with 1000 nodes, 980 with only one membership and 20 nodes with two memberships.

It is also possible to set the parameters writing flags and relative numbers in a file (look at flags.dat to see an example). To specify the file, use the option:

-f	[filename]

You can set the parameters both writing some of them in the file, and using flags from the command line for others (if you set a parameter twice, the latter one will be taken).

-N, -k, -maxk, -muw have to be specified. For the others, the program can use default values:

t1=2, 	t2=1, 	on=0,	om=0,	beta=1.5, mut=muw, minc and maxc will be chosen close to the degree sequence extremes.



-------------------- Other options ---------------------------

To have a random network use:
-rand

Using this option will set mut=0, muw=0 and minc=maxc=N, i.e. there will be one only community.

Use option:
-sup (-inf) 

if you want to produce a benchmark whose distribution of the ratio of external in-degree/total in-degree is superiorly (inferiorly) bounded by the mixing parameter (only for the topology). In other words, if you use one of these options, the mixing parameter is not the average ratio of external degree/total degree (as it used to be) but the maximum (or the minimum) of that distribution. When using one of these options, what the program essentially does is to approximate the external degree always by excess (or by defect) and if necessary to modify the degree distribution. Nevertheless, this last possibility occurs for a few nodes and numerical simulations show that it does not affect the degree distribution appreciably.


-------------------- Examples ---------------------------

Example1:
./benchmark -N 1000 -k 15 -maxk 50 -muw 0.1 -minc 20 -maxc 50
Example2:
./benchmark -f flags.dat -t1 3

If you want to produce a kind of Girvan-Newman benchmark, you can type:
./benchmark -N 128 -k 16 -maxk 16 -muw 0.1 -minc 32 -maxc 32 -beta 1


-------------------- Output ---------------------------

Please note that the community size distribution can be modified by the program to satisfy several constraints (a warning will be displayed).

The program will produce three files:

1) network.dat contains the list of edges (nodes are labelled from 1 to the number of nodes; the edges are ordered and repeated once, i.e. source-target), with the relative weight.

2) community.dat contains a list of the nodes and their membership (memberships are labelled by integer numbers >=1).

3) statistics.dat contains the in and out-degree degree distribution (in logarithmic bins), the community size distribution, the distribution of the mixing parameter for the topology (in and out) and the weights, and the internal and external weight distribution.



-------------------- Seed for the random number generator ---------------------------
 

-In the file time_seed.dat you can edit the seed which generates the random numbers. After reading, the program will increase this number by 1 (this is done to generate different networks running the program again and again). If the file is erased, it will be produced by the program again.


