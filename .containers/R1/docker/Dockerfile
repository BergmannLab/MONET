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
# This file allows you to build a Docker image that can run the method of
# one of the top performing teams: Team Causality
###############################################################################

FROM ubuntu
LABEL maintainer="Mattia Tomasoni <mattia.tomasoni@unil.ch>"

###############################################################################
# set time zone (prevent interactive prompt which would break build)
RUN apt-get update && \ 
 export DEBIAN_FRONTEND=noninteractive && \
 apt-get install -y tzdata && \
 ln -fs /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime && \
 dpkg-reconfigure --frontend noninteractive tzdata

###############################################################################
# install R and required libraries

RUN apt-get -y install r-base

RUN apt-get -y install r-cran-igraph

###############################################################################
# run method

ENTRYPOINT ["/bin/bash", "/R1_code/runCausality.sh"]
