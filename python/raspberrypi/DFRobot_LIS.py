# -*- coding: utf-8 -*
""" 
  @file DFRobot_LIS.py
  @brief Define the basic structure of class DFRobot_LIS 
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author [fengli](li.feng@dfrobot.com)
  @version  V1.0
  @date  2021-1-30
  @get from https://www.dfrobot.com
  @url https://github.com/DFRobot/DFRobot_LIS
"""
import struct
import serial
import time
import smbus
import spidev 
import numpy as np
import RPi.GPIO as RPIGPIO

H3LIS200DL                = 0x01  
LIS331HH                  = 0x02  

class DFRobot_LIS(object):
  REG_CARD_ID    = 0x0F       #Chip id
  REG_CTRL_REG1  = 0x20       #Control register 1
  REG_CTRL_REG4  = 0x23       #Control register 4
  REG_CTRL_REG2  = 0x21       #Control register 2
  REG_CTRL_REG3  = 0x22       #Control register 3
  REG_CTRL_REG5  = 0x24       #Control register 5
  REG_CTRL_REG6  = 0x25       #Control register 6
  REG_STATUS_REG = 0x27       #Status register
  REG_OUT_X_L    = 0x28       #The low order of the X-axis acceleration register
  REG_OUT_X_H    = 0x29       #The high point of the X-axis acceleration register
  REG_OUT_Y_L    = 0x2A       #The low order of the Y-axis acceleration register
  REG_OUT_Y_H    = 0x2B       #The high point of the Y-axis acceleration register
  REG_OUT_Z_L    = 0x2C       #The low order of the Z-axis acceleration register
  REG_OUT_Z_H    = 0x2D       #The high point of the Z-axis acceleration register
  REG_INT1_THS   = 0x32       #Interrupt source 1 threshold
  REG_INT2_THS   = 0x36       #Interrupt source 2 threshold
  REG_INT1_CFG   = 0x30       #Interrupt source 1 configuration register
  REG_INT2_CFG   = 0x34       #Interrupt source 2 configuration register
  REG_INT1_SRC   = 0x31       #Interrupt source 1 status register
  REG_INT2_SRC   = 0x35       #Interrupt source 2 status register
  
  __range = 100
  __reset = 0
  __chip = 0
  
  '''
    Power mode selection, determine the frequency of data collection
    Represents the number of data collected per second
  '''
  POWERDOWN_0HZ = 0
  LOWPOWER_HALFHZ = 1 
  LOWPOWER_1HZ = 2
  LOWPOWER_2HZ = 3
  LOWPOWER_5HZ = 4
  LOWPOWER_10HZ = 5 
  NORMAL_50HZ = 6
  NORMAL_100HZ = 7
  NORMAL_400HZ = 8
  NORMAL_1000HZ = 9
  
  '''
  Sensor range selection
  '''
  H3LIS200DL_100G = 100 #±100G
  H3LIS200DL_200G = 200 #±200G

  LIS331H_6G      = 6   #±6G
  LIS331H_12G     = 12  #±12G
  LIS331H_24G     = 24  #±24G

  '''
  #                           High-pass filter cut-off frequency configuration
  # |--------------------------------------------------------------------------------------------------------|
  # |                |    ft [Hz]      |        ft [Hz]       |       ft [Hz]        |        ft [Hz]        |
  # |   mode         |Data rate = 50 Hz|   Data rate = 100 Hz |  Data rate = 400 Hz  |   Data rate = 1000 Hz |
  # |--------------------------------------------------------------------------------------------------------|
  # |  eCutoffMode1  |     1           |         2            |            8         |             20        |
  # |--------------------------------------------------------------------------------------------------------|
  # |  eCutoffMode2  |    0.5          |         1            |            4         |             10        |
  # |--------------------------------------------------------------------------------------------------------|
  # |  eCutoffMode3  |    0.25         |         0.5          |            2         |             5         |
  # |--------------------------------------------------------------------------------------------------------|
  # |  eCutoffMode4  |    0.125        |         0.25         |            1         |             2.5       |
  # |--------------------------------------------------------------------------------------------------------|
  '''
  CUTOFF_MODE1 = 0
  CUTOFF_MODE2 = 1
  CUTOFF_MODE3 = 2
  CUTOFF_MODE4 = 3
  SHUTDOWN     = 4
  
  '''
  Interrupt event
  '''
  X_LOWTHAN_TH     = 0  #The acceleration in the x direction is less than the threshold
  X_HIGHERTHAN_TH  = 1  #The acceleration in the x direction is greater than the threshold
  Y_LOWTHAN_TH     = 2  #The acceleration in the y direction is less than the threshold
  Y_HIGHERTHAN_TH  = 3  #The acceleration in the y direction is greater than the threshold
  Z_LOWTHAN_TH     = 4  #The acceleration in the z direction is less than the threshold
  Z_HIGHERTHAN_TH  = 5  #The acceleration in the z direction is greater than the threshold
  EVENT_ERROR      = 6  # No event

  #Interrupt pin selection
  INT_1 = 0 #int1
  INT_2 = 1 #int2
  
  def __init__(self,chip1):
    __reset = 1
    self.__chip = chip1

  '''
    @brief Initialize the function
    @return Return 0 indicates a successful initialization, while other values indicates failure and return to error code.
  '''
  def begin(self):
    identifier = 0 
    identifier = self.read_reg(self.REG_CARD_ID)
    if identifier == 0x32:
      #print("identifier = :")
      #print(identifier)
      return 0
    else:
      return 1
      
  '''
    @brief Get chip id
    @return Returns the 8 bit serial number
  '''
  def get_id(self):
    identifier = 0 
    identifier = self.read_reg(self.REG_CARD_ID)
    return identifier

  '''
    @brief Set the measurement range
    @param range:Range(g)
                 RANGE_100_G =0   #±100g
                 RANGE_200_G = 1  # ±200g
                 LIS331H_6G  = 6  #±6G
                 LIS331H_12G = 12 #±12G
                 LIS331H_24G = 24 #±24G
  '''
  def set_range(self,range_r):
    reg = self.read_reg(self.REG_CTRL_REG4)
    if self.__chip == H3LIS200DL:
        if range_r == self.H3LIS200DL_100G:
         reg = reg & (~0x10)
         self.__range = 100
        else:
         reg = reg | 0x10
         self.__range = 200
    elif self.__chip == LIS331HH:
        self.__range = range_r
        if range_r == self.LIS331H_6G:
         reg = reg&(~(3<<4))
        elif range_r == self.LIS331H_6G:
         reg = reg&(~(3<<4))
         reg = reg | (0x01<<4)
        elif range_r == self.LIS331H_6G:
         reg = reg&(~(3<<4))
         reg = reg | (0x03<<4)
    #print(reg)
    self.write_reg(self.REG_CTRL_REG4,reg)

  
  '''
    @brief Set data measurement rate
    @param rate:rate(HZ)
                 POWERDOWN_0HZ   = 0
                 LOWPOWER_HALFHZ = 1 
                 LOWPOWER_1HZ    = 2
                 LOWPOWER_2HZ    = 3
                 LOWPOWER_5HZ    = 4
                 LOWPOWER_10HZ   = 5 
                 NORMAL_50HZ     = 6
                 NORMAL_100HZ    = 7
                 NORMAL_400HZ    = 8
                 NORMAL_1000HZ   = 9
  '''
  def set_acquire_rate(self, rate):    
    reg = self.read_reg(self.REG_CTRL_REG1)
    #print(reg);
    if rate == self.POWERDOWN_0HZ:
      reg = reg & (~(0x7 << 5))
    elif rate == self.LOWPOWER_HALFHZ:
      reg = reg & (~(0x7 << 5))
      reg = reg | (0x02 << 5)
    elif rate == self.LOWPOWER_1HZ:
      reg = reg & (~(0x7 << 5))
      reg = reg | (0x03 << 5)
    elif rate == self.LOWPOWER_2HZ:
      reg = reg & (~(0x7 << 5))
      reg = reg | (0x04 << 5)
    elif rate == self.LOWPOWER_5HZ:
      reg = reg & (~(0x7 << 5))
      reg = reg | (0x05 << 5)
    elif rate == self.LOWPOWER_10HZ:
      reg = reg & (~(0x7 << 5))
      reg = reg | (0x06 << 5)
    elif rate == self.NORMAL_50HZ:
      reg = reg & (~(0x7 << 5))
      reg = reg | (0x01 << 5)
      reg = reg & (~(0x3 << 3))
    elif rate == self.NORMAL_100HZ:
      reg = reg & (~(0x7 << 5))
      reg = reg | (0x01 << 5)
      reg = reg & (~(0x3 << 3))
      reg = reg | (0x01 << 3)
    elif rate == self.NORMAL_400HZ:
      reg = reg & (~(0x7 << 5))
      reg = reg | (0x01 << 5)
      reg = reg & (~(0x3 << 3))
      reg = reg | (0x02 << 3)
    elif rate == self.NORMAL_1000HZ:
      reg = reg & (~(0x7 << 5))
      reg = reg | (0x01 << 5)
      reg = reg & (~(0x3 << 3))
      reg = reg | (0x03 << 3)
    self.write_reg(self.REG_CTRL_REG1,reg)

  '''
    @brief Set the threshold of interrupt source 1 interrupt
    @param threshold:Threshold(g)
  '''
  def set_int1_th(self,threshold):
    reg = (threshold * 128)/self.__range
    #print(reg)
    self.write_reg(self.REG_INT1_THS,reg)


  '''
    @brief Set interrupt source 2 interrupt generation threshold
    @param threshold:Threshold(g)
  '''
  def set_int2_th(self,threshold):
    reg = (threshold * 128)/self.__range
    #print(reg)
    self.write_reg(self.REG_INT2_THS,reg)
  
  '''
    @brief Enable interrupt
    @param source Interrupt pin selection
             INT_1 = 0,/<int pad 1 >/
             INT_2,/<int pad 2>/
    @param event Interrupt event selection
                 X_LOWTHAN_TH     = 0 <The acceleration in the x direction is less than the threshold>
                 X_HIGHERTHAN_TH  = 1<The acceleration in the x direction is greater than the threshold>
                 Y_LOWTHAN_TH     = 2<The acceleration in the y direction is less than the threshold>
                 Y_HIGHERTHAN_TH  = 3<The acceleration in the y direction is greater than the threshold>
                 Z_LOWTHAN_TH     = 4<The acceleration in the z direction is less than the threshold
                 Z_HIGHERTHAN_TH  = 5<The acceleration in the z direction is greater than the threshold>
                 EVENT_ERROR      = 6 <No event>
  '''
  def enable_int_event(self,source,event):
    reg = 0    
    if source == self.INT_1:
      reg = self.read_reg(self.REG_INT1_CFG)
    else:
      reg = self.read_reg(self.REG_INT2_CFG)
    if self.__reset == 1:
       reg = 0
       self.__reset = 0
    if event == self.X_LOWTHAN_TH:
      reg = reg | 0x01
    elif event == self.X_HIGHERTHAN_TH:
      reg = reg | 0x02
    elif event == self.Y_LOWTHAN_TH:
      reg = reg | 0x04
    elif event == self.Y_HIGHERTHAN_TH:
      reg = reg | 0x08
    elif event == self.Z_LOWTHAN_TH:
      reg = reg | 0x10      
    elif event == self.Z_HIGHERTHAN_TH:
      reg = reg | 0x20
      
    #print(reg)
    if source == self.INT_1:
      self.write_reg(self.REG_INT1_CFG,reg)
    else:
      self.write_reg(self.REG_INT2_CFG,reg)

  '''
    @brief Check whether the interrupt event'event' is generated in interrupt 1
    @param event:Interrupt event
                  X_LOWTHAN_TH     = 0<The acceleration in the x direction is less than the threshold>
                  X_HIGHERTHAN_TH  = 1<The acceleration in the x direction is greater than the threshold>
                  Y_LOWTHAN_TH     = 2<The acceleration in the y direction is less than the threshold>
                  Y_HIGHERTHAN_TH  = 3<The acceleration in the y direction is greater than the threshold>
                  Z_LOWTHAN_TH     = 4<The acceleration in the z direction is less than the threshold
                  Z_HIGHERTHAN_TH  = 5<The acceleration in the z direction is greater than the threshold>
                  EVENT_ERROR      = 6 <No event>
    @return true 产生了此事件
            false 未产生此事件
  '''
  def get_int1_event(self,event):
    reg = self.read_reg(self.REG_INT1_SRC)
    if (reg & (1 << event)) >= 1:
         return True
    else:
         return False
         
  '''
    @brief Check whether the interrupt event'event' is generated in interrupt 2
    @param event:Interrupt event
                  X_LOWTHAN_TH     = 0<The acceleration in the x direction is less than the threshold>
                  X_HIGHERTHAN_TH  = 1<The acceleration in the x direction is greater than the threshold>
                  Y_LOWTHAN_TH     = 2<The acceleration in the y direction is less than the threshold>
                  Y_HIGHERTHAN_TH  = 3<The acceleration in the y direction is greater than the threshold>
                  Z_LOWTHAN_TH     = 4<The acceleration in the z direction is less than the threshold
                  Z_HIGHERTHAN_TH  = 5<The acceleration in the z direction is greater than the threshold>
                  EVENT_ERROR      = 6 <No event>
    @return true 产生了此事件
            false 未产生此事件
  '''
  def get_int2_event(self,event):
    reg = self.read_reg(self.REG_INT2_SRC)
    if (reg & (1 << event)) >= 1:
         return True
    else:
         return False
  '''
    @brief Enable sleep wake function
    @param enable:True(enable)/False(disable)
  '''
  def enable_sleep(self, enable):
    reg = 0
    if enable == True:
      reg = 3
    else:
      reg = 0
    self.write_reg(self.REG_CTRL_REG5,reg)
    return 0

  
  
  '''
    @brief Set data filtering mode
    @param mode:Four modes
                CUTOFF_MODE1 = 0
                CUTOFF_MODE2 = 1
                CUTOFF_MODE3 = 2
                CUTOFF_MODE4 = 3
                              High-pass filter cut-off frequency configuration
    |--------------------------------------------------------------------------------------------------------|
    |                |    ft [Hz]      |        ft [Hz]       |       ft [Hz]        |        ft [Hz]        |
    |   mode         |Data rate = 50 Hz|   Data rate = 100 Hz |  Data rate = 400 Hz  |   Data rate = 1000 Hz |
    |--------------------------------------------------------------------------------------------------------|
    |  CUTOFF_MODE1  |     1           |         2            |            8         |             20        |
    |--------------------------------------------------------------------------------------------------------|
    |  CUTOFF_MODE2  |    0.5          |         1            |            4         |             10        |
    |--------------------------------------------------------------------------------------------------------|
    |  CUTOFF_MODE3  |    0.25         |         0.5          |            2         |             5         |
    |--------------------------------------------------------------------------------------------------------|
    |  CUTOFF_MODE4  |    0.125        |         0.25         |            1         |             2.5       |
    |--------------------------------------------------------------------------------------------------------|
  '''
  def set_filter_mode(self,mode):
    reg = self.read_reg(self.REG_CTRL_REG2)
    if mode == self.SHUTDOWN:
      reg = reg & (~0x10)
      return 0
    else:
      reg = reg | 0x10
    reg = reg & (~3)
    reg = reg | mode
    self.write_reg(self.REG_CTRL_REG2,reg)
  
  '''
    @brief Get the acceleration in the three directions of xyz
    @return Three-axis acceleration 
  '''
  def read_acce_xyz(self):
    reg = self.read_reg(self.REG_STATUS_REG)
    data = [0,0,0,0,0,0,0]
    offset = 0
    x = 0
    y = 0
    z = 0
    if(reg & 0x01) == 1:
        data[0] = self.read_reg(self.REG_OUT_X_L)
        data[1] = self.read_reg(self.REG_OUT_X_H)
        data[2] = self.read_reg(self.REG_OUT_Y_L)
        data[3] = self.read_reg(self.REG_OUT_Y_H)
        data[4] = self.read_reg(self.REG_OUT_Z_L)
        data[5] = self.read_reg(self.REG_OUT_Z_H)
        
        data[0] = np.int8(data[0])
        data[1] = np.int8(data[1])
        data[2] = np.int8(data[2])
        data[3] = np.int8(data[3])
        data[4] = np.int8(data[4])
        data[5] = np.int8(data[5])

        if self.__chip == H3LIS200DL:
            x = (data[1]*self.__range)/128
            y = (data[3]*self.__range)/128
            z = (data[5]*self.__range)/128
        elif self.__chip == LIS331HH:
            x = data[1]*256+data[0]
            x = (x*1000*self.__range)/(256*128)
            y = data[3]*256+data[2]
            y = (y*1000*self.__range)/(256*128)
            z = data[5]*256+data[4]
            z = (z*1000*self.__range)/(256*128)
    return x,y,z

