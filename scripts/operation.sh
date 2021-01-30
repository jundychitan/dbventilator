#!/bin/bash
serial_port="/dev/ttyS0"
project_dir=/home/pi/dbventilator/dec-rpi-gui/temp
config_file=process_control.txt
tidal_volume_file=tidal_volume.txt
resp_rate_file=resp_rate.txt
ie_ratio_file=ie_ratio.txt 
mode_file=mode.txt 
max_tv=500

timestamp(){
	date +"%Y-%m-%d %H:%M:%S"
}
filename=$project_dir/$config_file
while inotifywait -q -e modify $filename >/dev/null;
do
	#echo "file changed"
	status=$(cat $filename)
	#echo $status
	if [ "$status" == "on" ];then
		echo "Status ON"
		actual_tv=$(cat $project_dir/$tidal_volume_file)
		if [ $actual_tv -ge $max_tv ]; then
			percent_tv=100
		else
			percent_tv=$((actual_tv*100/$max_tv))
		fi
		echo "percent volume " $percent_tv 
		
		command=$percent_tv,$(cat $project_dir/$resp_rate_file),$(cat $project_dir/$ie_ratio_file)
		echo $command
		echo -e "$command\r" > $serial_port
		sleep 0.5
		#check if assist mode or control mode
		mode=$(cat $project_dir/$mode_file)
		if [ "$mode" == "assist" ]; then
			echo "Assist mode"
			echo -e "1\r" > $serial_port
		else
			echo "Control mode"
			echo -e "2\r" > $serial_port	
		fi
	else
		echo "Status OFF"
		echo -e "0\r" > $serial_port	
		echo "0,255,0" > $project_dir/alarm_color.txt
		echo -n "STOPPED" > $project_dir/alarm_status.txt
		echo -n "0" > /mnt/ramdisk/beep #silence alarm when stopped
	fi
done
