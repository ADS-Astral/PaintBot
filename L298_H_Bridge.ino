/* Basic script for running 2 L298 H-Bridges. 

using 2-13 arduino digital pins for control of the H-Bridges and
leaving digital pins 0 & 1 for serial communication*/

// Fixed constants are used here to set pin numbers:

//Front Left Motor
const int EN_A =  2;      // Pin to enable motor 1
const int M1_1 = 3;       // motor1 direction pin (HIGH = FWD)
const int M1_2 = 4;       // motor1 direction pin (HIGH = REV)

//Front Right Motor
const int EN_B =  5;      // Pin to enable motor 2
const int M2_1 = 6;       // motor1 direction pin (HIGH = FWD)
const int M2_2 = 7;       // motor1 direction pin (HIGH = REV)

//Back Left Motor
const int EN_A1 =  8;      // Pin to enable motor 1
const int M3_1 = 9;       // motor1 direction pin (HIGH = FWD)
const int M3_2 = 10;       // motor1 direction pin (HIGH = REV)

//Back Right Motor
const int EN_B1 =  11;      // Pin to enable motor 2
const int M4_1 = 12;       // motor1 direction pin (HIGH = FWD)
const int M4_2 = 13;       // motor1 direction pin (HIGH = REV)

const int increment_time = 1; // time in seconds


// variables will change:

int motor_state = 0;         // variable for reading the pushbutton status

void setup() {
  // initialize the L298-H Bridge pins as outputs:
  
  pinMode(EN_A, OUTPUT);
  pinMode(M1_1, OUTPUT);
  pinMode(M1_2, OUTPUT);
  pinMode(EN_B, OUTPUT);
  pinMode(M2_1, OUTPUT);
  pinMode(M2_2, OUTPUT);

  pinMode(EN_A1, OUTPUT);
  pinMode(M3_1, OUTPUT);
  pinMode(M3_2, OUTPUT);
  pinMode(EN_B1, OUTPUT);
  pinMode(M4_1, OUTPUT);
  pinMode(M4_2, OUTPUT);
}

void loop() {
  
  switch (motor_state) {

  //Forward
  
  case 0:
    
    //Front Left
    digitalWrite(EN_A,HIGH)
    digitalWrite(M1_1,HIGH)
    digitalWrite(M1_2,LOW)
    
    //Front Right
    digitalWrite(EN_B,HIGH)
    digitalWrite(M2_1,HIGH)
    digitalWrite(M2_2,LOW)

    //Back Left
    digitalWrite(EN_A1,HIGH)
    digitalWrite(M3_1,HIGH)
    digitalWrite(M3_2,LOW)
    
    //Back Right
    digitalWrite(EN_B1,HIGH)
    digitalWrite(M4_1,HIGH)
    digitalWrite(M4_2,LOW)
    
    //Run for the duration of 'increment'
    delay(increment*1000);
    break;


    //Reverse

  case 1:
      
       //Front Left
    digitalWrite(EN_A,HIGH)
    digitalWrite(M1_1,LOW)
    digitalWrite(M1_2,HIGH)
    
    //Front Right
    digitalWrite(EN_B,HIGH)
    digitalWrite(M2_1,LOW)
    digitalWrite(M2_2,HIGH)

    //Back Left
    digitalWrite(EN_A1,HIGH)
    digitalWrite(M3_1,LOW)
    digitalWrite(M3_2,HIGH)
    
    //Back Right
    digitalWrite(EN_B1,HIGH)
    digitalWrite(M4_1,LOW)
    digitalWrite(M4_2,HIGH)
    
    //Run for the duration of 'increment'
    delay(increment*1000);
    
    break;
    
  //Default all motors activated  
  default:
       //Front Left
    digitalWrite(EN_A,HIGH)
   
    //Front Right
    digitalWrite(EN_B,HIGH)
    
    //Back Left
    digitalWrite(EN_A1,HIGH)
    
    //Back Right
    digitalWrite(EN_B1,HIGH)
  
    
    //Run for the duration of 'increment'
    delay(increment*1000);
    
    break;
}
  
}