class DFRobot_H3LIS_I2C(DFRobot_LIS): 
  def __init__(self ,bus ,addr):
    self.__addr = addr
    super(DFRobot_H3LIS_I2C, self).__init__(H3LIS200DL)
    self.i2cbus = smbus.SMBus(bus)
    RPIGPIO.setmode(RPIGPIO.BCM)
    RPIGPIO.setwarnings(False)
  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
        data1 = [0]
        data1[0] = data
        self.i2cbus.write_i2c_block_data(self.__addr ,reg,data1)
        
  '''
    @brief read the data from the register
    @param reg register address
    @rerun value read data
  '''
  def read_reg(self, reg):
    self.i2cbus.write_byte(self.__addr,reg)
    time.sleep(0.01)
    rslt = self.i2cbus.read_byte(self.__addr)
    return rslt
  
  '''
    @brief  Set External Interrupt
    @param pin Interrupt pin
    @param cb Interrupt service function
    @param mode Interrupt trigger mode
  '''
  def attach_interrupt(self,pin, cb,mode):
    RPIGPIO.setup(pin, RPIGPIO.IN)
    if mode != RPIGPIO.RISING and mode != RPIGPIO.FALLING and mode != RPIGPIO.BOTH:
      return
    RPIGPIO.add_event_detect(pin, mode, cb)
