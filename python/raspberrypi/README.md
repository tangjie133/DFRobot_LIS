# DFRobot_LIS
The H3LIS200DL is a low-power high performance 3-axis linear accelerometer 
belonging to the “nano” family, with digital I2C/SPI 
serial interface standard output. <br>
The device features ultra-low-power operational 
modes that allow advanced power saving and 
smart sleep-to-wakeup functions.<br>
The H3LIS200DL has dynamically user selectable full scales of ±100g/±200g and is 
capable of measuring accelerations with output 
data rates from 0.5 Hz to 1 kHz.<br>
The H3LIS200DL is available in a small thin 
plastic land grid array package (LGA) and is 
guaranteed to operate over an extended 
temperature range from -40 °C to +85 °C.<br>

The LIS331HH is an ultra low-power high 
performance high full-scale three axes linear 
accelerometer belonging to the “nano” family, with 
digital I2C/SPI serial interface standard output. 
The device features ultra low-power operational 
modes that allow advanced power saving and 
smart sleep to wake-up functions. 
The LIS331HH has dynamically user selectable 
full scales of ±6g/±12g/±24g and it is capable of 
measuring accelerations with output data rates 
from 0.5 Hz to 1 kHz. The self-test capability 
allows the user to check the funct

The IIS2DLPC is an ultra-low-power high-performance 
three-axis linear accelerometer with digital I²C/SPI 
output interface which leverages on the robust and 
mature manufacturing processes already used for the 
production of micromachined accelerometers.<br>
The IIS2DLPC has user-selectable full scales of 
±2g/±4g/±8g/±16g and is capable of measuring 
accelerations with output data rates from 1.6 Hz to 
1600 Hz.<br>

The LIS2DW12 is an ultra-low-power high-performance three-axis linear
accelerometer belonging to the “femto” family which leverages on the robust and
mature manufacturing processes already used for the production of micromachined
accelerometers.
The LIS2DW12 has user-selectable full scales of ±2g/±4g/±8g/±16g and is capable of
measuring accelerations with output data rates from 1.6 Hz to 1600 Hz.

CHIP                | Work Well    | Work Wrong  | Remarks
------------------ | :----------: | :----------| -----
H3LIS200DL       |      √       |              |             
LIS331HH      |      √       |              |   
LIS2DW12       |      √       |              |             
IIS2DLPC      |      √       |              |              

## DFRobot_LIS Library for RaspberryPi
---------------------------------------------------------

Provide an RaspberryPi library to get Three-axis acceleration by reading data from H3LIS200DL and LIS331HH.

## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

## Summary

Provide an RaspberryPi library to get Three-axis acceleration by reading data from H3LIS200DL and LIS331HH.

## Installation

下载DFRobot_LIS文件到树莓派文件目录下,然后运行下面两行命令行，使用此传感器:
```
cd DFRobot_LIS/python/raspberry/examples/LIS331HH/get_acceleration
python get_acceleration.py
```


## Methods(H3LIS200DL and LIS331HH)

