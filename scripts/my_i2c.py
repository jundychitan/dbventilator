#!/usr/bin/python3
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

import RPi.GPIO as GPIO

def limits_directory():
    return '/home/pi/dbventilator/scripts/limits/'

def alt_limits_directory():
    return '/home/pi/dbventilator/dec-rpi-gui/temp/'    

def working_directory():
    return '/home/pi/dbventilator/scripts/'

def gui_directory():
    return '/home/pi/dbventilator/dec-rpi-gui/temp/'

def realtime_directory():
    return '/mnt/ramdisk/'
    
def pressure_hi_lim_filename():
    return 'pressure_peak.txt'
    
def pressure_lo_lim_filename():
    return 'pressure_lo_lim.txt'    
    
def peep_hi_lim_filename():
    return 'peep.txt' 

def peep_lo_lim_filename():
    return 'peep.txt'     

def o2_lim_filename():
    return 'fio2.txt'

def get_red():
    return '255,0,0'

def get_green():
    return '0,255,0'

def get_yellow():
    return '255,255,0'
    
def get_black():
    return '0,0,0'

def get_ac_detect():
    return 17 #physical pin 7 (uses BCM gpio pin numbering)

def get_process_control():
    try:
        f=open(gui_directory()+"process_control.txt","r")
        value=f.read()
        f.close()
        return value 
    except:
        return "off"

def get_pressure_hi_lim():
    try:
        f=open(alt_limits_directory()+pressure_hi_lim_filename(),"r")
        value=float(f.read())
        f.close()
        return value
    except:
        print("get pressure limit error")
        value=40.0
        f=open(limits_directory()+pressure_hi_lim_filename(),"w")
        f.write("%0.1f" %(value))
        f.close()
        return value

def get_pressure_lo_lim():
    try:
        f=open(limits_directory()+pressure_lo_lim_filename(),"r")
        value=float(f.read())
        f.close()
        return value
    except:
        value=5
        f=open(limits_directory()+pressure_lo_lim_filename(),"w")
        f.write("%0.1f" %(value))
        f.close()
        return value        

def get_peep_hi_lim():
    try:
        f=open(alt_limits_directory()+peep_hi_lim_filename(),"r")
        value=float(f.read())
        value = value + 2.5
        f.close()
        return value
    except:
        value=10
        f=open(alt_limits_directory()+peep_hi_lim_filename(),"w")
        f.write("%0.1f" %(value))
        f.close()
        return value           

def get_peep_lo_lim():
    try:
        f=open(alt_limits_directory()+peep_lo_lim_filename(),"r")
        value=float(f.read())
        value = value - 2.5
        f.close()
        return value
    except:
        value=1
        f=open(alt_limits_directory()+peep_lo_lim_filename(),"w")
        f.write("%0.1f" %(value))
        f.close()
        return value    

def get_o2_lo_limit():
    try:
        f=open(alt_limits_directory()+o2_lim_filename(),"r")
        value=float(f.read())
        value =  - 10
        f.close()
        return value
    except:
        value=16.8
        f=open(alt_limits_directory()+o2_lim_filename(),"w")
        f.write("%0.1f" %(value))
        f.close()
        return value 

def get_o2_hi_limit():
    try:
        f=open(alt_limits_directory()+o2_lim_filename(),"r")
        value=float(f.read())
        value = value + 10
        f.close()
        return value
    except:
        value=25.2
        f=open(alt_limits_directory()+o2_lim_filename(),"w")
        f.write("%0.1f" %(value))
        f.close()
        return value                       
    
def get_volume_hi_lim():
    try:
        f=open(limits_directory()+"get_volume_hi_lim","r")
        value=float(f.read())
        f.close()
        return value
    except:
        value=800
        f=open(limits_directory()+"get_volume_hi_lim","w")
        f.write("%0.1f" %(value))
        f.close()
        return value                

def get_volume_lo_lim():
    try:
        f=open(limits_directory()+"get_volume_lo_lim","r")
        value=float(f.read())
        f.close()
        return value
    except:
        value=10
        f=open(limits_directory()+"get_volume_lo_lim","w")
        f.write("%0.1f" %(value))
        f.close()
        return value           

