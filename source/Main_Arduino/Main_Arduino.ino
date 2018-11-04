#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pwm.begin();
pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
for (int i=0; i<6; i++){
  pwm.setPWM(i, 0, 160); //(servo, 0, position)}
  }          
}

void loop() {
int data=0;
int servoIndex=0;
int dataArray[6]={-1,-1,-1,-1,-1,-1};
while (dataArray[5]==-1){
    if (Serial.available() > 0) {
                // read the incoming byte:
                 data=Serial.read();
                 dataArray[servoIndex]=map(data,0,240,160,300);
                 servoIndex++;
                 Serial.println(data, DEC);}
                }
  for (int i=0; i<6; i++){
  pwm.setPWM(i, 0, dataArray[i]); //(servo, 0, position)}
  }          
}
