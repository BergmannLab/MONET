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
# QUICK INSTALL TEST
# This is a quick test to make sure the installation procedure succeeded.
# We run the quickest method (R1, team "Causality") on the smallest challenge
# input using whatever container is available and check the exit code.
###############################################################################

output=/tmp/monet_quick_test/
rm -rf $output
mkdir $output

checkOutput() {
  # check the output file contains the success message
  if ! grep -r -q "Output is written to file" $output; then
    echo "Test failed"
    echo see "$output"console_output.txt for details
    exit 1
  else
    echo "Test succeeded"
    exit 0
  fi
}

#if Singularity is installed
singularity --help > /tmp/singularity_test 2>&1
if [ $? -eq "0" ]; then
  echo testing with singularity
  monet --input=./input/3_signal_anonym_directed_v3.txt --output=$output --method=R1 --container=singularity \
    --b=1.7 --c=400 --i=2 --filter=quantile --threshold=1 --post=discard --smallest=3 --largest=100 --b2=1.7 --c2=500 --i2=2 \
    > $output/console_output.txt 2>&1
  checkOutput
fi

# if Docker is installed
docker --help > /tmp/docker_test 2>&1
if [ $? -eq "0" ]; then
  echo testing with docker
  monet --input=./input/3_signal_anonym_directed_v3.txt --output=$output --method=R1 --container=docker \
    --b=1.7 --c=400 --i=2 --filter=quantile --threshold=1 --post=discard --smallest=3 --largest=100 --b2=1.7 --c2=500 --i2=2 \
    > $output/console_output.txt 2>&1
  checkOutput
fi

echo "ERROR: neither Docker nor Singularity appear to be installed" > /tmp/monet_quick_test/output.txt
exit 1
