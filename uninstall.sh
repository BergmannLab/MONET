#! /bin/bash -
# Copyright 2018 Bergmann's Lab UNIL <mattia.tomasoni@unil.ch>
#
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
echo "Uninstalling MONET"
echo

user_home=$HOME

if [ ! -d $user_home/.monet ]; then
  echo "MONET is not installed on the system. Nothing to do."
  echo "FINISHED"
  exit 1
fi

remove_docker_images(){
  docker --help > /tmp/docker_test 2>&1 # is docker installed?
  if [ $? -eq "0" ]; then docker_installed=true; else docker_installed=false; fi
  if $docker_installed; then
    rm -f /tmp/docker_rmi
    sudo docker rm K1-container >> /tmp/docker_rmi 2>&1
    sudo docker rmi k1-image >> /tmp/docker_rmi 2>&1
    sudo docker rm M1-container >> /tmp/docker_rmi 2>&1
    sudo docker rmi m1-image >> /tmp/docker_rmi 2>&1
    sudo docker rm R1-container >> /tmp/docker_rmi 2>&1
    sudo docker rmi r1-image >> /tmp/docker_rmi 2>&1
    echo "- Docker images were removed (see /tmp/docker_rmi for details)"
  fi
}

remove_singularity_images(){
  singularity --help > /tmp/singularity_test 2>&1 # is singularity installed?
  if [ $? -eq "0" ]; then singularity_installed=true; else singularity_installed=false; fi
  if $singularity_installed; then
    rm -f /tmp/singularity_rmi
    # the whole .monet folder will later be removed; keeping this for consistency/clarity 
    rm $user_home/.monet/containers/K1/singularity/K1-image.img >> /tmp/singularity_rmi 2>&1
    rm $user_home/.monet/containers/K1/singularity/M1-image.img >> /tmp/singularity_rmi 2>&1
    rm $user_home/.monet/containers/K1/singularity/R1-image.img >> /tmp/singularity_rmi 2>&1
    echo "- Singularity images were removed (see /tmp/singularity_rmi for details)"
  fi
}

# optionally remove virtualization images
# (if they had been created by running the corresponding method)
read -p "Would you like to remove Docker/Singularity images/containers? [y|n] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[y]$ ]]; then
  remove_docker_images
  remove_singularity_images
  echo ""
elif [[ $REPLY =~ ^[n]$ ]]; then
  echo "Docker images/containers were not removed."
  echo ""
else
  echo ""
  echo "ERROR: invalid option selected."
  echo "EXITING: MONET WAS NOT UNINSTALLED."
  exit 0
fi


# remove MONET installation folder
rm -rf ~/.monet

echo FINISHED: MONET was UNINSTALLED SUCCESSFULLY.
echo
