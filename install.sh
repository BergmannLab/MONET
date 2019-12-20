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
echo "MONET: MOdularising NEtwork Toolbox"
echo "       for mining of molecular and genetic networks"
echo

user_home=$HOME
username=$(whoami)

# check whether monet is already installed
if [ -d $user_home/.monet ]; then
  read -p "MONET is already installed. Would you like to overwrite? [y|n] " -n 1 -r
  echo ""
  if [[ $REPLY =~ ^[y]$ ]]; then
    ./uninstall.sh > /dev/null 2>&1
  elif [[ $REPLY =~ ^[n]$ ]]; then
    echo "EXITING: MONET WAS NOT RE-INSTALLED."
    exit 0
  else
    echo "invalid option selected"
    echo "EXITING: MONET WAS NOT RE-INSTALLED."
    exit 0
  fi  
fi

# check that either docker or singularity are installed
echo "- Are docker or singularity installed?..."
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
  echo "  ...YES"
fi

# store monet code in the home directory
echo "- Copying files..."
mkdir $user_home/.monet
cp -r ./* $user_home/.monet
chmod -R 750 $user_home/.monet
echo "  ...DONE"

function add_to_path {
# make monet command available: add location where monet will be installed to $PATH
case ":$PATH:" in
  *"monet"*)
    # already in path due to previous installation, nothing to do
    echo "" && echo "SUCCESS: installation completed."
    ;;
  *)
    # add to bashrc
    echo ""; echo export PATH=\"'$PATH':$HOME/.monet\" >>  $user_home/.bashrc
    # add to bash_profile (this is necessary on macOS)
    echo ""; echo export PATH=\"'$PATH':$HOME/.monet\" >>  $user_home/.bash_profile
    ;;
esac
}

# in the case of Singularity users, the images need to be built by root
if ! $docker_installed && $singularity_installed; then
  echo ""
  echo "It appears only Singularity is intalled on this system."
  echo "To complete the installation, you need SUPERUSER rights and INTERNET access."
  read -p "Do you want to proceeed? [y|n] " -n 1 -r
  echo " " && echo "Please wait while the Singularity containers are being built"
  echo "(this takes a few minutes)" 
  if [[ $REPLY =~ ^[y]$ ]]
    then
      # I could alternatively su root, but this does not work on Debian
      cd $user_home/.monet/containers/K1/singularity
      sudo singularity build ./K1-image.img Singularity
      cd $user_home/.monet/containers/M1/singularity
      sudo singularity build ./M1-image.img Singularity
      cd $user_home/.monet/containers/R1/singularity
      sudo singularity build ./R1-image.img Singularity
      chmod -R 750 $user_home/.monet
    else
      echo " "
      echo "The installation will need to be completed, manually, at a later stage."
      echo "Please contact mattia.tomasoni@unil.ch and ask for support."  
      add_to_path
      exit 0
  fi
fi

# (optionally) test the installation
echo ""
read -p "Would you like to test the installation? (takes a few mins) [y|n] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[y]$ ]]
then
echo "- Testing, thank you for waiting... "
  cd $user_home/.monet/test/system_test && ./quick_test.sh > /dev/null 2>&1 && cd ..
  if [ $? -gt "0" ]; then
    echo "  ERROR: see /tmp/monet_quick_test/console_output.txt"
    echo "" && echo "ABORTING: monet WAS NOT INSTALLED."
    exit 1
  else
    echo "  ...OK"
  fi  
fi

add_to_path

echo ""
echo "SUCCESS: please provide your password to finalize the installation."
echo "You are being REDIRECTED TO YOUR HOME DIRECTORY"
echo "INVOKE monet FROM ANY LOCATION"
su - $username #re-login and execute the profile script to make monet command available


