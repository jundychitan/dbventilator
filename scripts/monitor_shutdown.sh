#!/bin/bash

gpio_com=/usr/bin/gpio

shutdown_port=7
/usr/bin/gpio mode $shutdown_port in

port_status=1

while [ $port_status -eq 1 ]
do
	port_status=$(/usr/bin/gpio read $shutdown_port)
	sleep 1
	echo "power on"
done

echo "Shutdown"
sudo halt


