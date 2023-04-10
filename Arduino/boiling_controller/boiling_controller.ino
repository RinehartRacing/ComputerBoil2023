#include <Adafruit_BMP085.h>
#include <Wire.h>
#define FLUIDPIN A0
Adafruit_BMP085 bmp1;
Adafruit_BMP085 bmp2;
int koolanceRelay = 4;
int solenoidRelay = 3;
int pumpRelay = 5;
double pressure1;
double temperature1;
double pressure2;
double temperature2;
double diffPressure;
bool pumpStatus;
// 3.3 Fluid Level Parameters
double SLOPE = 11;
double YINT = 321;
/* 
5V Parameters
double SLOPE 17.473
double YINT 493.36
*/
// defines variables
long duration;
double distance;
//Flow Rate Variables
byte sensorInterrupt = 0;  // 0 = digital pin 2
byte sensorPin = 2;
// The hall-effect flow sensor outputs approximately 4.5 pulses per second per
// litre/minute of flow.
float calibrationFactor = 4.5;
volatile byte pulseCount;
float flowRate;
unsigned long oldTime;

void TCA9548A(uint8_t bus)  //function of TCA9548A
{
  Wire.beginTransmission(0x70);  // TCA9548A address is 0x70
  Wire.write(1 << bus);          // send byte to select bus
  Wire.endTransmission();
}
void pulseCounter() {
  pulseCount++;  //Every time this function is called, increment "count" by 1
}
void setup() {
  Serial.begin(115200);
  Wire.begin();
  delay(100);

  TCA9548A(0);
  bmp1.begin();  //Initialize HTU21D Sensor

  delay(100);
  TCA9548A(2);
  bmp2.begin();

  pinMode(koolanceRelay, OUTPUT);
  pinMode(solenoidRelay, OUTPUT);
  pinMode(pumpRelay, OUTPUT);

  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);

  pulseCount = 0;
  flowRate = 0.0;
  oldTime = 0;
  pumpStatus = false;
}

void loop() {
  if (Serial.available() > 0) {
    String code = Serial.readString();
    if (code.equals("FILTER")) {
      pumpStatus = !pumpStatus;
      if (pumpStatus) {
        digitalWrite(pumpRelay, HIGH);
      } else {
        digitalWrite(pumpRelay, LOW);
      }
    }
  }
  // Read values
  // Read temperature
  // Serial.println("Reading Temperature");
  TCA9548A(0);
  // delay(1000);
  String packet = "";
  temperature1 = bmp1.readTemperature();
  packet += "T " + (String)temperature1 + " ";
  // Read inside pressure
  // Serial.println("Reading Inside Pressure");
  bmp1.begin();
  pressure1 = bmp1.readPressure() * 0.0001450377;  //Pressure of BMP180 Sensor 1
  packet += "PI " + (String)pressure1 + " ";
  // Read outside pressure
  // Serial.println("Reading Outside Pressure");
  TCA9548A(2);
  // delay(1000);
  bmp2.begin();
  pressure2 = bmp2.readPressure() * 0.0001450377;  //Pressure of BMP180 Sensor 2
  packet += "PO " + (String)pressure2 + " ";
  // Read Flow Rate
  // Serial.println("Reading Flow Rate");
  if ((millis() - oldTime) > 1000)  // Only process counters once per second
  {
    detachInterrupt(sensorInterrupt);
    flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
    oldTime = millis();
    flowRate = flowRate * 0.2199693;

    // Print the flow rate for this second in litres / minute
    // Serial.println("Gallons/min");

    // Reset the pulse counter so we can start incrementing again
    pulseCount = 0;

    // Enable the interrupt again now that we've finished sending output
    attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
  }
  //Start the math
  // flowRate = (flowRate * 60) / 3785.412;         //Convert seconds to minutes, and ml to gallons
  //Flow rate is in gallons per minute
  // delay(100);
  // Serial.println(packet);


  // Read Fluid Level
  // Serial.println("Reading Fluid Level");
  float reading;
  float length;
  reading = analogRead(FLUIDPIN);
  length = (reading - YINT) / SLOPE;
  packet += "FR " + String(flowRate, 2) + " ";
  packet += "FL " + (String)length;
  Serial.println(packet);
  if ((pressure1 - pressure2) > 2.5) {
    digitalWrite(solenoidRelay, HIGH);
  } else {
    digitalWrite(solenoidRelay, LOW);
  }
  if ((pressure1 - pressure2) > 0.05) {
    digitalWrite(koolanceRelay, HIGH);
  } else {
    digitalWrite(koolanceRelay, LOW);
  }
  // if(testBool){
  //   digitalWrite(koolanceRelay, HIGH);
  //   digitalWrite(solenoidRelay, HIGH);
  //   digitalWrite(pumpRelay, HIGH);
  // }
  // else{
  //   digitalWrite(koolanceRelay, LOW);
  //   digitalWrite(solenoidRelay, LOW);
  //   digitalWrite(pumpRelay, LOW);
  // }
  // Serial.println("");
  // delay(1000);
}
