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
  float dataArray[6]={0,0,0,0,0,0};
  int servoIndex=0;
  while (servoIndex<6){
    if (Serial.available() > 0) {
                // read the incoming byte:
                float data = Serial.parseFloat();
                Serial.println(data, DEC);                // say what you got:
                dataArray[servoIndex]=data;
                servoIndex++;
  }}
                for(int i=0; i<6; i++){
                int servoPWM=mapf(dataArray[i],0.0,90.0,150.0,280.0); //cast floating point to nearest int
                pwm.setPWM(i, 0, servoPWM); //(servo, 0, position)}
        }
}

double mapf(double val, double in_min, double in_max, double out_min, double out_max) {
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
