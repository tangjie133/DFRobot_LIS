# -*- coding:utf-8 -*-
"""
   @file interrupt.py
   @brief  Interrupt detection of free fall, an interrupt signal will be generated in int1 once a free fall event occurs.
   @n When a free-fall motion is detected, it will be printed on the serial port.
   @n When using SPI, chip select pin can be modified by changing the value of RASPBERRY_PIN_CS
   @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
   @licence     The MIT License (MIT)
   @author [fengli](li.feng@dfrobot.com)
   @version  V1.0
   @date  2021-01-16
   @get from https://www.dfrobot.com
   @https://github.com/DFRobot/DFRobot_LIS2DW12
"""

import sys
sys.path.append("../../..") # set system path to top
from DFRobot_LIS2DW12 import *
import time

INT1 = 26                           #Interrupt pin, use BCM coding method, the code number is 26, corresponding to pin GPIO25
int_pad_Flag = False                 #intPad flag
def int_pad_callback(status):
  global int_pad_Flag
  int_pad_Flag = True

#If you want to use SPI to drive this module, open the following two-line comments, and connect the module with Raspberry Pi via it
#RASPBERRY_PIN_CS =  27              #Chip selection pin when SPI is selected, use BCM coding method, the number is 27, corresponding to pin GPIO2
#acce = DFRobot_IIS2DLPC_SPI(RASPBERRY_PIN_CS)

#If you want to use I2C to drive this module, open the following three-line comments, and connect the module with Raspberry Pi via it
#The I2C address can be switched through the DIP switch (gravity version) or SDO pin (Breakout version) on the board
I2C_BUS         = 0x01             #default use I2C1
#ADDRESS_0       = 0x18             #sensor address 0
ADDRESS_1       = 0x19             #sensor address 1
acce = DFRobot_IIS2DLPC_I2C(I2C_BUS ,ADDRESS_1)

# set int_Pad to input
GPIO.setup(INT1, GPIO.IN)
#set int_Pad interrupt callback
GPIO.add_event_detect(INT1,GPIO.RISING,int_pad_callback)

#Chip initialization
acce.begin()
#Get chip id
print('chip id :%x'%acce.get_id())
#Software reset to restore the value of all registers
acce.soft_reset()
#Choose whether to continuously let the chip collect data
acce.contin_refresh(True)

'''
   Set power mode:
     HIGH_PERFORMANCE_14BIT           #High-Performance Mode
     CONT_LOWPWR4_14BIT               #Continuous measurement,Low-Power Mode 4(14-bit resolution)
     CONT_LOWPWR3_14BIT               #Continuous measurement,Low-Power Mode 3(14-bit resolution)
     CONT_LOWPWR2_14BIT               #Continuous measurement,Low-Power Mode 2(14-bit resolution)
     CONT_LOWPWR1_12BIT               #Continuous measurement,Low-Power Mode 1(12-bit resolution)
     SING_LELOWPWR4_14BIT             #Single data conversion on demand mode,Low-Power Mode 4(14-bit resolution)
     SING_LELOWPWR3_14BIT             #Single data conversion on demand mode,Low-Power Mode 3(14-bit resolution
     SING_LELOWPWR2_14BIT             #Single data conversion on demand mode,Low-Power Mode 2(14-bit resolution)
     SING_LELOWPWR1_12BIT             #Single data conversion on demand mode,Low-Power Mode 1(12-bit resolution)
     HIGHP_ERFORMANCELOW_NOISE_14BIT  #High-Performance Mode,Low-noise enabled
     CONT_LOWPWRLOWNOISE4_14BIT       #Continuous measurement,Low-Power Mode 4(14-bit resolution,Low-noise enabled)
     CONT_LOWPWRLOWNOISE3_14BIT       #Continuous measurement,Low-Power Mode 3(14-bit resolution,Low-noise enabled)
     CONT_LOWPWRLOWNOISE2_14BIT       #Continuous measurement,Low-Power Mode 2(14-bit resolution,Low-noise enabled)
     CONT_LOWPWRLOWNOISE1_12BIT       #Continuous measurement,Low-Power Mode 1(14-bit resolution,Low-noise enabled)
     SINGLE_LOWPWRLOWNOISE4_14BIT     #Single data conversion on demand mode,Low-Power Mode 4(14-bit resolution),Low-noise enabled
     SINGLE_LOWPWRLOWNOISE3_14BIT     #Single data conversion on demand mode,Low-Power Mode 3(14-bit resolution),Low-noise enabled
     SINGLE_LOWPWRLOWNOISE2_14BIT     #Single data conversion on demand mode,Low-Power Mode 2(14-bit resolution),Low-noise enabled
     SINGLE_LOWPWRLOWNOISE1_12BIT     #Single data conversion on demand mode,Low-Power Mode 1(12-bit resolution),Low-noise enabled
'''
acce.set_power_mode(acce.CONT_LOWPWR4_14BIT);
'''
    Set the sensor data collection rate:
        RATE_OFF            #Measurement off
        RATE_1HZ6           #1.6hz, use only under low-power mode
        RATE_12HZ5          #12.5hz
        RATE_25HZ           
        RATE_50HZ           
        RATE_100HZ          
        RATE_200HZ          
        RATE_400HZ          #Use only under High-Performance mode
        RATE_800HZ          #Use only under High-Performance mode
        RATE_1600HZ         #Use only under High-Performance mode
        SETSWTRIG           #The software triggers a single measurement
'''
acce.set_data_rate(acce.RATE_100HZ);
'''
   Set the measurement range
               RANGE_2G     #±2g
               RANGE_4G     #±4g
               RANGE_8G     #±8g
               RANGE_16G    #±16g
'''
acce.set_range(acce.RANGE_2G)
'''
  Set the free fall time (Or the number of free-fall samples. The free-fall events will not occur unless the samples are enough.)
     dur duration(0 ~ 31)
     time = dur * (1/rate)(unit:s)
     |                      An example of a linear relationship between an argument and time                                  |
     |------------------------------------------------------------------------------------------------------------------------|
     |                |                     |                          |                          |                           |
     |  Data rate     |       25 Hz         |         100 Hz           |          400 Hz          |         = 800 Hz          |
     |------------------------------------------------------------------------------------------------------------------------|
     |   time         |dur*(1s/25)= dur*40ms|  dur*(1s/100)= dur*10ms  |  dur*(1s/400)= dur*2.5ms |  dur*(1s/800)= dur*1.25ms |
     |------------------------------------------------------------------------------------------------------------------------|
'''
acce.set_free_fall_Dur(dur = 0x06)

'''
  Set the interrupt source of the int1 pin:
          DOUBLE_TAP(Double tap)
          FREEFALL(Free fall)
          WAKEUP(wake)
          SINGLE_TAP(single tap)
          IA6D(Orientation change check)
'''
acce.set_int1_event(acce.FREEFALL)
time.sleep(0.1)

while True:
  if(int_pad_Flag == True):
    #Free fall event is detected
    time.sleep(0.1)
    free_fall = acce.free_fall_detected()
    if free_fall == True:
      print("free fall detected")
      time.sleep(0.2)
    int_pad_Flag = False
