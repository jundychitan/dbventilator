#!/bin/bash

gpio_com=/usr/bin/gpio

BUZZER=0
$gpio_com mode BUZZER out
$gpio_com write BUZZER 0

shutdown_port=7
$gpio_com mode $shutdown_port in
$gpio_com mode $shutdown_port up

port_status=1
while [ 1 ]
do
    while [ $port_status -eq 1 ]
    do
    	port_status=$($gpio_com read $shutdown_port)
    	sleep 1
    	echo "power on"
    done
    $gpio_com write BUZZER 0
    echo -n "HALT" >/home/pi/dbventilator/dec-rpi-gui/temp/alarm_status.txt
    echo "halt pressed"
    #sudo halt
    while [ $port_status -eq 0 ]
    do
        port_status=$($gpio_com read $shutdown_port)
        sleep 1        
    done    
    echo "halt released"
done

