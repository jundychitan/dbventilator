#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import print_function
import serial
import time
import sys
from timeit import default_timer as timer

file_path="/mnt/ramdisk/inhilation.txt"
target_value=0.1

def get_value():
	try:
		f=open(file_path,"r")
		value=float(f.read())
		f.close()
		return value
	except:
		return 0

def get_mode():
	try:
		f=open("/home/pi/dec-rpi-gui/temp/mode.txt","r")
		value=f.read()
		f.close()
		return value
	except:
		return "assist"
		
def main():
    while True:
        if get_mode() ==  "assist":
            value=get_value()
            print("value %1.3f" %(value))
            if value>target_value:
                print("Assist mode")
                ser=serial.Serial(port='/dev/ttyS0',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
                ser.write("1\r")
                ser.close()
                time.sleep(1)
            else:
                time.sleep (0.2)
	else:
		time.sleep (1)
			
if __name__ == "__main__":
    main()	

