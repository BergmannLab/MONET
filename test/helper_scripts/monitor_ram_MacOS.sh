#!/bin/sh -

while true; do
	top -l 1 | grep -E "^Phys" 
        sleep 5
done
