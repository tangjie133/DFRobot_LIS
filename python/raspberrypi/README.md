# DFRobot_H3LIS
The H3LIS200DL is a low-power high performance 3-axis linear accelerometer <br>
belonging to the “nano” family, with digital I2C/SPI <br>
serial interface standard output. <br>
The device features ultra-low-power operational <br>
modes that allow advanced power saving and <br>
smart sleep-to-wakeup functions.<br>
The H3LIS200DL has dynamically user selectable full scales of ±100g/±200g and is <br>
capable of measuring accelerations with output <br>
data rates from 0.5 Hz to 1 kHz.<br>
The H3LIS200DL is available in a small thin <br>
plastic land grid array package (LGA) and is <br>
guaranteed to operate over an extended <br>
temperature range from -40 °C to +85 °C.<br>


## DFRobot_H3LIS Library for RaspberryPi
---------------------------------------------------------

Provide an RaspberryPi library to get Three-axis acceleration by reading data from H3LIS200DL.

## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

## Summary

Provide an RaspberryPi library to get Three-axis acceleration by reading data from H3LIS200DL.

## Installation

To use this library, first download the library file, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.

## Methods

```python
  '''
    @brief Initialize the function
    @return Return 0 indicates a successful initialization, while other values indicates failure and return to error code.
  '''
  begin(self)
  
  '''
    @brief get chip id
    @return returns the 8 bit serial number
  '''
  get_id(self)

  '''
    @brief Set the measurement range
    @param range:Range(g)
               RANGE_100_G =0 # ±100g
               RANGE_200_G = 1# ±200g
  '''
  set_range(self,range_r)

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
  set_acquire_rate(self, rate)


  '''
    @brief Set the threshold of interrupt source 1 interrupt
    @param threshold:Threshold(g)
  '''
  set_int1_th(self,threshold)

  '''
    @brief Set interrupt source 2 interrupt generation threshold
    @param threshold:Threshold(g)
  '''
  set_int2_th(self,threshold)
  
  '''
    @brief Enable interrupt
    @source Interrupt pin selection
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
  enable_int_event(self,source,event)

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
    @return True ：产生了此事件
            False：未产生此事件
  '''
  get_int1_event(self,event)
         
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
    @return True ：产生了此事件
            False：未产生此事件
  '''
  get_int2_event(self,source)

  '''
    @brief Enable sleep wake function
    @param enable:True(enable)/False(disable)
  '''
  enable_sleep(self, enable)
  
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
  set_filter_mode(self,mode)

  '''
    @brief Get the acceleration in the three directions of xyz
    @return Three-axis acceleration 
  '''
  read_acce_xyz(self)

```

## Compatibility

MCU                | Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | -----
raspberry pi 3             |      √         |            |             | 




## History

- data 2021-1-26
- version V1.0


## Credits

Written by(li.feng@dfrobot.com), 2021. (Welcome to our [website](https://www.dfrobot.com/))
