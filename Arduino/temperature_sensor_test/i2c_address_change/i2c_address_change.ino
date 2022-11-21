// Simple sketch to read out one register of an I2C device
#define SDA_PORT PORTF
#define SDA_PIN 4 // = A4
#define SCL_PORT PORTF
#define SCL_PIN 5 // = A5
#include <SoftI2CMaster.h>

#define I2C_7BITADDR 0x77 // BMP180
#define MEMLOC 0x0A 

void setup(void) {
    Serial.begin(9600);
    if (!i2c_init()) // Initialize everything and check for bus lockup
        Serial.println("I2C init failed");
}

void loop(void){
    //i2c_rep_start((I2C_7BITADDR<<1)|I2C_READ); // restart for reading
    byte val = i2c_read(false); // read one byte and send NAK to terminate
    //i2c_stop(); // send stop condition
    Serial.println(val);
    delay(100);
}