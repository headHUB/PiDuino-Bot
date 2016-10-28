// connect serial 2.0
// using NewPing lib

#include <Ultrasonic.h>
#include <Servo.h>

//pi control
const int forwardPin = 8;

//Motor A
const int dir1PinA = 7;  // IN1
const int dir2PinA = 5;  // IN2
const int speedPinA = 6; // ENA

//motor B
const int dir1PinB = 4;  // IN3
const int dir2PinB = 2;  // IN4
const int speedPinB = 3; // ENB

//motor speed etc.
int speed = 255;
int halfspeed = 150;
int dir; 
int motor;
int time = 5000;

//servo
const int servoPin = 9;
int servoPos = 0;
const int servoMin = 20;
const int servoMax = 160;
const int servoMiddle = 90;
Servo myServo;

//range sensor
Ultrasonic ultrasonic(12,13);
const int trigger=12;
const int echo=13;
//range/direction
int leftscanval, centerscanval, rightscanval, ldiagonalscanval, rdiagonalscanval;
char choice;
const int distancelimit = 35; //Distance limit for obstacles in front           
const int sidedistancelimit = 22; //Minimum distance in cm to obstacles at both sides (the robot will allow a shorter distance sideways)
const int diagonaldistancelimit = 26;
//command control direction
//String commanddirection = 'stop';

//distance, myServo turning direction
int distance;
int numcycles = 0;
char turndirection; //Gets 'l', 'r' or 'f' depending on which direction is obstacle free
const int turntime = 350; //Time the robot spends turning (miliseconds)
int thereis;

// command direction
String commanddirection = "."; // movement direction received from pi
int commandint = 0;


void setup(){
  pinMode (dir1PinA, OUTPUT); 
  pinMode (dir2PinA, OUTPUT); 
  pinMode (speedPinA, OUTPUT); 
  pinMode (dir1PinB, OUTPUT); 
  pinMode (dir2PinB, OUTPUT); 
  pinMode (speedPinB, OUTPUT);
  myServo.attach(servoPin);
  myServo.write(servoMiddle);
  Serial.begin(9600);
  Serial.println("READY");
}

// movement functions
void go(){ 
  analogWrite (speedPinA, speed); 
  analogWrite (speedPinB, speed);
  digitalWrite (dir1PinA , HIGH); 
  digitalWrite (dir2PinA, LOW); 
  digitalWrite (dir1PinB, HIGH); 
  digitalWrite (dir2PinB, LOW);  
}

void backwards(){
  analogWrite (speedPinA, speed); 
  analogWrite (speedPinB, speed);
  digitalWrite (dir1PinA, LOW); 
  digitalWrite (dir2PinA, HIGH); 
  digitalWrite (dir1PinB, LOW); 
  digitalWrite (dir2PinB, HIGH);
}

void turnleft(){
  analogWrite (speedPinA, speed); 
  analogWrite (speedPinB, speed);
  digitalWrite (dir1PinA, HIGH); 
  digitalWrite (dir2PinA, LOW); 
  digitalWrite (dir1PinB, LOW); 
  digitalWrite (dir2PinB, HIGH);
}

void turnright(){
  analogWrite (speedPinA, speed); 
  analogWrite (speedPinB, speed);
  digitalWrite (dir1PinA, LOW); 
  digitalWrite (dir2PinA, HIGH); 
  digitalWrite (dir1PinB, HIGH); 
  digitalWrite (dir2PinB, LOW);
}

void goleft(){
  analogWrite (speedPinA, speed); 
  analogWrite (speedPinB, halfspeed);
  digitalWrite (dir1PinA, HIGH); 
  digitalWrite (dir2PinA, LOW); 
  digitalWrite (dir1PinB, HIGH); 
  digitalWrite (dir2PinB, LOW);
}

void goright(){
  analogWrite (speedPinA, halfspeed); 
  analogWrite (speedPinB, speed);
  digitalWrite (dir1PinA, HIGH); 
  digitalWrite (dir2PinA, LOW); 
  digitalWrite (dir1PinB, HIGH); 
  digitalWrite (dir2PinB, LOW);
}

void stopmove(){
  analogWrite (speedPinA, 0); 
  analogWrite (speedPinB, 0);
  digitalWrite (dir1PinA, LOW); 
  digitalWrite (dir2PinA, LOW); 
  digitalWrite (dir1PinB, LOW); 
  digitalWrite (dir2PinB, LOW);
} 

// sensor functions
int watch(){
  long howfar;
  digitalWrite(trigger,LOW);
  delayMicroseconds(5);                                                                              
  digitalWrite(trigger,HIGH);
  delayMicroseconds(15);
  digitalWrite(trigger,LOW);
  howfar=pulseIn(echo,HIGH);
  howfar=howfar*0.01657; //how far away is the object in cm
  return round(howfar);
}

void lookaround(){
  distance = watch();
  Serial.println(distance);
  myServo.write(140);  //left?
  delay(100);
  distance = watch();
  Serial.println(distance);
  myServo.write(servoMiddle);  //middle
  delay(100);
  distance = watch();
  Serial.println(distance);
  myServo.write(40);
  delay(100);
  distance = watch();
  Serial.println(distance);
  myServo.write(servoMiddle);
  delay(100);
}


void loop(){
  // read all serial data, act only on last byte
  while(Serial.available() > 0){
    commandint = Serial.read();
  }
  // act on the received command
  if(commandint == 10){    // stop
    //myServo.write(50);
    stopmove();
    delay(50);
    commandint = 0;
    //Serial.println(commandint);
  }
  else if(commandint == 2){ // left
    goleft();
    delay(50);
    //Serial.println(commandint);
  }
  else if(commandint == 3){ // forward
    go();
    delay(50);
    //Serial.println(commandint);
  }
  else if(commandint == 4){ // left
    goright();
    delay(50);
    //Serial.println(commandint);
  }
  else if(commandint == 5){ // left
    turnleft();
    delay(50);
    //Serial.println(commandint);
  }
  else if(commandint == 6){ // back
    backwards();
    delay(50);
    //Serial.println(commandint);
  }
  else if(commandint == 7){ // right
    turnright();
    delay(50);
    //Serial.println(commandint);
  }
  else{
    delay(100);
    distance = watch();
    delay(100);
    Serial.println(distance);
    delay(100);
  }
//  else{   //do stop and watch state here
//    delay(150);
//    distance = watch();
//    Serial.println(distance);
//    delay(150);
//  }
}
