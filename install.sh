#! /bin/bash -

# Copyright 2018 Bergmann's Lab UNIL <mattia.tomasoni@unil.ch>
# This file is part of MONET.
#
#    MONET is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MONET is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MONET. If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################
# Mattia Tomasoni - UNIL, CBG
# 2017 DREAM challenge on Disease Module Identification
# https://www.synapse.org/modulechallenge
###############################################################################

echo 
echo "Installing the DREAM_DMI TOOL"
echo "Disease module identification algorithms"
echo "top performers from the 2017 DREAM CHALLENGE"
echo

# ask for root password (needed to make monet command available from all
# locations by adding link in /usr/local/bin/monet)
echo "Superuser rights are required."
sudo ls > /dev/null
echo

# check whether monet is already installed
if [ -f /usr/local/bin/monet ]; then
  read -p "monet is already installed. Would you like to overwrite? [y|n] " -n 1 -r
  echo ""
  if [[ $REPLY =~ ^[y]$ ]]; then
    ./uninstall.sh > /dev/null 2>&1
  elif [[ $REPLY =~ ^[n]$ ]]; then
    echo "EXITING: monet WAS NOT RE-INSTALLED."
    exit 0
  else
    echo "invalid option selected"
    echo "EXITING: monet WAS NOT RE-INSTALLED."
    exit 0
  fi  
fi

# check that either docker or singularity are installed
echo "- Checking that docker and/or singularity are installed..."
docker --help > /tmp/docker_test 2>&1
if [ $? -eq "0" ]; then docker_installed=true; else docker_installed=false; fi
singularity --help > /tmp/singularity_test 2>&1
if [ $? -eq "0" ]; then singularity_installed=true; else singularity_installed=false; fi

if ! $docker_installed && ! $singularity_installed; then
  echo "  ERROR: Neither docker nor singularity are installed."
  echo "    Install either of the two to successfully run monet."
  echo "    Please visit https://www.docker.com or http://singularity.lbl.gov"
  echo "" && echo "ABORTING: monet WAS NOT INSTALLED."
  exit 1
else
  echo "  ...OK"
fi

# store monet code in the home directory
echo "- Copying files..."
mkdir ~/.monet
cp -r ./* ~/.monet
chmod -R 750 ~/.monet
echo "  ...OK"

# make monet command available
echo "- Updating operating system..."
sudo ln -s ~/.monet_tool/monet /usr/local/bin/monet 
echo "  ...OK"

# (optionally) test the installation
echo ""
read -p "Would you like to test the installation? (take a few mins) [y|n] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[y]$ ]]
then
echo "- Testing, thank you for waiting... "
  cd test/system_test && ./quick_test.sh > /dev/null 2>&1 && cd ..
  if [ $? -gt "0" ]; then
    echo "  ERROR: see /tmp/monet_quick_test/console_output.txt"
    echo "" && echo "ABORTING: monet WAS NOT INSTALLED."
    exit 1
  else
    echo "  ...OK"
  fi  
fi

echo "" && echo "FINISHED: monet WAS INSTALLED SUCCESSFULLY."
echo "Invoke monet in a bash shell from any location."
echo 

# reload current shell so changes to ~/.bashrc will become available
exec bash
