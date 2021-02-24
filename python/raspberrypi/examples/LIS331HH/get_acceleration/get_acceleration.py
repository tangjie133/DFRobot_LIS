# -*- coding:utf-8 -*-
"""
  @file get_acceleration.py
  @brief 获取x,y,z三个方向的加速度值,范围(±6g/±12g/±24g)
  @n 在使用SPI时,片选引脚时可以通过改变RASPBERRY_PIN_CS的值修改
  @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author [fengli](li.feng@dfrobot.com)
  @version  V1.0
  @date  2021-01-16
  @get from https://www.dfrobot.com
  @https://github.com/DFRobot/DFRobot_LIS
"""

import sys
sys.path.append("../../..") # set system path to top

from DFRobot_LIS import *
import time

#如果你想要用SPI驱动此模块，打开下面两行的注释,并通过SPI连接好模块和树莓派
#RASPBERRY_PIN_CS =  27              #Chip selection pin when SPI is selected
#acce = DFRobot_LIS331HH_SPI(RASPBERRY_PIN_CS)

#如果你想要应IIC驱动此模块，打开下面三行的注释，并通过I2C连接好模块和树莓派
I2C_BUS         = 0x01            #default use I2C1
ADDRESS         = 0x19            #I2C address
acce = DFRobot_LIS331HH_I2C(I2C_BUS ,ADDRESS)

#Chip initialization
acce.begin()
#Get chip id
print("chip id :")
print(acce.get_id())

'''
set range:Range(g)
          LIS331H_6G  = 6   #±6G
          LIS331H_12G = 12  #±12G
          LIS331H_24G = 24  #±24G
'''
acce.set_range(acce.LIS331H_6G)

'''
Set data measurement rate
         POWERDOWN_0HZ 
         LOWPOWER_HALFHZ 
         LOWPOWER_1HZ 
         LOWPOWER_2HZ 
         LOWPOWER_5HZ 
         LOWPOWER_10HZ 
         NORMAL_50HZ 
         NORMAL_100HZ 
         NORMAL_400HZ 
         NORMAL_1000HZ 
'''
acce.set_acquire_rate(acce.NORMAL_50HZ)
time.sleep(0.1)

while True:
    #Get the acceleration in the three directions of xyz
    x,y,z = acce.read_acce_xyz()
    time.sleep(1)
    print("Acceleration [X = %.2d mg,Y = %.2d mg,Z = %.2d mg]"%(x,y,z))
