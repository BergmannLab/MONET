#! /bin/sh -
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
# FULL SYSTEM TEST
# This is a thorough system test.
# We run all methods on all challenge inputs using both Docker and Singularity.
# The results are to be scored for evaluation (some methods are stochastic)
###############################################################################

# clean previous runs
output=./output_reproduce_challenge
rm -rf $output
mkdir $output
# clean all singularity and docker images
yes | sudo docker system prune -a > /dev/null
rm -f $HOME/.monet/containers/*/singularity/*.img



# R1 - CAUSALITY
monet --input=./input/1_ppi_anonym_v2.txt --output=$output --method=R1 --container=singularity \
  --b=2.4 --c=800 --i=2 --filter=double --threshold=4 --post=recluster --smallest=3 --largest=100 --b2=2.4 --c2=800 --i2=2
monet --input=./input/1_ppi_anonym_v2.txt --output=$output --method=R1 --container=docker \
  --b=2.4 --c=800 --i=2 --filter=double --threshold=4 --post=recluster --smallest=3 --largest=100 --b2=2.4 --c2=800 --i2=2

monet --input=./input/2_ppi_anonym_v2.txt --output=$output --method=R1 --container=singularity \
  --b=1.3 --c=500 --i=2 --filter=pageRank --threshold=3 --post=recluster --smallest=5 --largest=100 --b2=1.3 --c2=500 --i2=2 
monet --input=./input/2_ppi_anonym_v2.txt --output=$output --method=R1 --container=docker \
  --b=1.3 --c=500 --i=2 --filter=pageRank --threshold=3 --post=recluster --smallest=5 --largest=100 --b2=1.3 --c2=500 --i2=2

monet --input=./input/3_signal_anonym_directed_v3.txt --output=$output --method=R1 --container=singularity \
  --b=1.7 --c=400 --i=2 --filter=quantile --threshold=1 --post=discard --smallest=3 --largest=100 --b2=1.7 --c2=500 --i2=2 
monet --input=./input/3_signal_anonym_directed_v3.txt --output=$output --method=R1 --container=docker \
  --b=1.7 --c=400 --i=2 --filter=quantile --threshold=1 --post=discard --smallest=3 --largest=100 --b2=1.7 --c2=500 --i2=2

monet --input=./input/4_coexpr_anonym_v2.txt --output=$output --method=R1 --container=singularity \
  --b=1.8 --c=600 --i=2 --filter=quantile --threshold=4 --post=recluster --smallest=3 --largest=100 --b2=0.5 --c2=800 --i2=2 
monet --input=./input/4_coexpr_anonym_v2.txt --output=$output --method=R1 --container=docker \
  --b=1.8 --c=600 --i=2 --filter=quantile --threshold=4 --post=recluster --smallest=3 --largest=100 --b2=0.5 --c2=800 --i2=2

monet --input=./input/5_cancer_anonym_v2.txt --output=$output --method=R1 --container=singularity \
  --b=2 --c=600 --i=1.8 --filter=quantile --threshold=2 --post=discard --smallest=5 --largest=100 --b2=2 --c2=600 --i2=1.8 
monet --input=./input/5_cancer_anonym_v2.txt --output=$output --method=R1 --container=docker \
  --b=2 --c=600 --i=1.8 --filter=quantile --threshold=2 --post=discard --smallest=5 --largest=100 --b2=2 --c2=600 --i2=1.8

monet --input=./input/6_homology_anonym_v2.txt --output=$output --method=R1 --container=singularity \
  --b=3.5 --c=1000 --i=2 --filter=double --threshold=4 --post=recluster --smallest=10 --largest=100 --b2=0.5 --c2=800 --i2=2 
monet --input=./input/6_homology_anonym_v2.txt --output=$output --method=R1 --container=docker \
  --b=3.5 --c=1000 --i=2 --filter=double --threshold=4 --post=recluster --smallest=10 --largest=100 --b2=0.5 --c2=800 --i2=2



# M1 - ALEPH

monet --input=./input/1_ppi_anonym_v2.txt --output=$output --method=M1 --container=singularity
monet --input=./input/1_ppi_anonym_v2.txt --output=$output --method=M1 --container=docker

monet --input=./input/2_ppi_anonym_v2.txt --output=$output --method=M1 --container=singularity
monet --input=./input/2_ppi_anonym_v2.txt --output=$output --method=M1 --container=docker

monet --input=./input/3_signal_anonym_directed_v3.txt --output=$output --method=M1 --container=singularity
monet --input=./input/3_signal_anonym_directed_v3.txt --output=$output --method=M1 --container=docker

monet --input=./input/4_coexpr_anonym_v2.txt --output=$output --method=M1 --container=singularity
monet --input=./input/4_coexpr_anonym_v2.txt --output=$output --method=M1 --container=docker

monet --input=./input/5_cancer_anonym_v2.txt --output=$output --method=M1 --container=singularity
monet --input=./input/5_cancer_anonym_v2.txt --output=$output --method=M1 --container=docker

monet --input=./input/6_homology_anonym_v2.txt --output=$output --method=M1 --container=singularity
monet --input=./input/6_homology_anonym_v2.txt --output=$output --method=M1 --container=docker



# K1 - TUSK

monet --input=./input/2_ppi_anonym_v2.txt --output=$output --method=K1 --container=singularity
monet --input=./input/2_ppi_anonym_v2.txt --output=$output --method=K1 --container=docker

monet --input=./input/3_signal_anonym_directed_v3.txt --output=$output --method=K1 --container=singularity
monet --input=./input/3_signal_anonym_directed_v3.txt --output=$output --method=K1 --container=docker

monet --input=./input/4_coexpr_anonym_v2.txt --output=$output --method=K1 --container=singularity#OK
monet --input=./input/4_coexpr_anonym_v2.txt --output=$output --method=K1 --container=docker

monet --input=./input/5_cancer_anonym_v2.txt --output=$output --method=K1 --container=singularity
monet --input=./input/5_cancer_anonym_v2.txt --output=$output --method=K1 --container=docker

monet --input=./input/6_homology_anonym_v2.txt --output=$output --method=K1 --container=singularity
monet --input=./input/6_homology_anonym_v2.txt --output=$output --method=K1 --container=docker
