/*!
 * @file DFRobot_LIS.cpp
 * @brief Define the basic structure of class DFRobot_LIS 
 * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [fengli](li.feng@dfrobot.com)
 * @version  V1.0
 * @date  2021-1-27
 * @get from https://www.dfrobot.com
 * @https://github.com/DFRobot/DFRobot_LIS
 */

#include <DFRobot_LIS.h>
DFRobot_LIS::DFRobot_LIS(){}

uint8_t DFRobot_LIS::begin(void){


  uint8_t identifier = 0; 
  uint8_t regester = REG_CARD_ID;
  if(_interface == 1){
    regester  = REG_CARD_ID | 0x80;
  }
  uint8_t ret = readReg(regester,&identifier,1);
  DBG(identifier);
  if(identifier == 0x32){
    ret = 0;
  } else if(identifier == 0 || identifier == 0xff){
    DBG("Communication failure");
    ret = 1;
  } else {  
    DBG("the ic is not H3LIS");
    ret = 2;
  }
  return ret;
}

uint8_t DFRobot_LIS::getID(){
  uint8_t identifier; 
  uint8_t regester = REG_CARD_ID;
  if(_interface == 1){
    regester  = REG_CARD_ID | 0x80;
  }
  readReg(regester,&identifier,1);
  return identifier;
}
bool DFRobot_LIS::setRange(eRange_t range){
  uint8_t reg = 0;
  uint8_t regester = REG_CTRL_REG4;
  if(_interface == 1){
    regester  = REG_CTRL_REG4 | 0x80;
  }
  readReg(regester,&reg,1);
  
  
  switch(chip)
  {
    case H3LIS200DL :{
      if(range == eH3lis200dl_100g){
         reg = reg & (~0x10);
         _range = 100;
       } else if(range == eH3lis200dl_200g){
         reg = reg | 0x10;
         _range = 200;
       } else {
         reg = reg & (~0x10);
       }
       break;
      }
    case LIS331HH:{
      switch(range){
       
       case eLis331h_6g :{
         _range = range;
         reg = reg&(~(3<<4));
         break;
       }
       case eLis331h_12g :{
        _range = range;
         reg = reg&(~(3<<4));
         reg = reg | (0x01<<4);
         break;
       }
       case eLis331h_24g : {
         _range = range;
         reg = reg&(~(3<<4));
         reg = reg | (0x03<<4);
         break;
       }
      }
	  break;
    }
  }
  
  
  DBG(reg);
  writeReg(REG_CTRL_REG4,&reg,1);
}



