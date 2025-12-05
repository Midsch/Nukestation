#!/bin/bash
#echo =============================
#echo force nwipe writing progress



#nwipePID=$(ps -ax | grep -i 'sudo nwipe' | grep -i 'autonuke' | grep 'nogui' | awk '{print $1}')
nwipePID=$(ps -ax \
  | grep -i 'nwipe' \
  | grep -i 'autonuke' \
  | grep -i 'nogui' \
  | grep -v 'grep' \
  | awk '{printf "%s ", $1} END {print ""}')
#echo $nwipePID
#sudo kill -SIGUSR1 $nwipePID


if [ -n "$nwipePID" ]
then
        #echo process found with following pids: $nwipePID
        kill -SIGUSR1 $nwipePID
        #sudo kill -SIGUSR1 $(ps -ax | grep -i 'sudo nwipe' | grep -i 'autonuke' | grep 'nogui' | awk '{print $1}')
#else
        #echo "process not found"
fi