class DFRobot_H3LIS_SPI(DFRobot_LIS): 
  def __init__(self ,cs, bus = 0, dev = 0,speed = 100000):
    super(DFRobot_H3LIS_SPI, self).__init__(H3LIS200DL)
    RPIGPIO.setmode(RPIGPIO.BCM)
    RPIGPIO.setwarnings(False)
    self.__cs = cs
    RPIGPIO.setup(self.__cs, RPIGPIO.OUT)
    RPIGPIO.output(self.__cs, RPIGPIO.LOW)
    self.__spi = spidev.SpiDev()
    self.__spi.open(bus, dev)
    self.__spi.no_cs = True
    self.__spi.max_speed_hz = speed
  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
     data1 =[reg,data]
     RPIGPIO.output(self.__cs, RPIGPIO.LOW)
     self.__spi.writebytes(data1)
     RPIGPIO.output(self.__cs, RPIGPIO.HIGH)
     #self._spi.transfer(data)
  '''
    @brief read the data from the register
    @param reg register address
    @return value read data
  '''
  def read_reg(self, reg):
     data1 =[reg+0x80]
     RPIGPIO.output(self.__cs, RPIGPIO.LOW)
     self.__spi.writebytes(data1)
     time.sleep(0.01)
     data = self.__spi.readbytes(1)
     RPIGPIO.output(self.__cs, RPIGPIO.HIGH)
     return  data[0]
  
  '''
    @brief  Set External Interrupt
    @param pin Interrupt pin
    @param cb Interrupt service function
    @param mode Interrupt trigger mode
  '''
  def attach_interrupt(self,pin, cb,mode):
    RPIGPIO.setup(pin, RPIGPIO.IN)
    if mode != RPIGPIO.RISING and mode != RPIGPIO.FALLING and mode != RPIGPIO.BOTH:
      return
    RPIGPIO.add_event_detect(pin, mode, cb)
     
     
