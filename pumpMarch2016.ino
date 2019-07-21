// 48 Vertical Syringe Pump
// Written Taylor Howell
// March 2016

// pump specifications
double motorFullSteps = 200*5.2; //gear ratio motor 5.2:1
double microstepping = 8; //1,2,8,16
double lead = 1.25; //mm
double steps = motorFullSteps*microstepping; // total number of steps per revolution due to microstepping
double displacementPerStep = lead/steps; // mm
double diameter = 4.7; //mm, diameter of BD 1cc syringe
double area = pow((diameter/2),2)*3.141592; //mm^2, internal area of 1cc syringe

double flushVolume = 100; //microliters
double flushRate = 1800; //microliters per hour
double movingFlushVolume = 5; //microliters
double movingFlushRate = 60; //microliters per hour

double rate = 0;
double volume = 0;

String rate_str = "";
String volume_str = "";
String numberOfHours_str = "";
int directionPin = 8;
int stepPin = 9;

char s; // initial value for exit task command
String command;
int i = 0;
int k = 0;


// specific flow rate function
void flow(double rate, double volume){
  double verticalDistance = volume/area; //mm, total vertical displacement needed dispense desired volume from 1cc syringe
  float numberSteps = verticalDistance/displacementPerStep; // the number of steps required to traveled the desired vertical displacement in one hour
  double totaltime = (volume/rate)*3.6*pow(10,6);
  double timeStep = (totaltime/numberSteps)/2; //ms, each pulse has a time delay inbetween HIGH and LOW, so the timestep here is half; half between high and low, the other half after low
  float currentSteps = 0;
  
  Serial.println("*Flow Mode Selected*");
  Serial.print("Flowing "); Serial.print(volume); Serial.print(" uL at: "); Serial.print(rate); Serial.println(" uL/Hr");
  Serial.println("Flowing...");
  if(timeStep >= 1){
  while(currentSteps <= numberSteps){
    digitalWrite(stepPin,HIGH);
    delay(timeStep);
      s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
    digitalWrite(stepPin,LOW);
    delay(timeStep);
    currentSteps = currentSteps + 1;
    s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
  }
  
  }
  if( timeStep < 1){
    timeStep = timeStep*1000;
    while(currentSteps <= numberSteps){
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(timeStep);
      s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
    digitalWrite(stepPin,LOW);
    delayMicroseconds(timeStep);
    currentSteps = currentSteps + 1;
    s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
  }
  
  }
  Serial.println("Flow Complete"); 
}

// Up Function
void up(){
  Serial.println("Moving Up...");
  float currentSteps = 0;
    while(currentSteps < 10*steps){
      digitalWrite(directionPin, LOW);
      digitalWrite(stepPin,HIGH);
      delayMicroseconds(100);
      digitalWrite(stepPin,LOW);
      delayMicroseconds(100);
      currentSteps = currentSteps + 1;
      s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
    }
    digitalWrite(directionPin,HIGH);
    currentSteps = 0; 
    Serial.println("Up complete");
  }
  
void down(){
  Serial.println("Moving Down...");
  float currentSteps = 0;
    while(currentSteps < 10*steps){
      digitalWrite(directionPin, HIGH);
      digitalWrite(stepPin,HIGH);
      delayMicroseconds(100);
      digitalWrite(stepPin,LOW);
      delayMicroseconds(100);
      currentSteps = currentSteps + 1;
      s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
    }
    currentSteps = 0; 
    Serial.println("Down complete");
  }

//Flush mode: .1mL at 30micro/minute
void Flush(){
  double volume = flushVolume;
  double rate = flushRate;
  double verticalDistance = volume/area; //mm, total vertical displacement needed dispense desired volume from 1cc syringe
  double numberSteps = verticalDistance/displacementPerStep; // the number of steps required to traveled the desired vertical displacement in one hour
  double totaltime= ((volume/rate)*3.6*pow(10,6)); //ms, each pulse has a time delay inbetween HIGH and LOW, so the timestep here is half; half between high and low, the other half after low
  double timeStep = (totaltime/numberSteps)/2;//ms
  float currentSteps = 0;
  
  Serial.println("*Flush Mode Selected*");
  Serial.println("Flushing at "); Serial.print(volume); Serial.print(" uL at: "); Serial.print(rate); Serial.println(" uL/Hr");
  if(timeStep >= 1){
  while(currentSteps <= numberSteps){
    digitalWrite(stepPin,HIGH);
    delay(timeStep);
      s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
    digitalWrite(stepPin,LOW);
    delay(timeStep);
    currentSteps = currentSteps + 1;
    s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
  }
  
  }
  if( timeStep < 1){
    timeStep = timeStep*1000;
    while(currentSteps <= numberSteps){
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(timeStep);
      s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
    digitalWrite(stepPin,LOW);
    delayMicroseconds(timeStep);
    currentSteps = currentSteps + 1;
    s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
  }
  
  }
  Serial.println("Flow Complete"); 
}
//moving Flush mode: 5 micro at 1micro/min 
void movingFlush(){
  double volume = movingFlushVolume;
  double rate = movingFlushRate;
  double verticalDistance = volume/area; //mm, total vertical displacement needed dispense desired volume from 1cc syringe
  double numberSteps = verticalDistance/displacementPerStep; // the number of steps required to traveled the desired vertical displacement in one hour
  double totaltime = ((volume/rate)*3.6*pow(10,6)); 
  double timeStep= (totaltime/numberSteps)/2; //ms, each pulse has a time delay inbetween HIGH and LOW, so the timestep here is half; half between high and low, the other half after low
  float currentSteps = 0;
  
  Serial.println("*Moving Flush Mode Selected*");
  Serial.println("Moving flush at "); Serial.print(volume); Serial.print(" uL at: "); Serial.print(rate); Serial.println(" uL/Hr");
  
  if(timeStep >= 1){
  while(currentSteps <= numberSteps){
    digitalWrite(stepPin,HIGH);
    delay(timeStep);
      s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
    digitalWrite(stepPin,LOW);
    delay(timeStep);
    currentSteps = currentSteps + 1;
    s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
  }
  
  }
  if( timeStep < 1){
    timeStep = timeStep*1000;
    while(currentSteps <= numberSteps){
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(timeStep);
      s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
    digitalWrite(stepPin,LOW);
    delayMicroseconds(timeStep);
    currentSteps = currentSteps + 1;
    s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
  }
  
  }
  Serial.println("Flow Complete"); 
}

