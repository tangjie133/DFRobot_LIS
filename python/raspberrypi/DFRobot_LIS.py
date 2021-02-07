# -*- coding: utf-8 -*
""" 
  @file DFRobot_H3LIS.py
  @brief Define the basic structure of class DFRobot_H3LIS 
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author [fengli](li.feng@dfrobot.com)
  @version  V1.0
  @date  2021-1-30
  @get from https://www.dfrobot.com
  @url https://github.com/DFRobot/DFRobot_H3LIS
"""
import struct
import serial
import time
import smbus
import spidev
#from gpio import GPIO
import numpy as np

I2C_MODE                  = 0x01
SPI_MODE                  = 0x02
H3LIS200DL        = 0x01  
LIS331HH          = 0x02  

class SPI:
  
  MODE_1 = 1
  MODE_2 = 2
  MODE_3 = 3
  MODE_4 = 4
  def __init__(self, bus, dev, speed = 100000, mode = MODE_4):
    self._bus = spidev.SpiDev()
    self._bus.open(0, 0)
    self._bus.no_cs = True
    self._bus.max_speed_hz = speed
    #self._bus.threewire  = True
  def transfer(self, buf):
    if len(buf):
      return self._bus.writebytes(buf)
    return []
  def readData(self, cmd):
    return self._bus.readbytes(cmd)

import RPi.GPIO as RPIGPIO

RPIGPIO.setmode(RPIGPIO.BCM)
RPIGPIO.setwarnings(False)

class GPIO:

  HIGH = RPIGPIO.HIGH
  LOW = RPIGPIO.LOW

  OUT = RPIGPIO.OUT
  IN = RPIGPIO.IN

  RISING = RPIGPIO.RISING
  FALLING = RPIGPIO.FALLING
  BOTH = RPIGPIO.BOTH

  def __init__(self, pin, mode, defaultOut = HIGH):
    self._pin = pin
    self._fInt = None
    self._intDone = True
    self._intMode = None
    if mode == self.OUT:
      RPIGPIO.setup(pin, mode)
      if defaultOut == self.HIGH:
        RPIGPIO.output(pin, defaultOut)
      else:
        RPIGPIO.output(pin, self.LOW)
    else:
      RPIGPIO.setup(pin, self.IN, pull_up_down = RPIGPIO.PUD_UP)

  def setOut(self, level):
    if level:
      RPIGPIO.output(self._pin, self.HIGH)
    else:
      RPIGPIO.output(self._pin, self.LOW)

  def _intCB(self, status):
    if self._intDone:
      self._intDone = False
      time.sleep(0.02)
      if self._intMode == self.BOTH:
        self._fInt()
      elif self._intMode == self.RISING and self.read() == self.HIGH:
        self._fInt()
      elif self._intMode == self.FALLING and self.read() == self.LOW:
        self._fInt()
      self._intDone = True

  def setInterrupt(self, mode, cb):
    if mode != self.RISING and mode != self.FALLING and mode != self.BOTH:
      return
    self._intMode = mode
    RPIGPIO.add_event_detect(self._pin, mode, self._intCB)
    self._fInt = cb

  def read(self):
    return RPIGPIO.input(self._pin)
  
  def cleanup(self):
    RPIGPIO.cleanup()
