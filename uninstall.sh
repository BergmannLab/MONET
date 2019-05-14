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
echo "Uninstalling the DREAM_DMI TOOL"
echo 

# ask for root password (needed to remove /usr/local/bin/monet)
echo "Superuser rights are required."
sudo ls > /dev/null
echo


sudo rm -f /usr/local/bin/monet
rm -rf ~/.monet
echo FINISHED: monet was UNINSTALLED SUCCESSFULLY.
echo