void DFRobot_LIS::setAcquireRate(ePowerMode_t rate)
{
  uint8_t reg = 0;

  uint8_t regester = REG_CTRL_REG1;
  if(_interface == 1){
    regester  = REG_CTRL_REG1 | 0x80;
  }
  readReg(regester,&reg,1);
  switch(rate){
    case ePowerDown_0HZ : {
     reg = reg & (~(0x7 << 5));
     break;
    }
    case eLowPower_halfHZ :{
     reg = reg & (~(0x7 << 5));
     reg = reg | (0x02 << 5);
     break;
    }
    case eLowPower_1HZ :{
     reg = reg & (~(0x7 << 5));
     reg = reg | (0x03 << 5);
     break;
    }
    case eLowPower_2HZ :{
     reg = reg & (~(0x7 << 5));
     reg = reg | (0x04 << 5);
     break;
    }
    case eLowPower_5HZ :{
     reg = reg & (~(0x7 << 5));
     reg = reg | (0x05 << 5);
     break;
    }
    case eLowPower_10HZ :{
     reg = reg & (~(0x7 << 5));
     reg = reg | (0x06 << 5);
     break;
    }
    case eNormal_50HZ :{
     reg = reg & (~(0x7 << 5));
     reg = reg | (0x01 << 5);
     reg = reg & (~(0x3 << 3));
     break;
    }
    case eNormal_100HZ :{
     reg = reg & (~(0x7 << 5));
     reg = reg | (0x01 << 5);
     reg = reg & (~(0x3 << 3));
     reg = reg | (0x01 << 3);
     break;
    }
    case eNormal_400HZ :{
     reg = reg & (~(0x7 << 5));
     reg = reg | (0x01 << 5);
     reg = reg & (~(0x3 << 3));
     reg = reg | (0x02 << 3);
     break;
    }
    case eNormal_1000HZ :{
     reg = reg & (~(0x7 << 5));
     reg = reg | (0x01 << 5);
     reg = reg & (~(0x3 << 3));
     reg = reg | (0x03 << 3);
     break;
    }
  }
  DBG(reg);
  writeReg(REG_CTRL_REG1,&reg,1);
}
void DFRobot_LIS::setInt1Th(uint8_t threshold)
{
    uint8_t reg = (threshold * 128)/_range;
    DBG(reg);
    writeReg(REG_INT1_THS,&reg,1);
}
void DFRobot_LIS::setInt2Th(uint8_t threshold)
{
    uint8_t reg = (threshold * 128)/_range;
    DBG(reg);
    writeReg(REG_INT2_THS,&reg,1);
}
void DFRobot_LIS::enableInterruptEvent(eInterruptSource_t source,eInterruptEvent_t event)
{
  uint8_t reg = 0;

  uint8_t regester1 = REG_INT1_CFG;
  uint8_t regester2 = REG_INT2_CFG;
  if(_interface == 1){
    regester1  = REG_INT1_CFG | 0x80;
    regester2  = REG_INT2_CFG | 0x80;
  }

  if(source == eINT1)
    readReg(regester1,&reg,1);
  else
    readReg(regester2,&reg,1);

  if(reset == 1){
     reg = 0;
     reset = 0;
  }
  switch(event){
    case eXLowThanTh :{
      reg = reg | 0x01;
      break;
    }
    case eXHigherThanTh :{
      reg = reg | 0x02;
      break;
    }
    case eYLowThanTh :{
      reg = reg | 0x04;
      break;
    }
    case eYHigherThanTh :{
      reg = reg | 0x08;
      break;
    }
    case eZLowThanTh :{
      reg = reg | 0x10;
      break;
    }
    case eZHigherThanTh :{
      reg = reg | 0x20;
      break;
    }
  }
  DBG(reg);
  if(source == eINT1)
    writeReg(REG_INT1_CFG,&reg,1);
  else
    writeReg(REG_INT2_CFG,&reg,1);
 
 
}
bool DFRobot_LIS::getInt1Event(eInterruptEvent_t event)
{
  uint8_t reg = 0;
  uint8_t regester = REG_INT1_SRC;
  
  if(_interface == 1){
    regester  = REG_INT1_SRC | 0x80;
  }
  readReg(regester,&reg,1);

  DBG(reg);
  if(reg & (1 << event))  return true;
  return false;
}
bool DFRobot_LIS::getInt2Event(eInterruptEvent_t event)
{
  uint8_t reg = 0;
  uint8_t regester = REG_INT2_SRC;
  if(_interface == 1){
    regester  = REG_INT2_SRC | 0x80;
  }
  readReg(regester,&reg,1);
  DBG(reg);
  if(reg & (1 << event))  return true;
  return false;
}


uint8_t DFRobot_LIS::enableSleep(bool enable)
{
  uint8_t reg = 0;
  uint8_t readRe = 0;

  if(enable == true)
    reg = 3;
  else
    reg = 0;
  writeReg(REG_CTRL_REG5,&reg,1);

  uint8_t regester = REG_CTRL_REG5;
  if(_interface == 1){
    regester  = REG_CTRL_REG5 | 0x80;
  }
  readReg(regester,&readRe,1);
  
  if(reg == readRe)
    return 0;
  else 
    return 1;
}
void DFRobot_LIS::setHFilterMode(eHighPassFilter_t mode){

  uint8_t reg = 0;
  uint8_t regester = REG_CTRL_REG2;
  if(_interface == 1){
    regester  = REG_CTRL_REG2 | 0x80;
  }
  readReg(regester,&reg,1);
  if(mode == eShutDown){
    reg = reg & (~0x10);
    return;
  } else{
    reg = reg | 0x10;
  }
  reg = reg & (~3);
  reg = reg | (uint8_t)mode;
  DBG(reg);
  writeReg(REG_CTRL_REG2,&reg,1);
}