class DFRobot_LIS331HH_I2C(DFRobot_LIS): 
  def __init__(self ,bus ,addr):
    self.__addr = addr
    super(DFRobot_LIS331HH_I2C, self).__init__(LIS331HH)
    self.i2cbus = smbus.SMBus(bus)
    RPIGPIO.setmode(RPIGPIO.BCM)
    RPIGPIO.setwarnings(False)
  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
        data1 = [0]
        data1[0] = data
        self.i2cbus.write_i2c_block_data(self.__addr ,reg,data1)
  '''
    @brief read the data from the register
    @param reg register address
    @return value read data
  '''
  def read_reg(self, reg):
    self.i2cbus.write_byte(self.__addr,reg)
    time.sleep(0.01)
    rslt = self.i2cbus.read_byte(self.__addr)
    #print(rslt)
    return rslt
  
  '''
    @brief  Set External Interrupt
    @param pin Interrupt pin
    @param cb Interrupt service function
    @param mode Interrupt trigger mode
  '''
  def attach_interrupt(self,pin, cb,mode):
    RPIGPIO.setup(pin, RPIGPIO.IN)
    if mode != RPIGPIO.RISING and mode != RPIGPIO.FALLING and mode != RPIGPIO.BOTH:
      return
    RPIGPIO.add_event_detect(pin, mode, cb)
    
