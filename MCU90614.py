#!/usr/bin/env python3
import serial
from time import sleep
import sys
import statistics ,random


class Temperature_detect():
    def __init__(self,compensation):
        self.compensation = compensation
        self.AVG_targetTemperature = []
        self.send_data= b'\xA5\x45\xEA'
        self.offset2 = b'\xA5\xCC\x78\xDF'
        self.offset_default= b'\xA5\x64\xDF'
    def Temperature_detect_start(self):
        ser = serial.Serial('/dev/ttyAMA0',9600)
        ser.write(self.send_data)
        ser.write(self.offset2)
        
        while True :
             temperature = bytes(ser.read(10))#read temperature                 
             targetTemperature = (temperature[4]*256+temperature[5])/100
             self.AVG_targetTemperature.append(targetTemperature + self.compensation)
             print("Target temperature is =>%.2f"%((temperature[4]*256+temperature[5])/100))
             print('Add the compensation total temperature is =>%.2f'%(targetTemperature + self.compensation))
             print("Get 15 AVG temperatures is =>%.2f"%statistics.mean(self.AVG_targetTemperature))
             if len(self.AVG_targetTemperature) >15 : self.AVG_targetTemperature.clear()
             
    
    
class Temperature_compensation():
    def __init__(self):
        self.T_compensation = 0
        self.Randomcompensation =random.randrange(0,4,1)
        
    def Compensation(self):
        while True:
            try:
                compensation =int(input('Enter you want compensation value '))            
                return compensation 
            except ValueError as e:
                print("ValueError：",repr(e))
    def RandomCompensation(self):
        print('Random : ',self.Randomcompensation)
        return self.Randomcompensation
        
        
if __name__ == '__main__':

    print('==============demo version=============\nnote: this version provide test MCU90614 sensor so have two choice can use please follow manual \nchoice compensation mode\n1.Manul set Value(best parameter 1~4).\n2.Random get value.')
    mode = int(input('Enter you want mode.  '))
    try:
        if mode == 1:
            compensation_set_value = Temperature_compensation().Compensation()
        if mode == 2:
            compensation_set_value = Temperature_compensation().RandomCompensation()
    except ValueError as e:
        print(repr(e))
        
    TemperatureWork = Temperature_detect(compensation_set_value).Temperature_detect_start()
    