def get_battery_50pcnt():
    try:
        f=open(limits_directory()+"get_battery_50pcnt","r")
        value=float(f.read())
        f.close()
        return value
    except:
        value=12
        f=open(limits_directory()+"get_battery_50pcnt","w")
        f.write("%0.1f" %(value))
        f.close()
        return value     

def get_battery_20pcnt():
    try:
        f=open(limits_directory()+"get_battery_20pcnt","r")
        value=float(f.read())
        f.close()
        return value
    except:
        value=11.5
        f=open(limits_directory()+"get_battery_20pcnt","w")
        f.write("%0.1f" %(value))
        f.close()
        return value           

def get_bpm():
    try:
        f=open(alt_limits_directory()+"resp_rate.txt", "r")
        value=int(f.read())
        f.close()
        return value
    except:
        value=12

def get_tv():
    try:
        f=open(alt_limits_directory()+"tidal_volume.txt", "r")
        value=int(f.read())
        f.close()
        return value
    except:
        value=600
    
def map_value(x, in_min, in_max, out_min, out_max):
    return float((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def kpa_cmh2o(kpa):
	return kpa*10.197162129779

def main():
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    OXYGEN = AnalogIn(ads, ADS.P3)
    PRESSURE = AnalogIn(ads, ADS.P1)
    INHILATION = AnalogIn(ads, ADS.P0)
    BATTERY = AnalogIn(ads, ADS.P2)
    
    flow_address=0x49
    bus = smbus.SMBus(1)
    sampling_time = 100
    prev_sampling_time = 100
    start = time.time()

    inhilation_start = False
    exhilation_start = False

    start_inhilation_time = time.time()
    end_inhilation_time = time.time()
    total_inhilation_time = 0
    start_exhilation_time = time.time()
    end_exhilation_time = time.time()
    total_exhilation_time = 0

    battery_wait = time.time()
    ac_wait = time.time()
    #other_alarm = False
    batt_alarm = False
    main_alarm = False

    vt = 0
    vt_total = [0]
    slpm = 0
    inhilation = 0
    pressure = 0
    oxygen = 0
    oxygen_array = [21]
    battery = 0
    prev_slpm = 0
    peep_pressure = 0
    peep_counter = 0
    max_pressure = 0
    max_flow = 0
    max_volume = 0
    pressure_range = tuple()
    flow_range = tuple()
    volume_range = tuple()
    channel = 2
    gain = 1	

    bpm = 0
    prev_bpm = 0

    tidal_volume = 0
    prev_tidal_volume = 0
    total_volume = 0

    run_once = False

    f = open(realtime_directory()+'pressure_peak.txt','w')
    f.write("0")
    f.close()

    f = open(realtime_directory()+'volume_peak.txt','w')
    f.write("0")
    f.close()

    f = open(realtime_directory()+'flow_peak.txt','w')
    f.write("0")
    f.close()

    f = open(realtime_directory()+'max_peep.txt','w')
    f.write("0")
    f.close()  

    #configure GPIO
    GPIO.setmode(GPIO.BCM)  
    #GPIO.setup(get_ac_detect(), GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

    while True:
        inhilation=INHILATION.voltage
        #print("inhilation %0.2f" %(inhilation))
        if inhilation<0.5:inhilation=0.5
        inhilation = map_value(inhilation, 0.5, 4.5, -2.0, 2.0)
        inhilation = kpa_cmh2o(inhilation)
        #print("inhilation %0.2f" %(inhilation))

        f = open("/mnt/ramdisk/inhilation.txt","w")
        f.write("%1.3f" %(inhilation))
        f.close()
            
        pressure=PRESSURE.voltage
        if pressure<0.5:
            pressure=0.5
        pressure = map_value(pressure, 0.5, 4.5, 0, 5)
        pressure = kpa_cmh2o(pressure)
        pressure_range = pressure_range + (pressure,)
        f = open(realtime_directory()+"pressure.txt","w")
        f.write("%1.3f" %(pressure))
        f.close()
        
        oxygen=OXYGEN.voltage * 100

        if len(oxygen_array)>100:
        	oxygen_array.pop(0)
        	oxygen_array+=[oxygen]
        else:
        	oxygen_array+=[oxygen]

        oxygen=(sum(oxygen_array)/len(oxygen_array))
        #print ("Oxygen %0.2f" %(oxygen))

        oxygen=map_value(oxygen, 0.5, 6.9, 21.0, 100.0)
        
        if oxygen>100:
            oxygen=100.0

        if oxygen<21:
        	oxygen=21.0

        f = open(realtime_directory()+"oxygen.txt","w")
        f.write("%1.1f" %(oxygen))
        f.close()
        
        battery=BATTERY.voltage
        battery = map_value(battery, 0, 4.1, 0, 13.47)
        f = open(realtime_directory()+"battery.txt","w")
        f.write("%1.3f" %(battery))
        f.close()

        if time.time()-battery_wait>5:
            #print("battery: %0.1f" %(battery))
            battery_wait=time.time()
            if battery < get_battery_50pcnt() and battery > get_battery_20pcnt():
                #battery is less than 50%
                batt_alarm = True
                print("battery less than 50%")
                f=open(gui_directory()+'power_source.txt','w')
                f.write("BATT <50%")
                f.close()  

                f=open(gui_directory()+'power_source_color.txt','w')
                f.write("%s" %(get_red()))
                f.close()    

                f = open(realtime_directory()+'beep','w')
                f.write("5")
                f.close()

            elif battery < get_battery_20pcnt():
                #battery is less than 20%
                batt_alarm = True
                print("battery less than 20%")
                f=open(gui_directory()+'power_source.txt','w')
                f.write("BATT <20%")
                f.close()  

                f=open(gui_directory()+'power_source_color.txt','w')
                f.write("%s" %(get_red()))
                f.close()    

                f = open(realtime_directory()+'beep','w')
                f.write("1")
                f.close()

            else:
                if batt_alarm == True:
                    batt_alarm = False
                    print("Normal")
                    f=open(gui_directory()+'power_source.txt','w')
                    f.write("BATTERY")
                    f.close()  

                    f=open(gui_directory()+'power_source_color.txt','w')
                    f.write("%s" %(get_black()))
                    f.close()   

                    f = open(realtime_directory()+'beep','w')
                    f.write("0")
                    f.close()

        if time.time() - ac_wait > 2:
            ac_wait = time.time()
            #if GPIO.input(get_ac_detect()) == 0:
            if GPIO.input(17) == 0:    
                print("ac disconnected")
                if batt_alarm == False:
                    #other_alarm = True
                    print("AC Loss")
                    f=open(gui_directory()+'power_source.txt','w')
                    f.write("BATTERY")
                    f.close()  

                    f=open(gui_directory()+'power_source_color.txt','w')
                    f.write("%s" %(get_black()))
                    f.close()    

                    #f = open(realtime_directory()+'beep','w')
                    #f.write("1")
                    #f.close()        
            else:
                #other_alarm = False
                #print("Normal")
                f=open(gui_directory()+'power_source.txt','w')
                f.write("NORMAL")
                f.close()  

                f=open(gui_directory()+'power_source_color.txt','w')
                f.write("%s" %(get_black()))
                f.close()   

                #f = open(realtime_directory()+'beep','w')
                #f.write("0")
                #f.close()


        #read honeywell sensor
        try:
            sampling_time = (time.time()-start)*1000.0
            start = time.time()

            flow = bus.read_byte(flow_address)<<8 | bus.read_byte(flow_address)
            slpm = 50 * ((flow / 16384.0) - 0.1) / 0.8;
            if slpm>50:
                slpm=prev_slpm
            else:
                prev_slpm=slpm

            f = open(realtime_directory()+"flow.txt","w")
            f.write("%1.3f" %(slpm))
            f.close()
            
            if slpm<0:slpm=0
            if slpm>0:
                run_once = False
                peep_counter = 0                
                if inhilation_start == False:
                    #print ("start inhilation")
                    inhilation_start = True
                    exhilation_start = False
                    start_inhilation_time = time.time()

                if inhilation_start == True and exhilation_start == True:
                    total_exhilation_time = time.time() - start_exhilation_time
                    #print ("Inhilation: %0.1f" %(total_inhilation_time))
                    #print ("Exhilation: %0.1f" %(total_exhilation_time))
                    f = open(realtime_directory()+"inh_time.txt","w")
                    f.write("%0.1f" %(total_inhilation_time))
                    f.close()
                    f = open(realtime_directory()+"exh_time.txt","w")
                    f.write("%0.1f" %(total_exhilation_time))
                    f.close()
                    inhilation_start = False
                    exhilation_start = False

                if (sampling_time < 90):
                    sampling_time = prev_sampling_time
                else:
                    prev_sampling_time = sampling_time

                vt += (((slpm / 60) / (1 / (sampling_time / 1000.0))) * 1000)*1.3 #scale tidal volume by 30%
                #print (sampling_time)
                flow_range = flow_range + (slpm,)
                volume_range = volume_range + (vt,)

            else:
                if exhilation_start == False:
                    #print ("start_exhilation")
                    exhilation_start = True
                    start_exhilation_time = time.time()
                    total_inhilation_time = time.time() - start_inhilation_time

                peep_counter += 1
                if peep_counter == 15:   
                    #peep_counter = 0                 
                    if get_process_control() == "on":      
                        run_once = False   

                        #record the initial assist pressure
                        start_assist_press = inhilation 
                        #set limit to 0.5 above the recorded start assist  pressure
                        start_assist_press = start_assist_press + 0.5
                        #alt_limits_directory
                        f = open(realtime_directory()+'assist_pressure.txt', 'w')
                        f.write("%1.3f" %(start_assist_press))
                        f.close()

                        peep_pressure = pressure
                        f = open(realtime_directory()+'max_peep.txt','w')
                        f.write("%0.1f" %(peep_pressure))
                        f.close()

                        #print("PEEP: %0.1f" %(peep_pressure))
                        max_pressure = max(pressure_range)
                        max_flow = max(flow_range)
                        max_volume = max(volume_range)

                        f = open(realtime_directory()+'pressure_peak.txt','w')
                        f.write("%0.1f" %(max_pressure))
                        f.close()

                        f = open(realtime_directory()+'volume_peak.txt','w')
                        f.write("%0.1f" %(max_volume))
                        f.close()

                        f = open(realtime_directory()+'flow_peak.txt','w')
                        f.write("%0.1f" %(max_flow))
                        f.close()
                        #print("Max pressure: %0.1f" %(max_pressure))
                        #reset tuple
                        pressure_range = tuple()
                        flow_range = tuple()
                        volume_range = tuple()

                        #if any changes is tv and bpm, reset volume array
                        bpm = get_bpm()
                        if bpm != prev_bpm:
                            prev_bpm = bpm
                            vt_total = []

                        if get_tv() != prev_tidal_volume:
                            prev_tidal_volume = get_tv()
                            vt_total = []

                        #compute average volume
                        if len(vt_total)==bpm:
                            total_volume = sum(vt_total)/len(vt_total)
                            #print ("Total vol: %0.1f"  %(total_volume) )
                            vt_total.pop(0)
                            vt_total += [max_volume]                              
                        else:
                            vt_total += [max_volume] 
                            total_volume = get_tv()                                                 

                        #evaluate alarms here
                        #evaluate peep and pressure limits
                        if max_pressure < get_pressure_lo_lim() and peep_pressure < get_peep_lo_lim():
                            main_alarm = True
                            print("Circuit Fault Alarm")
                            #set alarm to critical color
                            f=open(gui_directory()+'alarm_color.txt','w')
                            f.write("%s" %(get_red()))
                            f.close()

                            f=open(gui_directory()+'alarm_status.txt','w')
                            f.write("CKT FAULT")
                            f.close()   

                            f = open(realtime_directory()+'beep','w')
                            f.write("1")
                            f.close()                         

                        else: 
                            if max_pressure > get_pressure_hi_lim():
                                main_alarm = True
                                print("High Pressure Alarm: %0.1f" %(max_pressure))
                                f=open(gui_directory()+'alarm_color.txt','w')
                                f.write("%s" %(get_red()))
                                f.close()     

                                f=open(gui_directory()+'alarm_status.txt','w')
                                f.write("HIGH PIP")
                                f.close()

                                f = open(realtime_directory()+'beep','w')
                                f.write("1")
                                f.close()         

                            elif peep_pressure > get_peep_hi_lim():
                                main_alarm = True
                                print("Max PEEP Alarm %0.1f" %(peep_pressure))  
                                f=open(gui_directory()+'alarm_color.txt','w')
                                f.write("%s" %(get_red()))
                                f.close()   

                                f=open(gui_directory()+'alarm_status.txt','w')
                                f.write("HIGH PEEP")
                                f.close()  

                                f = open(realtime_directory()+'beep','w')
                                f.write("1")
                                f.close()

                            elif peep_pressure < get_peep_lo_lim():
                                main_alarm = True
                                print("Low PEEP Alarm %0.1f" %(peep_pressure))
                                f=open(gui_directory()+'alarm_color.txt','w')
                                f.write("%s" %(get_red()))
                                f.close()        

                                f=open(gui_directory()+'alarm_status.txt','w')
                                f.write("LOW PEEP")
                                f.close()  

                                f = open(realtime_directory()+'beep','w')
                                f.write("1")
                                f.close()
                        
                            #evaluate O2 sensor
                            elif oxygen < get_o2_lo_limit():
                                #low oxygen
                                main_alarm = True
                                print("Low Oxygen")
                                #set alarm to critical color
                                f=open(gui_directory()+'alarm_color.txt','w')
                                f.write("%s" %(get_red()))
                                f.close()

                                f=open(gui_directory()+'alarm_status.txt','w')
                                f.write("LOW O2")
                                f.close()   

                                f = open(realtime_directory()+'beep','w')
                                f.write("1")
                                f.close()    

                            elif oxygen > get_o2_hi_limit():
                                    #high oxygen
                                    main_alarm = True
                                    print("High Oxygen")
                                    #set alarm to critical color
                                    f=open(gui_directory()+'alarm_color.txt','w')
                                    f.write("%s" %(get_red()))
                                    f.close()

                                    f=open(gui_directory()+'alarm_status.txt','w')
                                    f.write("HIGH O2")
                                    f.close()   

                                    f = open(realtime_directory()+'beep','w')
                                    f.write("1")
                                    f.close()  


                            #compare it with set volume
                            elif(total_volume > get_tv() *1.1):
                                main_alarm = True
                                print("High VT")
                            
                                f=open(gui_directory()+'alarm_color.txt','w')
                                f.write("%s" %(get_red()))
                                f.close()

                                f=open(gui_directory()+'alarm_status.txt','w')
                                f.write("HIGH VT")
                                f.close()   

                                f = open(realtime_directory()+'beep','w')
                                f.write("1")
                                f.close()                                 

                            elif( total_volume < get_tv() *0.9):
                                main_alarm = True
                                print("Low VT")

                                f=open(gui_directory()+'alarm_color.txt','w')
                                f.write("%s" %(get_red()))
                                f.close()

                                f=open(gui_directory()+'alarm_status.txt','w')
                                f.write("LOW VT")
                                f.close()   

                                f = open(realtime_directory()+'beep','w')
                                f.write("1")
                                f.close() 
                        
                            else:
                                main_alarm = False
                                #if other_alarm == False:
                                #print("Normal")
                                f=open(gui_directory()+'alarm_color.txt','w')
                                f.write("%s" %(get_green()))
                                f.close()   

                                f=open(gui_directory()+'alarm_status.txt','w')
                                f.write("NORMAL")
                                f.close()  

                                f = open(realtime_directory()+'beep','w')
                                f.write("0")
                                f.close()                                                              

                    else:
                        if run_once == False:
                            run_once = True
                            #print("Stopped")
                            f=open(gui_directory()+'alarm_color.txt','w')
                            f.write("%s" %(get_green()))
                            f.close()   

                            f=open(gui_directory()+'alarm_status.txt','w')
                            f.write("STOPPED")
                            f.close()                             

                vt = 0            

            f = open(realtime_directory()+"volume.txt","w")
            #print (vt)
            f.write("%1.3f" %(vt))
            f.close()
            
        except:
            f = open("error.txt","a")
            f.write("%1.1f,%1.1f,%1.1f\r\n" %(slpm, vt, sampling_time))
            f.close()
            print("ERROR")
            pass
                    
        #print("Values: SLPM: %1.3f, INH %1.3f, PRES %1.3f, OXY %1.3f, BATT %1.3f, VT %1.3f " %(slpm,inhilation,pressure,oxygen,battery, vt))
        #sys.stdout.flush()
        #print("Values: SLPM: %1.3f, INH %1.3f" %(slpm,inhilation))
        time.sleep(0.06)
		
		
if __name__ == "__main__":
    main()		
