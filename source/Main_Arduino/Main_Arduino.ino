#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
int servoMap[2][6]={
  {160,168,178,150,190,165},
  {315,325,395,315,400,320,}
};

void setup() {
  // put your setup code here, to run once:
Serial.begin(19200);
pwm.begin();
pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
for (int i=0; i<6; i++){
  pwm.setPWM(i, 0, servoMap[0][i]); //(servo, 0, position)}
  }          
}

void loop() {
float data=0.0;
int servoIndex=0;
int dataArray[6]={-1,-1,-1,-1,-1,-1};
while (dataArray[5]==-1){
    if (Serial.available() > 0) {
                // read the incoming byte:
                 data=Serial.readStringUntil('\n').toInt();
                 int angle=int(data*4.0);
                 dataArray[servoIndex]=map(angle,0,360,servoMap[0][servoIndex],servoMap[1][servoIndex]);
                 servoIndex++;
                 Serial.println(angle, DEC);}
                }
  for (int i=0; i<6; i++){
  pwm.setPWM(i, 0, dataArray[i]); //(servo, 0, position)}
  }          
}