long DFRobot_LIS::readAccX(){
  uint8_t reg = 0;
  uint8_t offset = 0x0;
  uint8_t sensorData[2];
  long a = 0;
  if(_interface == 1){
    offset = 0x80;
     }
  readReg(REG_STATUS_REG+offset,&reg,1);
  readReg(REG_OUT_X_L+offset,&sensorData[0],1);
  readReg(REG_OUT_X_L+1+offset,&sensorData[1],1);
  //Serial.println(_range);
  switch(chip)
  {
    case H3LIS200DL :{
       a = ((int8_t)sensorData[1] *_range)/128;
       break;
      }
    case LIS331HH:{
       
       a = ((int8_t)sensorData[1])*256+sensorData[0];
       #if defined(__AVR__) 
         a = -(a * 1000 * (uint8_t)_range)/(256*128);
       #else 
         a = (a * 1000 * (uint8_t)_range)/(256*128);
       #endif
      break;
    }
  }
  return a;


}
long DFRobot_LIS::readAccY(){
  uint8_t reg = 0;
  uint8_t offset = 0x0;
  uint8_t sensorData[2];
  long a = 0;
  if(_interface == 1){
    offset = 0x80;
     }
  readReg(REG_STATUS_REG+offset,&reg,1);
  readReg(REG_OUT_Y_L+offset,&sensorData[0],1);
  readReg(REG_OUT_Y_L+1+offset,&sensorData[1],1);
  
  switch(chip)
  {
    case H3LIS200DL :{
       a = ((int8_t)sensorData[1] *_range)/128;
       break;
      }
    case LIS331HH:{
       a = ((int8_t)sensorData[1])*256+sensorData[0];
       #if defined(__AVR__) 
         a = -(a * 1000 * (uint8_t)_range)/(256*128);
       #else 
         a = (a * 1000 * (uint8_t)_range)/(256*128);
       #endif
      break;
    }
  }
     return a;


  
}
long DFRobot_LIS::readAccZ(){
  uint8_t reg = 0;
  uint8_t offset = 0x0;
  uint8_t sensorData[2];
  long a = 0;
  if(_interface == 1){
    offset = 0x80;
     }
  readReg(REG_STATUS_REG+offset,&reg,1);
  readReg(REG_OUT_Z_L+offset,&sensorData[0],1);
  readReg(REG_OUT_Z_L+1+offset,&sensorData[1],1);
  
  switch(chip)
  {
    case H3LIS200DL :{
       a = ((int8_t)sensorData[1] *_range)/128;
       break;
      }
    case LIS331HH:{
       a = ((int8_t)sensorData[1])*256+sensorData[0];
       #if defined(__AVR__) 
         a = -(a * 1000 * (uint8_t)_range)/(256*128);
       #else 
         a = (a * 1000 * (uint8_t)_range)/(256*128);
       #endif
      break;
    }
  }
     return a;
}
/*
DFRobot_LIS::sAccel_t DFRobot_LIS::getAcceFromXYZ()
{

  uint8_t reg = 0;
  uint8_t ACCX = 0;
  uint8_t sensorData[3];
  sAccel_t accel;
  uint8_t offset = 0x0;
  uint8_t regester = REG_STATUS_REG;
  if(_interface == 1){
    regester  = REG_STATUS_REG | 0x80;
  }
  readReg(regester,&reg,1);
  if((reg & 0x01) == 1){
     if(_interface == 1){
      offset = 0x80;
     }
     readReg(REG_OUT_X+offset,&sensorData[0],1);
     readReg(REG_OUT_Y+offset,&sensorData[1],1);
     readReg(REG_OUT_Z+offset,&sensorData[2],1);


     float a = ((int8_t)sensorData[0]*_range)/128;
     float b = ((int8_t)sensorData[1]*_range)/128;
     float c = ((int8_t)sensorData[2]*_range)/128;
     accel.acc_x = a;
     accel.acc_y = b;
     accel.acc_z = c;
  }
return accel;

}
*/
bool DFRobot_LIS::getAcceFromXYZ(long &accx,long &accy,long &accz)
{
  uint8_t reg = 0;
  uint8_t sensorData[3];
  uint8_t offset = 0x0;
  uint8_t regester = REG_STATUS_REG;
  long a,b,c;
  if(_interface == 1){
    regester  = REG_STATUS_REG | 0x80;
  }
  readReg(regester,&reg,1);
  if((reg & 0x01) == 1){
    if(_interface == 1){
       offset = 0x80;
    }
   
    readReg(REG_OUT_X_L+offset,&sensorData[0],1);
    readReg(REG_OUT_X_H+offset,&sensorData[1],1);
    readReg(REG_OUT_Y_L+offset,&sensorData[2],1);
    readReg(REG_OUT_Y_H+offset,&sensorData[3],1);
    readReg(REG_OUT_Z_L+offset,&sensorData[4],1);
    readReg(REG_OUT_Z_H+offset,&sensorData[5],1);

    switch(chip)
    {
      case H3LIS200DL :{
         a = ((int8_t)sensorData[1]*_range)/128;
         b = ((int8_t)sensorData[3]*_range)/128;
         c = ((int8_t)sensorData[5]*_range)/128;
         break;
        }
      case LIS331HH:{
         a = ((int8_t)sensorData[1])*256+(int8_t)sensorData[0];
        (a * 1000 * (uint8_t)_range)/(256*128);
         b = ((int8_t)sensorData[3])*256+(int8_t)sensorData[2];
        (b * 1000 * (uint8_t)_range)/(256*128);
         c = ((int8_t)sensorData[5])*256+(int8_t)sensorData[4];
         c = (c * 1000 * (uint8_t)_range)/(256*128);
        break;
      }
    }
    accx = a;
    accy = b;
    accz = c;
    return true;
  }
return false;
}
bool DFRobot_LIS::getSleepState()
{
  return state;
}
void DFRobot_LIS::setSleepFlag(bool into){

   state = into;
}


