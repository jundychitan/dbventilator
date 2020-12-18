#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import print_function
import smbus
import time
import sys
from timeit import default_timer as timer

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


def map_value(x, in_min, in_max, out_min, out_max):
    return float((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def kpa_cmh2o(kpa):
	return kpa*10.197162129779

def main():
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    OXYGEN = AnalogIn(ads, ADS.P0)
    PRESSURE = AnalogIn(ads, ADS.P1)
    INHILATION = AnalogIn(ads, ADS.P2)
    BATTERY = AnalogIn(ads, ADS.P3)
    
    #ad_address = 0x48
    # A0 = 0x40
    # A1 = 0x41
    # A2 = 0x42
    # A3 = 0x43

    #fletch's setup
    # OXYGEN=0
    # PRESSURE=1 #ok
    # INHILATION=2
    # BATTERY=3 #ok

    #OXYGEN=A0
    #PRESSURE=A1
    #INHILATION=A2
    #BATTERY=A3

    #jun's setup
    #OXYGEN=A2
    #PRESSURE=A1
    #INHILATION=A0
    #BATTERY=A3

    flow_address=0x49
    bus = smbus.SMBus(1)
    sampling_time = 0
    start = time.time()
    vt = 0
    slpm = 0
    inhilation = 0
    pressure = 0
    oxygen = 0
    battery = 0
    prev_slpm = 0
    
    channel = 2
    gain = 1	
    while True:
        #read honeywell sensor
        try:
            flow = bus.read_byte(flow_address)<<8 | bus.read_byte(flow_address)
            slpm = 50 * ((flow / 16384.0) - 0.1) / 0.8;
            f = open("/mnt/ramdisk/flow.txt","w")
            f.write("%1.3f" %(slpm))
            f.close()
            sampling_time = (time.time()-start)*1000.0
            start = time.time()
            if slpm<0:slpm=0
            if slpm>0:
                vt += ((slpm / 60) / (1 / (sampling_time / 1000.0))) * 1000;
            else:
                vt = 0
            f = open("/mnt/ramdisk/volume.txt","w")
            f.write("%1.3f" %(vt))
            f.close()
            
        except:
            f = open("error.txt","w")
            f.write("%1.3f\r\n" %(slpm))
            f.close()
            print("ERROR")
            pass
            
        inhilation=INHILATION.voltage
        if inhilation<0.5:inhilation=0.5
        inhilation = map_value(inhilation, 0.5, 4.5, -2.0, 2.0)
        f = open("/mnt/ramdisk/inhilation.txt","w")
        f.write("%1.3f" %(inhilation))
        f.close()
        	
        pressure=PRESSURE.voltage
        if pressure<0.5:
            pressure=0.5
        pressure = map_value(pressure, 0.5, 4.5, 0, 5)
        pressure = kpa_cmh2o(pressure)
        f = open("/mnt/ramdisk/pressure.txt","w")
        f.write("%1.3f" %(pressure))
        f.close()
        
        oxygen=OXYGEN.voltage
        f = open("/mnt/ramdisk/oxygen.txt","w")
        f.write("%1.3f" %(oxygen))
        f.close()
        
        battery=BATTERY.voltage
        battery = map_value(battery, 0, 4.1, 0, 13.47)
        f = open("/mnt/ramdisk/battery.txt","w")
        f.write("%1.3f" %(battery))
        f.close()
        
        print("Values: SLPM: %1.3f, INH %1.3f, PRES %1.3f, OXY %1.3f, BATT %1.3f, VT %1.3f " %(slpm,inhilation,pressure,oxygen,battery, vt))
        #sys.stdout.flush()
        #print("Values: SLPM: %1.3f, INH %1.3f" %(slpm,inhilation))
        time.sleep(0.1)
		
		
if __name__ == "__main__":
    main()		
