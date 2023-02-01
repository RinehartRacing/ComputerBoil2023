#include <Adafruit_BMP085.h>

/*
  Made on 18 may 2021
  By Amirmohammad Shojaei
  Home
  
*/
#include <Wire.h>

Adafruit_BMP085 bmp1;
Adafruit_BMP085 bmp2;




void TCA9548A(uint8_t bus) //function of TCA9548A
{
  Wire.beginTransmission(0x70);  // TCA9548A address is 0x70
  Wire.write(1 << bus);          // send byte to select bus
  Wire.endTransmission();
}

void setup()
{
  Serial.begin(9600);
  Wire.begin();
  delay(100);

  TCA9548A(0);
  bmp1.begin();        //Initialize HTU21D Sensor

  delay(100);
  TCA9548A(2);
  bmp2.begin();

}

double pressure1;
double temperature1;
double pressure2;
double temperature2;
double diffPressure;
void loop() {
  
  
  TCA9548A(0);
  delay(1000);
  pressure1 = bmp1.readPressure() * 0.0001450377;   //Pressure of BMP180 Sensor 1
  temperature1 = bmp1.readTemperature();
  // Serial.println("\nPressure1: " + pressure1);
  // Serial.println("Temperature1: " + temperature1);

  

  TCA9548A(2);
  delay(1000);
  pressure2 = bmp2.readPressure() * 0.0001450377;   //Pressure of BMP180 Sensor 2 
  temperature2 = bmp2.readTemperature();
  // Serial.println("\nPressure2: " + pressure2);
  // Serial.println("Temperature2: " + temperature2);
  diffPressure = pressure2 - pressure1;
  Serial.println("Differential Pressure: " + String(diffPressure));

}
