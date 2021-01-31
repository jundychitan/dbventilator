#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import print_function
import serial
import time
import sys
from timeit import default_timer as timer

import RPi.GPIO as GPIO

file_path="/mnt/ramdisk/inhilation.txt"
target_value=1.8

def get_value():
	try:
		f=open(file_path,"r")
		value=float(f.read())
		f.close()
		print(value)
		return value
	except:
		return 0

def get_mode():
	try:
		f=open("/home/pi/dbventilator/dec-rpi-gui/temp/mode.txt","r")
		value=f.read()
		f.close()
		return value
	except:
		return "assist"
        
def get_operation():
	try:
		f=open("/home/pi/dbventilator/dec-rpi-gui/temp/process_control.txt","r")
		value=f.read()
		f.close()
		return value
	except:
		return "off"       

def get_limit():
    try:
        #f=open("/mnt/ramdisk/assist_pressure.txt","r")
        f=open("/home/pi/dbventilator/dec-rpi-gui/temp/assist_pressure.txt","r")
        value=float(f.read())
        f.close()
        return value
    except:
        return target_value    
		
def main():
    #configure GPIO
    GPIO.setmode(GPIO.BCM)  
    GPIO.setup(22, GPIO.OUT) 
    GPIO.output(22, GPIO.LOW)
    while True:
        if get_mode() ==  "assist" and get_operation() == "on":
            value=get_value()
            limit=get_limit()
            print("value %1.3f" %(value))
            print("limit %1.3f" %(limit))
            if value>limit:
                print("Assist mode")
                GPIO.output(22, GPIO.HIGH)                
                time.sleep(0.2)
                GPIO.output(22, GPIO.LOW)
                # ser=serial.Serial(port='/dev/ttyS0',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
                # ser.write("1\r")
                # ser.close()
                # time.sleep(1)

            else:
                time.sleep (0.2)
        else:
		time.sleep (1)

if __name__ == "__main__":
    main()	

