#!/bin/sh -

echo "Minitoring RAM usage (MB) for user:" $USER
echo " "
while true; do
    ps -U $USER --no-headers -o rss | awk '{ sum+=$1} END {print int(sum/1024)}'
    sleep 1
done
