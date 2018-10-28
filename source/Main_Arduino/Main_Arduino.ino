void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
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


