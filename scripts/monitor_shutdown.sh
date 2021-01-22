#!/bin/bash

gpio_com=/usr/bin/gpio

BUZZER=0
$gpio_com mode BUZZER out
$gpio_com write BUZZER 0

shutdown_port=0
$gpio_com mode $shutdown_port up

port_status=1

while [ $port_status -eq 1 ]
do
	port_status=$($gpio_com read $shutdown_port)
	sleep 1
	echo "power on"
done
$gpio_com write BUZZER 1
echo "Shutdown"
sudo halt


