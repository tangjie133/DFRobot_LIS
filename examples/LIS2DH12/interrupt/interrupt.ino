/**！
 * @file interrupt.ino
 * @brief Interrupt detection
 * @n In this example, the enable eZHigherThanTh interrupt event means when the acceleration in the Z direction exceeds the
 * @n threshold set by the program, the interrupt level can be detected on the interrupt pin int1/int2 we set, and the level change on the
 * @n interrupt pin can be used to determine whether the interrupt occurs. The following are the 6 settable interrupt events：eXHigherThanTh,
 * @n eXLowerThanTh, eYHigherThanTh, eYLowerThanTh, eZHigherThanTh, eZLowerThanTh. For a detailed explanation of each of them,
 * @n please look up the comments of the enableInterruptEvent() function.
 * @n This example needs to connect the int2/int1 pin of the module to the interrupt pin of the motherboard. Default UNO(2), Mega2560(2), 
 * @n       Leonardo(3), microbit(P0),FireBeetle-ESP8266(D6),FireBeetle-ESP32((D6),FireBeetle-M0(6)        
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author [fengli](li.feng@dfrobot.com)
 * @version  V1.0
 * @date  2021-01-16
 * @url https://github.com/DFRobot/DFRobot_LIS
 */
#include <DFRobot_LIS2DH12.h>

//When using I2C communication, use the following program to construct an object by DFRobot_H3LIS200DL_I2C
/*!
 * @brief Constructor 
 * @param pWire I2c controller
 * @param addr  I2C address(0x18/0x19)
 */
DFRobot_LIS2DH12 acce(&Wire,0x18);

//Interrupt generation flag
volatile bool intFlag = false;

void interEvent(){
  intFlag = true;
}

void setup(void){

  Serial.begin(9600);
    //Chip initialization
  while(!acce.begin()){
     delay(1000);
     Serial.println("Initialization failed, please check the connection and I2C address settings");
  }
  //Get chip id
  Serial.print("chip id : ");
  Serial.println(acce.getID(),HEX);
  
  /**
    set range:Range(g)
              eLIS2DH12_2g,/< ±2g>/
              eLIS2DH12_4g,/< ±4g>/
              eLIS2DH12_8g,/< ±8g>/
              eLIS2DH12_16g,/< ±16g>/
  */
  acce.setRange(/*Range = */DFRobot_LIS2DH12::eLIS2DH12_16g);


  /**
    Set data measurement rate：
      ePowerDown_0Hz 
      eLowPower_1Hz 
      eLowPower_10Hz 
      eLowPower_25Hz 
      eLowPower_50Hz 
      eLowPower_100Hz
      eLowPower_200Hz
      eLowPower_400Hz
  */
  acce.setAcquireRate(/*Rate = */DFRobot_LIS2DH12::eLowPower_10Hz);
  
  #if defined(ESP32) || defined(ESP8266)
  //The D6 pin is used as the interrupt pin by default, and other non-conflicting pins can also be selected as the external interrupt pin.
  attachInterrupt(digitalPinToInterrupt(D6)/*Query the interrupt number of the D6 pin*/,interEvent,CHANGE);
  #elif defined(ARDUINO_SAM_ZERO)
  //The pin 5 is used as the interrupt pin by default, and other non-conflicting pins can also be selected as the external interrupt pin.
  attachInterrupt(digitalPinToInterrupt(5)/*Query the interrupt number of the pin 5*/,interEvent,CHANGE);
  #else
  /*    The Correspondence Table of AVR Series Arduino Interrupt Pins And Terminal Numbers
   * ---------------------------------------------------------------------------------------
   * |                                        |  DigitalPin  | 2  | 3  |                   |
   * |    Uno, Nano, Mini, other 328-based    |--------------------------------------------|
   * |                                        | Interrupt No | 0  | 1  |                   |
   * |-------------------------------------------------------------------------------------|
   * |                                        |    Pin       | 2  | 3  | 21 | 20 | 19 | 18 |
   * |               Mega2560                 |--------------------------------------------|
   * |                                        | Interrupt No | 0  | 1  | 2  | 3  | 4  | 5  |
   * |-------------------------------------------------------------------------------------|
   * |                                        |    Pin       | 3  | 2  | 0  | 1  | 7  |    |
   * |    Leonardo, other 32u4-based          |--------------------------------------------|
   * |                                        | Interrupt No | 0  | 1  | 2  | 3  | 4  |    |
   * |--------------------------------------------------------------------------------------
   */
  /*                      The Correspondence Table of micro:bit Interrupt Pins And Terminal Numbers
   * ---------------------------------------------------------------------------------------------------------------------------------------------
   * |             micro:bit                       | DigitalPin |P0-P20 can be used as an external interrupt                                     |
   * |  (When using as an external interrupt,      |---------------------------------------------------------------------------------------------|
   * |no need to set it to input mode with pinMode)|Interrupt No|Interrupt number is a pin digital value, such as P0 interrupt number 0, P1 is 1 |
   * |-------------------------------------------------------------------------------------------------------------------------------------------|
   */
  attachInterrupt(/*Interrupt No*/0,interEvent,CHANGE);//Open the external interrupt 0, connect INT1/2 to the digital pin of the main control: 
     //UNO(2), Mega2560(2), Leonardo(3), microbit(P0).
  #endif

  /**
    Set the threshold of interrupt source 1 interrupt
    threshold:Threshold(g)
   */
  acce.setInt1Th(/*Threshold = */6);//Unit: g

  /*!
    Enable interrupt
    Interrupt pin selection:
      eINT1 = 0,/<int1 >/
      eINT2,/<int2>/
    Interrupt event selection:
      eXLowerThanTh ,/<The acceleration in the x direction is less than the threshold>/
      eXHigherThanTh ,/<The acceleration in the x direction is greater than the threshold>/
      eYLowerThanTh,/<The acceleration in the y direction is less than the threshold>/
      eYHigherThanTh,/<The acceleration in the y direction is greater than the threshold>/
      eZLowerThanTh,/<The acceleration in the z direction is less than the threshold>/
      eZHigherThanTh,/<The acceleration in the z direction is greater than the threshold>/
   */
  acce.enableInterruptEvent(/*int pin*/DFRobot_LIS2DH12::eINT1,/*interrupt event = */DFRobot_LIS2DH12::eZHigherThanTh);
  
  delay(1000);
}

void loop(void){
    //Get the acceleration in the three directions of xyz
    //The mearsurement range is ±100g or ±200g, set by setRange() function.
    Serial.print("Acceleration x: "); 
    Serial.print(acce.readAccX());
    Serial.print(" mg \ty: ");
    Serial.print(acce.readAccY());
    Serial.print(" mg \tz: ");
    Serial.print(acce.readAccZ());
    Serial.println(" mg");
    delay(300);
   //The interrupt flag is set
   if(intFlag == true){
      //Check whether the interrupt event is generated in interrupt 1
     if(acce.getInt1Event(DFRobot_LIS2DH12::eZHigherThanTh)){
       Serial.println("The acceleration in the z direction is greater than the threshold");
      }
      intFlag = false;
   }
}