DFRobot_H3LIS200DL_I2C::DFRobot_H3LIS200DL_I2C(TwoWire * pWire,uint8_t addr)
{
  _deviceAddr = addr;
  _pWire = pWire;
    chip = H3LIS200DL;
}

uint8_t DFRobot_H3LIS200DL_I2C::begin(void)
{
  _pWire->begin();
  return DFRobot_LIS::begin();
}

uint8_t DFRobot_H3LIS200DL_I2C::writeReg(uint8_t reg, const void * pBuf, size_t size)
{
  if(pBuf == NULL){
	  DBG("pBuf ERROR!! : null pointer");
  }
  uint8_t * _pBuf = (uint8_t *)pBuf;
  _pWire->beginTransmission(_deviceAddr);
  _pWire->write(&reg, 1);

  for(uint16_t i = 0; i < size; i++){
    _pWire->write(_pBuf[i]);
  }
  _pWire->endTransmission();
}

uint8_t DFRobot_H3LIS200DL_I2C::readReg(uint8_t reg, void* pBuf, size_t size)
{
  if(pBuf == NULL){
    DBG("pBuf ERROR!! : null pointer");
  }
  uint8_t * _pBuf = (uint8_t *)pBuf;
  _pWire->beginTransmission(_deviceAddr);
  _pWire->write(&reg, 1);
  if( _pWire->endTransmission() != 0){
      return 0;
  }
  _pWire->requestFrom(_deviceAddr, (uint8_t) size);
  for(uint16_t i = 0; i < size; i++){
	  
    _pBuf[i] = _pWire->read();
	//Serial.println(_pBuf[i],HEX);
	  DBG(_pBuf[i]);
  }
  return size;
}







DFRobot_H3LIS200DL_SPI::DFRobot_H3LIS200DL_SPI(uint8_t cs,SPIClass *pSpi)
{
  _pSpi = pSpi;
  _cs = cs;
  chip = H3LIS200DL;
}




uint8_t DFRobot_H3LIS200DL_SPI::begin(void){

  _pSpi->begin();
  pinMode(_cs,OUTPUT);
  digitalWrite(_cs,1);
  _interface = 1;
  return DFRobot_LIS::begin();
}
uint8_t DFRobot_H3LIS200DL_SPI::readReg(uint8_t reg,void * pBuf ,size_t size){
  if(pBuf == NULL){
	  DBG("pBuf ERROR!! : null pointer");
  }
  uint8_t * _pBuf = (uint8_t *)pBuf;
  size_t count = 0;
#if (defined NRF5)
  _pSpi->beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE1));
#else
  _pSpi->beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
