#! /bin/bash -
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


# clean results from previous runs
monitor_ram_script=$PWD/src/monitor_ram.sh
chmod +x $monitor_ram_script
stats_output="$PWD/output/__resource_usage/"
rm -rf $stats_output && mkdir $stats_output
stats_output_file="$stats_output"benchmark_resource_usage.tsv
printf "method\ttime\tmax_RAM\tmean_RAM\n" >> $stats_output_file


start_resource_monitor () {
  ram_output="/tmp/monet_benchmark_test/"
  rm -rf $ram_output && mkdir $ram_output
  # take initial timestamp
  begin=$(date +%s)
  timestamp=`date '+%Y-%m-%d-%H%M%S'`
  # start monitoring RAM
  screen -dmS measureRAM sh -c "$monitor_ram_script > "$ram_output"ramusage.tsv"
}
stop_resource_monitor () {
  method=$1
  printf "$method\t" >> $stats_output_file
  # calculate time usage
  end=$(date +%s) # calculate execution time
  tottime=$(expr $end - $begin)
  printf "$tottime\t" >> $stats_output_file
  # calculate RAM usage
  screen -S measureRAM -X quit # kill RAM monitoring script
  base_RAM=$( cat "$ram_output"ramusage.tsv | awk '{if(min==""){min=max=$1}; if($1>max) {max=$1}; if($1<min) {min=$1}; total+=$1; count+=1} END {print min}')
  max_RAM=$( cat "$ram_output"ramusage.tsv | awk '{if(min==""){min=max=$1}; if($1>max) {max=$1}; if($1<min) {min=$1}; total+=$1; count+=1} END {print max}')
  max_RAM=$(($max_RAM-$base_RAM))
  mean_RAM=$( cat "$ram_output"ramusage.tsv | awk '{if(min==""){min=max=$1}; if($1>max) {max=$1}; if($1<min) {min=$1}; total+=$1; count+=1} END {print total/count}')
  mean_RAM=${mean_RAM%.*}
  mean_RAM=$(($mean_RAM-$base_RAM))
  printf "$max_RAM\t$mean_RAM\n" >> $stats_output_file
}


cd input
base=$(pwd)

for dir in */; do
  cd $dir
  chmod +x *.sh

  start_resource_monitor
  ./run_monet_R1.sh
  stop_resource_monitor "R1"

  service docker restart
  sleep 30
  find  ~/.monet -name "core.*" -delete # clean any core dumps

  start_resource_monitor
  ./run_monet_M1.sh
  stop_resource_monitor "M1"

  service docker restart
  sleep 30
  find  ~/.monet -name "core.*" -delete 

  start_resource_monitor
  ./run_monet_K1.sh
  stop_resource_monitor "K1"

  service docker restart
  sleep 30
  find  ~/.monet -name "core.*" -delete 

  cd $base
  
done