void experiment(double experimentRate,float numberOfHours){
  rate = experimentRate; //microliters per hour
  volume = experimentRate*numberOfHours; 
  double verticalDistance = volume/area; //mm, total vertical displacement needed dispense desired volume from 1cc syringe
  float numberSteps = verticalDistance/displacementPerStep; // the number of steps required to traveled the desired vertical displacement in one hour
  double totaltime = (volume/rate)*3.6*pow(10,6);
  double timeStep = (totaltime/numberSteps)/2; //ms, each pulse has a time delay inbetween HIGH and LOW, so the timestep here is half; half between high and low, the other half after low
  float currentSteps = 0;
  
  Serial.println("*Experiment Mode Selected*");
  Serial.print("Flowing at a rate of: "); Serial.print(experimentRate); Serial.print(" uL/Hr for  "); Serial.print(numberOfHours); Serial.println(" hours");
  Serial.println("Flowing...");
  if(timeStep >= 1){
  while (k < numberOfHours){
  while(currentSteps <= numberSteps/numberOfHours/30){ //number of steps in two minutes
    digitalWrite(stepPin,HIGH);
    delay(timeStep);
      s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
    digitalWrite(stepPin,LOW);
    delay(timeStep);
    currentSteps = currentSteps + 1;
    s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
  }
  Serial.println("Waiting for 58 minutes");
  while(i < 58*60){
    delay(1000); // delay for 1 second 58*60 times
    i = i + 1;
  }
  i = 0;
  k = k + 1;
  currentSteps = 0;
  Serial.print(k); Serial.println(" hours complete");
  Serial.println("Flowing");
  }
  Serial.println("Experiment Complete"); 
}
if(timeStep < 1){
  timeStep = timeStep*1000;
  while (k < numberOfHours){
  while(currentSteps <= numberSteps/numberOfHours/30){ //number of steps in two minutes
    digitalWrite(stepPin,HIGH);
    delay(timeStep);
      s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
    digitalWrite(stepPin,LOW);
    delay(timeStep);
    currentSteps = currentSteps + 1;
    s = Serial.read();
      if( s == 's'){
        stopTask();
        break;
      }
  }
  Serial.println("Waiting for 58 minutes");
  while(i < 58*60){
    delay(1000); // delay for 1 second 58*60 times
    i = i + 1;
  }
  i = 0;
  k = k + 1;
  currentSteps = 0;
  Serial.print(k); Serial.println(" hours complete");
  Serial.println("Flowing");
  }
  Serial.println("Experiment Complete"); 
}
  k = 0;
}

void stopTask(){
  digitalWrite(stepPin, LOW);
  digitalWrite(directionPin, HIGH);
  Serial.println("Process Terminated");
}

void setup(){
    Serial.begin(9600);
    pinMode(directionPin,OUTPUT); // direction pin (again may want to put it somewhere else)
    pinMode(stepPin,OUTPUT); // step pin
    digitalWrite(directionPin,HIGH);
    digitalWrite(stepPin,LOW);
    Serial.println("Please type: up, down, flow, flush, moving flush or experiment");
}

void loop(){
  if( Serial.available()){
    command = Serial.readString();
    if (command == "up"){
      up();
    }
    
    if (command == "down"){
      down();
    }
    
    if (command == "flush"){
      Flush();
    }
    if (command == "moveflush"){
      movingFlush();
    }
    if (command == "flow"){
      Serial.println("Enter Flow Rate (uL/Hr)");
      while( Serial.available() == 0){}
      rate_str = Serial.readString();
      Serial.print("Flow Rate: "); Serial.print(rate_str); Serial.println(" uL/Hr");
      Serial.println("Enter Volume (uL)");
      while(Serial.available() == 0){}
      volume_str = Serial.readString();
      Serial.print("Volume: "); Serial.println(volume_str);
      flow(rate_str.toFloat(),volume_str.toFloat());
    }
    if (command == "experiment"){
      Serial.println("Experiment: Enter Flow Rate (uL/Hr)");
      while( Serial.available() == 0){}
      rate_str = Serial.readString();
      Serial.print("Flow Rate: "); Serial.print(rate_str); Serial.println(" uL/Hr");
      Serial.println("Enter Hours ( > 1) for experiment");
      while(Serial.available() == 0){}
      numberOfHours_str = Serial.readString();
      Serial.print("Hours: "); Serial.println(numberOfHours_str);
      experiment(rate_str.toFloat(),numberOfHours_str.toFloat()); 
    }
  }
}
