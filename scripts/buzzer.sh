#!/bin/bash

BUZZER=0
gpio mode BUZZER out
gpio write BUZZER 0
if [ ! -f /mnt/ramdisk/beep ]; then
	echo "0" > /mnt/ramdisk/beep
fi

while [ 1 ]
do
	sleep_time=$(cat /mnt/ramdisk/beep)
	echo $sleep_time
	if [ $sleep_time -gt 0 ]
	then
		echo "On"
		gpio write BUZZER 1
		sleep 0.1
		echo "off"
		gpio write BUZZER 0
		sleep $sleep_time
	else
		echo "no sound"
		gpio write BUZZER 0
		sleep 2.5
	fi

done

