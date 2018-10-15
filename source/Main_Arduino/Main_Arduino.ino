void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}


void loop() {
if (Serial.available() > 0) {
                // read the incoming byte:
                int data = Serial.read();

                // say what you got:
                Serial.print("I received: ");
                Serial.println(data, DEC);
                //wait for us to get 6 values
                servoInterface(data) #tell the servos to move
        }
}

void servoInterface(int anglesVector){
  //TODO sends the required signals to the servos
  //Kelly this is all you
}


