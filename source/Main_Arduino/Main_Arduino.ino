#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
int servoMap[2][6]={
  {235,225,250,255,245,190},
  {390,390,470,445,400,340,}
};
int oldData[6]={265,240,250,255,245,220};
int deltas[6]={0,0,0,0,0,0};
int substeps=50;
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
                 deltas[servoIndex]=(dataArray[servoIndex]-oldData[servoIndex])/substeps;
                 servoIndex++;
                 Serial.println(angle/4, DEC);}
                }
                
  for (int j=0; j<substeps; j++){
    for (int i=0; i<6; i++){
      PWMstep=oldData[i]+j*deltas[i];
  pwm.setPWM(i, 0, PWMStep); //(servo, 0, position)}
  delay(2);
  }          
  }
  
}