#endif
  digitalWrite(_cs,0);
  _pSpi->transfer(reg);
  while(size--) {
    *_pBuf = SPI.transfer(0x00);
    _pBuf++;
    count++;
  }
  DBG(pBuf[0]);
  _pSpi->endTransaction();
  digitalWrite(_cs,1);
  return count;

}

uint8_t  DFRobot_H3LIS200DL_SPI::writeReg(uint8_t reg,const void *pBuf,size_t size){
  if(pBuf == NULL){
	  DBG("pBuf ERROR!! : null pointer");
  }
  uint8_t * _pBuf = (uint8_t *)pBuf;
  _pSpi->beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
  digitalWrite(_cs,0);
  _pSpi->transfer(reg);
  while(size--) {
    _pSpi->transfer(*_pBuf);
    _pBuf ++;
  }

  SPI.endTransaction();
  digitalWrite(_cs,1);
}
DFRobot_LIS331HH_I2C::DFRobot_LIS331HH_I2C(TwoWire * pWire,uint8_t addr)
{
  _deviceAddr = addr;
  _pWire = pWire;
    chip = LIS331HH;
}

uint8_t DFRobot_LIS331HH_I2C::begin(void)
{
  _pWire->begin();
  return DFRobot_LIS::begin();
}

uint8_t DFRobot_LIS331HH_I2C::writeReg(uint8_t reg, const void * pBuf, size_t size)
{
  if(pBuf == NULL){
	  DBG("pBuf ERROR!! : null pointer");
  }
  uint8_t * _pBuf = (uint8_t *)pBuf;
  _pWire->beginTransmission(_deviceAddr);
  _pWire->write(&reg, 1);

  for(uint16_t i = 0; i < size; i++){
    _pWire->write(_pBuf[i]);
  }
  _pWire->endTransmission();
}

uint8_t DFRobot_LIS331HH_I2C::readReg(uint8_t reg, void* pBuf, size_t size)
{
  if(pBuf == NULL){
    DBG("pBuf ERROR!! : null pointer");
  }
  uint8_t * _pBuf = (uint8_t *)pBuf;
  _pWire->beginTransmission(_deviceAddr);
  _pWire->write(&reg, 1);
  if( _pWire->endTransmission() != 0){
      return 0;
  }
  _pWire->requestFrom(_deviceAddr, (uint8_t) size);
  for(uint16_t i = 0; i < size; i++){
	  
    _pBuf[i] = _pWire->read();
  }
  return size;
}

DFRobot_LIS331HH_SPI::DFRobot_LIS331HH_SPI(uint8_t cs,SPIClass *pSpi)
{
  _pSpi = pSpi;
  _cs = cs;
  chip = LIS331HH;
}

uint8_t DFRobot_LIS331HH_SPI::begin(void){

  _pSpi->begin();
  pinMode(_cs,OUTPUT);
  digitalWrite(_cs,1);
  _interface = 1;
  return DFRobot_LIS::begin();
}
uint8_t DFRobot_LIS331HH_SPI::readReg(uint8_t reg,void * pBuf ,size_t size){
  if(pBuf == NULL){
	  DBG("pBuf ERROR!! : null pointer");
  }
  uint8_t * _pBuf = (uint8_t *)pBuf;
  size_t count = 0;


#if (defined NRF5)
  _pSpi->beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE1));
#else
  _pSpi->beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
#endif
  digitalWrite(_cs,0);
  _pSpi->transfer(reg);
  while(size--) {
    *_pBuf = SPI.transfer(0x00);
    _pBuf++;
    count++;
  }
  _pSpi->endTransaction();
  digitalWrite(_cs,1);
  return count;

}

uint8_t  DFRobot_LIS331HH_SPI::writeReg(uint8_t reg,const void *pBuf,size_t size){
  if(pBuf == NULL){
	  DBG("pBuf ERROR!! : null pointer");
  }
  uint8_t * _pBuf = (uint8_t *)pBuf;

  
  _pSpi->beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
  digitalWrite(_cs,0);
  _pSpi->transfer(reg);
  while(size--) {
    _pSpi->transfer(*_pBuf);
    _pBuf ++;
  }

  SPI.endTransaction();
  digitalWrite(_cs,1);
}