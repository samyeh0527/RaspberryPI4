#!/usr/bin/env python3
import serial
from time import sleep
import sys
import statistics ,random
from threading import Timer
send_d = b'\xA5\x45\xEA'
offset2 = b'\xA5\xCC\x78\xDF'
offset_default= b'\xA5\x64\xDF'
ser = serial.Serial('/dev/ttyUSB0',9600)
class Temperature_detect():
    def __init__(self,compensation):
        self.compensation = compensation
        self.AVG_targetTemperature = []
        self.send_data = b'\xA5\x45\xEA'
        self.offset2 = b'\xA5\xCC\x78\xDF'
        self.offset_default = b'\xA5\x64\xDF'
        self.targetTemperature = None
        self.compensation_temperature = None
        self.avg_nubmer = 40
        self.switch = False
    def Temperature_detect_start(self):
        
        #ser.write(self.send_data)
        self.switch = True
        
        while self.switch == True :
             temperature = bytes(ser.read(10))#read temperature                 
             self.targetTemperature = (temperature[4]*256+temperature[5])/100
             self.compensation_temperature = self.targetTemperature + self.compensation
             self.AVG_targetTemperature.append(self.targetTemperature + self.compensation)
             
             print("Target temperature is %.2f"%self.targetTemperature)
             print('Add the compensation total temperature is %.2f'%self.compensation_temperature)
             print("Get 15 AVG temperatures is %.2f"%statistics.mean(self.AVG_targetTemperature))
             if len(self.AVG_targetTemperature) >self.avg_nubmer : self.AVG_targetTemperature.clear()
             
    def Temperature_get(self):
        temperature = bytes(ser.read(10))
        self.targetTemperature = (temperature[4]*256+temperature[5])/100
        self.compensation_temperature = self.targetTemperature + self.compensation
        print("Target temperature is %.2f"%self.targetTemperature)
        print('Add the compensation total temperature is %.2f'%self.compensation_temperature)
        return self.compensation_temperature

        
    
class Temperature_compensation():
    def __init__(self):
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

    print('==============HC version=============\nnote: this version provide test MCU90614 sensor so have two choice can use please follow manual \nchoice compensation mode\n1.Manul set Value(best parameter 30cm = 2 60cm = 3 ).\n2.Random get value.\n3.Sample code')
    mode = int(input('Enter you want mode.  '))
    try:
        if mode == 1:
            compensation_set_value = Temperature_compensation().Compensation()
            TemperatureWork = Temperature_detect(compensation_set_value).Temperature_detect_start()
            
        elif mode == 2:
            compensation_set_value = Temperature_compensation().RandomCompensation()
            TemperatureWork = Temperature_detect(compensation_set_value).Temperature_detect_start()
            
        elif mode == 3:
            #sample code 
            print('=========================now is example funcition=========================\n')
            avg_temprature =[]
            compensation_set_value = Temperature_compensation().Compensation()
            #if face is match .set match = true 
            match = True
            if match == True:
                for _ in range(10):
                    TemperatureWork = Temperature_detect(compensation_set_value).Temperature_get()
                    avg_temprature.append(TemperatureWork)
                print("Get AVG temperatures is %.2f"%statistics.mean(avg_temprature[5:]))
                
                if statistics.mean(avg_temprature[5:]) > 37.5 or statistics.mean(avg_temprature[5:]) < 30 :
                    print('=========================Warning=========================')
                    print("Get AVG temperatures is %.2f"%statistics.mean(avg_temprature[5:]))
                
            else: print("Error didn't match ")
            
            
            
            
            
    except ValueError as e:
        print(repr(e))
        
  
    #TemperatureWork = Temperature_detect(compensation_set_value).Temperature_detect_start()
        
    