```python
  '''
    @brief Initialize the function
    @return return True(成功)/False(失败)
  '''
  def begin(self)
  
  '''
    @brief get chip id
    @return 8 bit serial number
  '''
  def get_id(self)

  '''
    @brief Set the measurement range
    @param range Range(g)
                 H3LIS200DL_100G = 100 #±100G
                 H3LIS200DL_200G = 200 #±200G
                 LIS331HH_6G     #±6G
                 LIS331HH_12G    #±12G
                 LIS331HH_24G    #±24G
  '''
  def set_range(self,range_r)

  '''
    @brief Set data measurement rate
    @param rate rate(HZ)
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
  def set_acquire_rate(self, rate)

  '''
    @brief Set the threshold of interrupt source 1 interrupt
    @param threshold Threshold(g)
  '''
  def set_int1_th(self,threshold)

  '''
    @brief Set interrupt source 2 interrupt generation threshold
    @param threshold Threshold(g)
  '''
  def set_int2_th(self,threshold)
  
  '''
    @brief Enable interrupt
    @source Interrupt pin selection
             INT_1 = 0,/<int pad 1 >/
             INT_2,/<int pad 2>/
    @param event Interrupt event selection
             X_LOWERTHAN_TH     = 0x1<The acceleration in the x direction is less than the threshold>
             X_HIGHERTHAN_TH  = 0x2<The acceleration in the x direction is greater than the threshold>
             Y_LOWERTHAN_TH     = 0x4<The acceleration in the y direction is less than the threshold>
             Y_HIGHERTHAN_TH  = 0x8<The acceleration in the y direction is greater than the threshold>
             Z_LOWERTHAN_TH     = 0x10<The acceleration in the z direction is less than the threshold
             Z_HIGHERTHAN_TH  = 0x20<The acceleration in the z direction is greater than the threshold>
             EVENT_ERROR      = 0 <No event>
  '''
  def enable_int_event(self,source,event)

  '''
    @brief Check whether the interrupt event'event' is generated in interrupt 1
    @param event Interrupt event
             X_LOWERTHAN_TH     = 0x1<The acceleration in the x direction is less than the threshold>
             X_HIGHERTHAN_TH  = 0x2<The acceleration in the x direction is greater than the threshold>
             Y_LOWERTHAN_TH     = 0x4<The acceleration in the y direction is less than the threshold>
             Y_HIGHERTHAN_TH  = 0x8<The acceleration in the y direction is greater than the threshold>
             Z_LOWERTHAN_TH     = 0x10<The acceleration in the z direction is less than the threshold
             Z_HIGHERTHAN_TH  = 0x20<The acceleration in the z direction is greater than the threshold>
             EVENT_ERROR      = 0 <No event>
    @return True ：产生了此事件
            False：未产生此事件
  '''
  def get_int1_event(self,event)
         
  '''
    @brief Check whether the interrupt event'event' is generated in interrupt 2
    @param event Interrupt event
             X_LOWERTHAN_TH     = 0x1<The acceleration in the x direction is less than the threshold>
             X_HIGHERTHAN_TH  = 0x2<The acceleration in the x direction is greater than the threshold>
             Y_LOWERTHAN_TH     = 0x4<The acceleration in the y direction is less than the threshold>
             Y_HIGHERTHAN_TH  = 0x8<The acceleration in the y direction is greater than the threshold>
             Z_LOWERTHAN_TH     = 0x10<The acceleration in the z direction is less than the threshold
             Z_HIGHERTHAN_TH  = 0x20<The acceleration in the z direction is greater than the threshold>
             EVENT_ERROR      = 0 <No event>
    @return True ：产生了此事件
            False：未产生此事件
  '''
  def get_int2_event(self,source)

  '''
    @brief Enable sleep wake function
    @param enable True(enable)/False(disable)
  '''
  def enable_sleep(self, enable)
  
  '''
    @brief Set data filtering mode
    @param mode Four modes
                CUTOFF_MODE1 = 0
                CUTOFF_MODE2 = 1
                CUTOFF_MODE3 = 2
                CUTOFF_MODE4 = 3
     eg：在50HZ的频率下,选择eCutOffMode1,滤波后的频率为 1 HZ
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
  def set_filter_mode(self,mode)

  '''
    @brief Get the acceleration in the three directions of xyz
    @return Three-axis acceleration 
  '''
  def read_acce_xyz(self)

```

## Methods(LIS2DW12 and IIS2DLPC)

