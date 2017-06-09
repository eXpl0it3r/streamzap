#!/bin/sh
cd /home/fitpc/Dokumente/streamzap
pip uninstall .
pip install .
clear
while(true)
do
	streamzap
	echo "I'm going to sleep for a minute"
	sleep 60
done