class DFRobot_LIS(object):
  REG_CARD_ID = 0x0F     #Chip id
  REG_CTRL_REG1 = 0x20     #Control register 1
  REG_CTRL_REG4 = 0x23     #Control register 4
  REG_CTRL_REG2 = 0x21     #Control register 2
  REG_CTRL_REG3 = 0x22     #Control register 3
  REG_CTRL_REG5 = 0x24     #Control register 5
  REG_CTRL_REG6 = 0x25     #Control register 6
  REG_STATUS_REG = 0x27    #Status register
  REG_OUT_X_L = 0x28     #Acceleration register
  REG_OUT_X_H = 0x29
  REG_OUT_Y_L = 0x2A     #Acceleration register
  REG_OUT_Y_H = 0x2B     #Acceleration register
  REG_OUT_Z_L = 0x2C     #Acceleration register
  REG_OUT_Z_H = 0x2D     #Acceleration register
  REG_INT1_THS = 0x32     #Interrupt source 1 threshold
  REG_INT2_THS = 0x36     #Interrupt source 2 threshold
  REG_INT1_CFG = 0x30     #Interrupt source 1 configuration register
  REG_INT2_CFG = 0x34     #Interrupt source 2 configuration register
  REG_INT1_SRC = 0x31     #Interrupt source 1 status register
  REG_INT2_SRC = 0x35     #Interrupt source 2 status register
  __m_flag   = 0                # mode flag
  __count    = 0                # acquisition count    
  __txbuf        = [0]          # i2c send buffer
  __uart_i2c     =  0
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
  H3LIS200DL_100G =100  # ¡À100G
  H3LIS200DL_200G = 200 # ¡À200G

  LIS331H_6G = 6  #¡À6G
  LIS331H_12G = 12  #¡À12G
  LIS331H_24G = 24   #¡À24G

  '''
  # High-pass filter cut-off frequency configuration
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
  SHUTDOWN = 4
  
  '''
  Interrupt event
  '''
  X_LOWTHAN_TH = 0     #The acceleration in the x direction is less than the threshold
  X_HIGHERTHAN_TH  = 1  #The acceleration in the x direction is greater than the threshold
  Y_LOWTHAN_TH = 2 # The acceleration in the y direction is less than the threshold
  Y_HIGHERTHAN_TH = 3#  The acceleration in the y direction is greater than the threshold
  Z_LOWTHAN_TH = 4# The acceleration in the z direction is less than the threshold
  Z_HIGHERTHAN_TH = 5# The acceleration in the z direction is greater than the threshold
  EVENT_ERROR = 6# No event

  #Interrupt pin selection
  INT_1 = 0,#int1
  INT_2 = 1,#int2
  
  ERROR                     = -1
  def __init__(self ,bus ,Baud,chip1):
    __reset = 1
    if bus != 0:
      self.i2cbus = smbus.SMBus(bus)
      self.__uart_i2c = I2C_MODE
      
    else:
      self.__uart_i2c = SPI_MODE
    #print("chip1 =")
    #print(chip1)
    self.__chip = chip1


  '''
    @brief Initialize the function
    @return Return 0 indicates a successful initialization, while other values indicates failure and return to error code.
  '''
  def begin(self):
    identifier = 0 
    if(self.__uart_i2c == SPI_MODE):
      identifier = self.read_reg(self.REG_CARD_ID + 0x80)  
    else:
      identifier = self.read_reg(self.REG_CARD_ID)
    #print(identifier)
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
    if(self.__uart_i2c == SPI_MODE):
      identifier = self.read_reg(self.REG_CARD_ID + 0x80)  
    else:
      identifier = self.read_reg(self.REG_CARD_ID)
    return identifier

  '''
    @brief Set the measurement range
    @param range:Range(g)
                 RANGE_100_G =0 #¡À100g
                 RANGE_200_G = 1# ¡À200g
                 LIS331H_6G = 6  #¡À6G
                 LIS331H_12G = 12  #¡À12G
                 LIS331H_24G = 24   #¡À24G
  '''
  def set_range(self,range_r):
    regester = self.REG_CTRL_REG4
    if(self.__uart_i2c == SPI_MODE):
      regester  = self.REG_CTRL_REG4 | 0x80
    reg = self.read_reg(regester)
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
  def set_acquire_rate(self, rate):
    regester = self.REG_CTRL_REG1;
    if(self.__uart_i2c == SPI_MODE):
      regester  = self.REG_CTRL_REG1 | 0x80;
    
    reg = self.read_reg(regester)
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
    #print(reg);
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
                 X_LOWTHAN_TH = 0 <The acceleration in the x direction is less than the threshold>
                 X_HIGHERTHAN_TH  = 1<The acceleration in the x direction is greater than the threshold>
                 Y_LOWTHAN_TH = 2<The acceleration in the y direction is less than the threshold>
                 Y_HIGHERTHAN_TH = 3<The acceleration in the y direction is greater than the threshold>
                 Z_LOWTHAN_TH = 4<The acceleration in the z direction is less than the threshold
                 Z_HIGHERTHAN_TH = 5<The acceleration in the z direction is greater than the threshold>
                 EVENT_ERROR = 6 <No event>
  '''
  def enable_int_event(self,source,event):
    reg = 0
    regester1 = self.REG_INT1_CFG
    regester2 = self.REG_INT2_CFG
    if(self.__uart_i2c == SPI_MODE):
      regester1 = self.REG_INT1_CFG | 0x80
      regester2 = self.REG_INT2_CFG | 0x80
    
    if source == self.INT_1:
      reg = self.read_reg(regester1)
    else:
      reg = self.read_reg(regester2)
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
                  X_LOWTHAN_TH = 0 <The acceleration in the x direction is less than the threshold>
                  X_HIGHERTHAN_TH  = 1<The acceleration in the x direction is greater than the threshold>
                  Y_LOWTHAN_TH = 2<The acceleration in the y direction is less than the threshold>
                  Y_HIGHERTHAN_TH = 3<The acceleration in the y direction is greater than the threshold>
                  Z_LOWTHAN_TH = 4<The acceleration in the z direction is less than the threshold
                  Z_HIGHERTHAN_TH = 5<The acceleration in the z direction is greater than the threshold>
                  EVENT_ERROR = 6 <No event>
    @return true ï¼šproduce
            falseï¼šInterrupt event
  '''
  def get_int1_event(self,event):
    regester = self.REG_INT1_SRC;
    if(self.__uart_i2c == SPI_MODE):
      regester  = self.REG_INT1_SRC | 0x80;
    reg = self.read_reg(regester)
      #print(reg & (1 << source))
      #print(1 << source)
    if (reg & (1 << source)) >= 1:
         return True
    else:
         return False
         
  '''
    @brief Check whether the interrupt event'event' is generated in interrupt 2
    @param event:Interrupt event
                  X_LOWTHAN_TH = 0 <The acceleration in the x direction is less than the threshold>
                  X_HIGHERTHAN_TH  = 1<The acceleration in the x direction is greater than the threshold>
                  Y_LOWTHAN_TH = 2<The acceleration in the y direction is less than the threshold>
                  Y_HIGHERTHAN_TH = 3<The acceleration in the y direction is greater than the threshold>
                  Z_LOWTHAN_TH = 4<The acceleration in the z direction is less than the threshold
                  Z_HIGHERTHAN_TH = 5<The acceleration in the z direction is greater than the threshold>
                  EVENT_ERROR = 6 <No event>
    @return true ï¼šproduce
            falseï¼šInterrupt event
  '''
  def get_int2_event(self,event):
    regester = self.REG_INT2_SRC
    if(self.__uart_i2c == SPI_MODE):
      regester  = self.REG_INT2_SRC | 0x80;
    reg = self.read_reg(regester)
    if (reg & (1 << source)) >= 1:
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
    regester = self.REG_CTRL_REG2
    if(self.__uart_i2c == SPI_MODE):
      regester  = self.REG_CTRL_REG2 | 0x80; 
    reg = self.read_reg(regester)
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
    regester = self.REG_STATUS_REG
    if(self.__uart_i2c == SPI_MODE):
      regester  = self.REG_STATUS_REG | 0x80; 
    reg = self.read_reg(regester)
     # reg = 1
    data = [0,0,0,0,0,0,0]
    offset = 0
    x = 0
    y = 0
    z = 0
    if(reg & 0x01) == 1:
        if(self.__uart_i2c == SPI_MODE):
		       offset = 0x80
     
        data[0] = self.read_reg(self.REG_OUT_X_L+offset)
        data[1] = self.read_reg(self.REG_OUT_X_H+offset)
        data[2] = self.read_reg(self.REG_OUT_Y_L+offset)
        data[3] = self.read_reg(self.REG_OUT_Y_H+offset)
        data[4] = self.read_reg(self.REG_OUT_Z_L+offset)
        data[5] = self.read_reg(self.REG_OUT_Z_H+offset)
        
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
'''
  @brief An example of an i2c interface module
