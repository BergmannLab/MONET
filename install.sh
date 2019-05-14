#! /bin/bash -

# Copyright 2018 Bergmann's Lab UNIL <mattia.tomasoni@unil.ch>
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

echo 
echo "Installing the DREAM_DMI TOOL"
echo "Disease module identification algorithms"
echo "top performers from the 2017 DREAM CHALLENGE"
echo

# ask for root password (needed to make dream_dmi command available from all
# locations by adding link in /usr/local/bin/dream_dmi)
echo "Superuser rights are required."
sudo ls > /dev/null
echo

# check whether dream_dmi is already installed
if [ -f /usr/local/bin/dream_dmi ]; then
  read -p "dream_dmi is already installed. Would you like to overwrite? [y|n] " -n 1 -r
  echo ""
  if [[ $REPLY =~ ^[y]$ ]]; then
    ./uninstall.sh > /dev/null 2>&1
  elif [[ $REPLY =~ ^[n]$ ]]; then
    echo "EXITING: dream_dmi WAS NOT RE-INSTALLED."
    exit 0
  else
    echo "invalid option selected"
    echo "EXITING: dream_dmi WAS NOT RE-INSTALLED."
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
  echo "    Install either of the two to successfully run dream_dmi."
  echo "    Please visit https://www.docker.com or http://singularity.lbl.gov"
  echo "" && echo "ABORTING: dream_dmi WAS NOT INSTALLED."
  exit 1
else
  echo "  ...OK"
fi

# store dream_dmi code in the home directory
echo "- Copying files..."
mkdir ~/.dream_dmi_tool
cp -r ./* ~/.dream_dmi_tool
chmod -R 750 ~/.dream_dmi_tool
echo "  ...OK"

# make dream_dmi command available
echo "- Updating operating system..."
sudo ln -s ~/.dream_dmi_tool/dream_dmi /usr/local/bin/dream_dmi 
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
    echo "  ERROR: see /tmp/dream_dmi_quick_test/console_output.txt"
    echo "" && echo "ABORTING: dream_dmi WAS NOT INSTALLED."
    exit 1
  else
    echo "  ...OK"
  fi  
fi

echo "" && echo "FINISHED: dream_dmi WAS INSTALLED SUCCESSFULLY."
echo "Invoke dream_dmi in a bash shell from any location."
echo 

# reload current shell so changes to ~/.bashrc will become available
exec bash