```python
  '''
     @brief Initialize the function
     @return True(初始化成功)/Fasle(初始化失败)
  '''
  def begin(self):
  
  '''
     @brief Get chip id
     @return 8 bit serial number
  '''
  def get_id(self):

  '''
     @brief Software reset to restore the value of all registers to the default value
  '''
  def soft_reset(self):
    
  '''
     @brief Set the measurement range
     @param range Range(g)
                 RANGE_2G     #±2g
                 RANGE_4G     #±4g
                 RANGE_8G     #±8g
                 RANGE_16G    #±16g
  '''
  def set_range(self,range_r):
    
  '''
     @brief Choose whether to continuously let the chip collect data
     @param enable  true(continuous update)/false( output registers not updated until MSB and LSB read)
  '''
  def contin_refresh(self,enable):
  
  '''
    @brief Set the filter processing mode
    @param path path of filtering
                LPF          #Low pass filter
                HPF          #High pass filter
  '''
  def set_filter_path(self,path):

  '''
    @brief Set the  bandwidth of the data
    @param bw bandwidth
                RATE_DIV_2   #RATE/2 (up to RATE = 800 Hz, 400 Hz when RATE = 1600 Hz)
                RATE_DIV_4   #RATE/4 (High Power/Low power)
                RATE_DIV_10  #RATE/10 (HP/LP)
                RATE_DIV_20  #RATE/20 (HP/LP)
  '''
  def set_filter_bandwidth(self,bw):
    
  '''
     @brief Set power mode
     @param mode 16 power modes to choose from
               HIGH_PERFORMANCE_14BIT          #High-Performance Mode
               CONT_LOWPWR4_14BIT              #Continuous measurement,Low-Power Mode 4(14-bit resolution)
               CONT_LOWPWR3_14BIT              #Continuous measurement,Low-Power Mode 3(14-bit resolution)
               CONT_LOWPWR2_14BIT              #Continuous measurement,Low-Power Mode 2(14-bit resolution)
               CONT_LOWPWR1_12BIT              #Continuous measurement,Low-Power Mode 1(12-bit resolution)
               SING_LELOWPWR4_14BIT            #Single data conversion on demand mode,Low-Power Mode 4(14-bit resolution)
               SING_LELOWPWR3_14BIT            #Single data conversion on demand mode,Low-Power Mode 3(14-bit resolution
               SING_LELOWPWR2_14BIT            #Single data conversion on demand mode,Low-Power Mode 2(14-bit resolution)
               SING_LELOWPWR1_12BIT            #Single data conversion on demand mode,Low-Power Mode 1(12-bit resolution)
               HIGHP_ERFORMANCELOW_NOISE_14BIT #High-Performance Mode,Low-noise enabled
               CONT_LOWPWRLOWNOISE4_14BIT      #Continuous measurement,Low-Power Mode 4(14-bit resolution,Low-noise enabled)
               CONT_LOWPWRLOWNOISE3_14BIT      #Continuous measurement,Low-Power Mode 3(14-bit resolution,Low-noise enabled)
               CONT_LOWPWRLOWNOISE2_14BIT      #Continuous measurement,Low-Power Mode 2(14-bit resolution,Low-noise enabled)
               CONT_LOWPWRLOWNOISE1_12BIT      #Continuous measurement,Low-Power Mode 1(14-bit resolution,Low-noise enabled)
               SINGLE_LOWPWRLOWNOISE4_14BIT    #Single data conversion on demand mode,Low-Power Mode 4(14-bit resolution),Low-noise enabled
               SINGLE_LOWPWRLOWNOISE3_14BIT    #Single data conversion on demand mode,Low-Power Mode 3(14-bit resolution),Low-noise enabled
               SINGLE_LOWPWRLOWNOISE2_14BIT    #Single data conversion on demand mode,Low-Power Mode 2(14-bit resolution),Low-noise enabled
               SINGLE_LOWPWRLOWNOISE1_12BIT    #Single data conversion on demand mode,Low-Power Mode 1(12-bit resolution),Low-noise enabled
  '''
  def set_power_mode(self,mode):
    
  '''
     @brief Set data measurement rate
     @param rate rate
                 RATE_OFF          #测量关闭
                 RATE_1HZ6         #1.6hz,仅在低功耗模式下使用
                 RATE_12HZ5        #12.5hz
                 RATE_25HZ         
                 RATE_50HZ         
                 RATE_100HZ        
                 RATE_200HZ        
                 RATE_400HZ        #仅在High-Performance mode下使用
                 RATE_800HZ        #仅在High-Performance mode下使用
                 RATE_1600HZ       #仅在High-Performance mode下使用
                 SETSWTRIG         #软件触发单次测量
  '''
  def set_data_rate(self, rate):
    
  '''
     @brief 设置自由落体时间,也可以称作自由落体样本个数，只有产生足够多的自由落体样本，才会产生自由落体事件
     @param dur duration,范围:0~31
     @n time = dur * (1/rate)(unit:s)
     |                                  参数与时间之间的线性关系的示例                                                           |
     |------------------------------------------------------------------------------------------------------------------------|
     |                |                     |                          |                          |                           |
     |  Data rate     |       25 Hz         |         100 Hz           |          400 Hz          |         = 800 Hz          |
     |------------------------------------------------------------------------------------------------------------------------|
     |   time         |dur*(1s/25)= dur*40ms|  dur*(1s/100)= dur*10ms  |  dur*(1s/400)= dur*2.5ms |  dur*(1s/800)= dur*1.25ms |
     |------------------------------------------------------------------------------------------------------------------------|
  '''
  def set_free_fall_dur(self,dur):

  
  '''
    @brief Set the interrupt source of the int1 pin
    @param event  Several interrupt events, after setting, when an event is generated, a level transition will be generated on the int1 pin
              DOUBLE_TAP    #双击事件
              FREEFALL      #自由落体事件
              WAKEUP        #唤醒事件
              SINGLE_TAP    #单击事件
              IA6D          #在正面朝上/朝下/朝左/朝右/朝前/朝后 的状态发生改变的事件
    
  '''
  def set_int1_event(self,event):
    
  '''
     @brief 设置唤醒持续时间,在setActMode()函数使用eDetectAct的检测模式时,芯片在被唤醒后,会持续一段时间以正常速率采集数据
     @n 然后便会继续休眠,以12.5hz的频率采集数据
     @param dur  duration,范围:0~3
     @n time = dur * (1/rate)(unit:s)
     |                                  参数与时间之间的线性关系的示例                                                           |
     |------------------------------------------------------------------------------------------------------------------------|
     |                |                     |                          |                          |                           |
     |  Data rate     |       25 Hz         |         100 Hz           |          400 Hz          |         = 800 Hz          |
     |------------------------------------------------------------------------------------------------------------------------|
     |   time         |dur*(1s/25)= dur*40ms|  dur*(1s/100)= dur*10ms  |  dur*(1s/400)= dur*2.5ms |  dur*(1s/800)= dur*1.25ms |
     |------------------------------------------------------------------------------------------------------------------------|
  '''
  def set_wakeup_dur(self,dur):
  
  '''
    @brief 设置运动检测的模式,第一种模式不会去检测模块是否在运动，第二种模式在设置后芯片会以较低的频率测量数据,以降低功耗
    @n 在检测到运动后会恢复到正常频率,第三种只会检测模块是否处于睡眠状态
    @param mode 运动检测模式
                NO_DETECTION         #No detection
                DETECT_ACT           #Detect movement,the chip automatically goes to 12.5 Hz rate in the low-power mode
                DETECT_STATMOTION    #Detect Motion, the chip detects acceleration below a fixed threshold but does not change either rate or operating mode
  '''
  def set_act_mode(self,mode):

  '''
    @brief Set the wake-up threshold,某个方向的加速度大于此值时,会触发wake-up事件
    @param th threshold ,unit:mg,数值是在量程之内
  '''
  def set_wakeup_threshold(self,th):
    
  '''
    @brief Set to detect tap events in the Z direction
    @param enable Ture(使能点击检测\False(禁用点击检测)
  '''
  def enable_tap_detection_on_z(self, enable):
  
  '''
    @brief Set to detect tap events in the Y direction
    @param enable Ture(使能点击检测\False(禁用点击检测)
  '''
  def enable_tap_detection_on_y(self, enable):

    
  '''
    @brief Set to detect tap events in the X direction
    @param enable Ture(使能点击检)\False(禁用点击检)
  '''
  def enable_tap_detection_on_x(self, enable):

  '''
    @brief Set the tap threshold in the X direction
    @param th Threshold(g),Can only be used in the range of ±2g
  '''
  def set_tap_threshold_on_x(self,th):
  
  '''
    @brief Set the tap threshold in the Y direction
    @param th Threshold(g),Can only be used in the range of ±2g
  '''
  def set_tap_threshold_on_y(self,th):
    
  '''
    @brief Set the tap threshold in the Z direction
    @param th Threshold(g),Can only be used in the range of ±2g
  '''
  def set_tap_threshold_on_z(self,th):
    
  '''
     @brief Duration of maximum time gap for double-tap recognition. When double-tap 
     @n recognition is enabled, this register expresses the maximum time between two 
     @n successive detected taps to determine a double-tap event.
     @param dur  duration,范围:0~15
     @n time = dur * (1/rate)(unit:s)
     |                                  参数与时间之间的线性关系的示例                                                           |
     |------------------------------------------------------------------------------------------------------------------------|
     |                |                     |                          |                          |                           |
     |  Data rate     |       25 Hz         |         100 Hz           |          400 Hz          |         = 800 Hz          |
     |------------------------------------------------------------------------------------------------------------------------|
     |   time         |dur*(1s/25)= dur*40ms|  dur*(1s/100)= dur*10ms  |  dur*(1s/400)= dur*2.5ms |  dur*(1s/800)= dur*1.25ms |
     |------------------------------------------------------------------------------------------------------------------------|
  '''
  def set_tap_dur(self,dur):
  
  '''
    @brief Set the tap detection mode,检测单击或者单击双击都检测
    @param mode  点击检测模式
                     ONLY_SINGLE        #检测单击
                     BOTH_SINGLE_DOUBLE #检测单击和双击
  '''
  def set_tap_mode(self,mode):
  
  '''
    @brief Set Thresholds for 4D/6D，当转动的阈值大于指定角度时,就发生方向转变的事件
    @param degree   DEGREES_80   #80°
                    DEGREES_70   #70°
                    DEGREES_60   #60°
                    DEGREES_50   #50°
  '''
  def set_6d_threshold(self,degree):
    
  '''
    @brief 选择在中断2引脚产生的中断事件
    @param event  Several interrupt events, after setting, when an event is generated, a level transition will be generated on the int2 pin
                  SLEEP_CHANGE  #Enable routing of SLEEP_STATE on INT2 pad
                  SLEEP_STATE   #0x80 Sleep change status routed to INT2 pad
  '''
  def set_int2_event(self,event):
  
  '''
    @brief Read the acceleration in the x direction
    @return Acceleration data from x(mg),测量的量程为±2g,±4g,±8g或±16g,通过set_range()函数设置
  '''
  def read_acc_x(self):

  '''
    @brief Read the acceleration in the y direction
    @return  Acceleration data from y(mg),测量的量程为±2g,±4g,±8g或±16g,通过set_range()函数设置
  '''
  def read_acc_y(self):

  '''
    @brief Read the acceleration in the z direction
    @return Acceleration data from z(mg),测量的量程为±2g,±4g,±8g或±16g,通过set_range()函数设置
  '''
  def read_acc_z(self):
  
  '''
    @brief 检测是否有运动产生
    @return True(产生运动)/False(传感器未运动)
  '''
  def act_detected(self):
      
  '''
    @brief 自由落体运动检测
    @return True(检测到自由落体运动)/False(未检测到自由落体运动)
  '''
  def free_fall_detected(self):
    
  '''
    @brief 检测芯片在正面朝上/朝下/朝左/朝右/朝前/朝后（即6D）的状态下是否发生方向的变化
    @return True(a change in position is detected)/False(no event detected)
  '''
  def ori_change_detected(self):
      
  '''
     @brief 该函数仅用于6D（正面朝上/朝下/朝左/朝右/朝前/朝后）状态下，能获取传感器相对于z轴正向的朝向
     @return      X_DOWN   #X is now down
               X_UP     #X is now up
               Y_DOWN   #Y is now down
               Y_UP     #Y is now up
               Z_DOWN   #Z is now down
               Z_UP     #Z is now up
  '''
  def get_oriention(self):
     
  '''
    @brief 点击检测,能检测是发生的双击,还是单击
    @return   S_TAP       #single tap
              D_TAP       #double tap
              NO_TAP,     #没有点击产生
  '''
  def tap_detect(self):

  '''
    @brief 点击方向的源头检测
    @return     DIR_X_UP   #在X 正方向发生的点击事件
                DIR_X_DOWN #在X 负方向发生的点击事件
                DIR_Y_UP   #在Y 正方向发生的点击事件
                DIR_Y_DOWN #在Y 负方向发生的点击事件
                DIR_Z_UP   #在Z 正方向发生的点击事件
                DIR_Z_DOWN #在Z 负方向发生的点击事件
  '''
  def get_tap_direction(self):
   
  '''
    @brief 唤醒的运动方向检测
    @return    DIR_X  #X方向的运动唤醒芯片
               DIR_Y  #Y方向的运动唤醒芯片
               DIR_Z  #Z方向的运动唤醒芯片
               eDirError,
  '''
  def get_wake_up_dir(self):

  '''
    @brief In Single data conversion on demand mode,请求测量一次数据
  '''
  def demand_data(self):
```
## Compatibility

MCU                | Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | -----
Raspberry Pi              |      √         |            |             | 



## History

- data 2021-1-26
- version V1.0


## Credits

Written by(li.feng@dfrobot.com), 2021. (Welcome to our [website](https://www.dfrobot.com/))