'''
class DFRobot_H3LIS_I2C(DFRobot_LIS): 
  def __init__(self ,bus ,addr):
    self.__addr = addr
    super(DFRobot_H3LIS_I2C, self).__init__(bus,0,1)

  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
        data1 = [0]
        data1[0] = data
        self.i2cbus.write_i2c_block_data(self.__addr ,reg,data1)
        #self.i2cbus.write_byte(self.__addr ,reg)
        #self.i2cbus.write_byte(self.__addr ,data)




  '''
    @brief read the data from the register
    @param reg register address
    @param value read data
  '''
  def read_reg(self, reg):
    self.i2cbus.write_byte(self.__addr,reg)
    time.sleep(0.01)
    rslt = self.i2cbus.read_byte(self.__addr)
    #print(rslt)
    return rslt

class DFRobot_H3LIS_SPI(DFRobot_LIS): 


  def __init__(self ,cs):
    super(DFRobot_H3LIS_SPI, self).__init__(0,cs,1)
    #DFRobot_H3LIS.__init__(0,0)
    #self._busy = GPIO(busy, GPIO.IN)
    self.__cs = GPIO(cs, GPIO.OUT)
    self.__cs.setOut(GPIO.LOW)
    self._spi = SPI(0, 0)
    
  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
     data1 =[reg,data]
     self.__cs.setOut(GPIO.LOW)
     self._spi.transfer(data1)
     self.__cs.setOut(GPIO.HIGH)
     #self._spi.transfer(data)
  '''
    @brief read the data from the register
    @param reg register address
    @param value read data
  '''
  def read_reg(self, reg):
     data1 =[reg]
     self.__cs.setOut(GPIO.LOW)
     self._spi.transfer(data1)
     time.sleep(0.01)
     data = self._spi.readData(1)
     self.__cs.setOut(GPIO.HIGH)
     #print(data)
     return  data[0]
class DFRobot_LIS331HH_I2C(DFRobot_LIS): 
  def __init__(self ,bus ,addr):
    self.__addr = addr
    super(DFRobot_LIS331HH_I2C, self).__init__(bus,0,2)

  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
        data1 = [0]
        data1[0] = data
        self.i2cbus.write_i2c_block_data(self.__addr ,reg,data1)
        #self.i2cbus.write_byte(self.__addr ,reg)
        #self.i2cbus.write_byte(self.__addr ,data)
  '''
    @brief read the data from the register
    @param reg register address
    @param value read data
  '''
  def read_reg(self, reg):
    self.i2cbus.write_byte(self.__addr,reg)
    time.sleep(0.01)
    rslt = self.i2cbus.read_byte(self.__addr)
    #print(rslt)
    return rslt

class DFRobot_LIS331HH_SPI(DFRobot_LIS): 


  def __init__(self ,cs):
    super(DFRobot_LIS331HH_SPI, self).__init__(0,cs,2)
    #DFRobot_H3LIS.__init__(0,0)
    #self._busy = GPIO(busy, GPIO.IN)
    self.__cs = GPIO(cs, GPIO.OUT)
    self.__cs.setOut(GPIO.LOW)
    self._spi = SPI(0, 0)

    #print("LIS331HH")

    
  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
     data1 =[reg,data]
     self.__cs.setOut(GPIO.LOW)
     self._spi.transfer(data1)
     self.__cs.setOut(GPIO.HIGH)
     #self._spi.transfer(data)
  '''
    @brief read the data from the register
    @param reg register address
    @param value read data
  '''
  def read_reg(self, reg):
     data1 =[reg]
     self.__cs.setOut(GPIO.LOW)
     self._spi.transfer(data1)
     time.sleep(0.01)
     data = self._spi.readData(1)
     self.__cs.setOut(GPIO.HIGH)
     #print(data)
     return  data[0]
