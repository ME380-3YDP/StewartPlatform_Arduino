#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pwm.begin();
pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
}

void loop() {
if (Serial.available() > 0) {
                // read the incoming byte:
                int data = Serial.read();

                // say what you got:
                Serial.println(data, DEC);
                //TODO wait for us to get 6 values, put them into dataArray
                for(int i=0; i<5 i++){
                pwm.setPWM(i, 0, dataArray[i]); //(servo, 0, position)}
        }
}


@todo make this better