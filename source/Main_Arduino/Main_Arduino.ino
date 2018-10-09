class baked //precomputed from python module unless we want to hook them together somehow
{
  public:
  int mazeSolution=0;//hardcoded 2D array of lenghts and timings for mazesolution. Might be a better way to do this using std::Vectors
  int wave=0; //do the wave
  int tiltX=0;// manual mode positions
  int tiltY=0;// manual mode positions
};

class userInterface
{public:

  bool errorHandler(int e){
    //TODO output the error to serial
    };

  bool stateWriter(char ){
    //TODO print the state of the system (positions, ect) to Serial for debugging
    };
  void inputHandler(int key){
    //determine what to do when the user presses a certain key, see example code
    //TODO handle commands to run the solution, reset to the default position, manual yaw and pitch
    };
  };

baked motions; //new pre-baked motions object

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}


void loop() {
  bool run=0;
  //(pseudocode) Serial.onRecieve= UI.inputHandler(serial.recieved)
  //wait for "run" command in this loop
  if (run) mazeSolve(motions.mazeSolution); //run with the main maze solution
}

void motorAngles(int lengthVector){
  //TODO compute the servo angles for each servo based on the required length. Lengths are defined with 0 being fully retracted (deltaL).
  //Audrey, I think this one is yours
}

void servoInterface(int anglesVector){
  //TODO sends the required signals to the servos
  //Kelly this is all you
}

bool mazeSolve(int lengthVector){
  userInterface UI; //define a new userInterface object
  for(obj = var in lengthVector) //TODO build proper array iterator
  {
    timeDelay=obj.time; //get time from the lengthVector
    angles=motorAngles(lengthVector) //compute angles
    servoInterface(angles) //move the servoes
    delay(timeDelay)//wait until the end of the move
    UI.stateWriter(lengthVector) //output our expected lenghts or whatever
  }
  return 1;
  if (error){ //general form for any errors we have
    UI.errorHandler(error); 
    return 0;
  }
}
