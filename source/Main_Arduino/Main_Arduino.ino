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
  int dataArray[]={0,0,0,0,0,0};
  int servoIndex=0;
  while (servoIndex<6){
    if (Serial.available() > 0) {
                // read the incoming byte:
                int data = Serial.read();
                // say what you got:
                Serial.println(data, DEC);
                dataArray[servoIndex]=data;
                servoIndex++;
  }}

                for(int i=0; i<5; i++){
                int servoPWM=map(dataArray[i],0,90,150,280);
                pwm.setPWM(i, 0, servoPWM); //(servo, 0, position)}
        }
}