class DFRobot_LIS331HH_SPI(DFRobot_LIS): 
  def __init__(self ,cs, bus = 0, dev = 0,speed = 1000000):
    super(DFRobot_LIS331HH_SPI, self).__init__(LIS331HH)
    RPIGPIO.setmode(RPIGPIO.BCM)
    RPIGPIO.setwarnings(False)
    self.__cs = cs
    RPIGPIO.setup(self.__cs, RPIGPIO.OUT)
    RPIGPIO.output(self.__cs, RPIGPIO.LOW)
    self.__spi = spidev.SpiDev()
    self.__spi.open(bus, dev)
    self.__spi.no_cs = True
    self.__spi.max_speed_hz = speed
  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
     data1 =[reg,data]
     RPIGPIO.output(self.__cs, RPIGPIO.LOW)
     self.__spi.writebytes(data1)
     RPIGPIO.output(self.__cs, RPIGPIO.HIGH)
     #self._spi.transfer(data)
  '''
    @brief read the data from the register
    @param reg register address
    @return value read data
  '''
  def read_reg(self, reg):
     data1 =[reg+0x80]
     RPIGPIO.output(self.__cs, RPIGPIO.LOW)
     self.__spi.writebytes(data1)
     time.sleep(0.01)
     data = self.__spi.readbytes(1)
     RPIGPIO.output(self.__cs, RPIGPIO.HIGH)
     #print(data)
     return  data[0]
  
  '''
    @brief  Set External Interrupt
    @param pin Interrupt pin
    @param cb Interrupt service function
    @param mode Interrupt trigger mode
  '''
  def attach_interrupt(self,pin, cb,mode):
    RPIGPIO.setup(pin, RPIGPIO.IN)
    if mode != RPIGPIO.RISING and mode != RPIGPIO.FALLING and mode != RPIGPIO.BOTH:
      return
    RPIGPIO.add_event_detect(pin, mode, cb)