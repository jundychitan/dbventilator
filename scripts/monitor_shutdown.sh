#!/bin/bash
serial_port="/dev/ttyS0"

filename=/home/pi/dbventilator/dec-rpi-gui/temp/power.txt
while inotifywait -q -e modify $filename >/dev/null; 
do 
    echo "filename is changed" 
    echo "">$filename
    operation=$(cat /home/pi/dbventilator/dec-rpi-gui/temp/process_control.txt)
    echo $operation
    if [ "$operation" == "off" ]; then
        echo "shutdown"
        echo -e "0\r" > $serial_port
        echo -n "assist" >/home/pi/dbventilator/dec-rpi-gui/temp/mode.txt
        sudo halt
    else
        echo "no shutdown"
    fi
done
