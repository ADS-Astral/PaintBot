


// variables will change:

String incomingByte; // for incoming serial data
int motorState =0;

// Variables that remain the same

const int increment_time = 1; //Time in seconds

void setup() {
  
  // initialize the L298-H Bridge pins as outputs:
  
  DDRD = B11111100; // set PORTD (digital 7~2) to outputs
  DDRB = B11111111; // set PORTB (digital 13~8) to outputs

   Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
}


void loop() {

// Read serial until terminator; convert input to int for switch statement.
// Switch controls direction of the vehicle.

  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.readStringUntil('Q');
    motorState = incomingByte.toInt();

     // say what you got:
    Serial.print("I received: ");
    Serial.println(motorState);
  
    switch (motorState) {

    //Forward
  
    case 0:

      PORTD=B01101100; // Pins 7-2
      PORTB=B11011011; // Pins 13-8 
      
      //Run for the duration of 'increment'
      delay(increment_time*1000);
      break;


      //Reverse

      case 1:

        PORTB=B11101101; // Pins 7-2
        PORTD=B10110100; // Pins 13-8
      
        //Run for the duration of 'increment'
        delay(increment_time*1000);
        
        break;
        
      //Strafe Left
      case 2:

        PORTB=B11101011; // Pins 7-2
        PORTD=B01110100; // Pins 13-8
        
        //Run for the duration of 'increment'
        delay(increment_time*1000);
        break;


      //Strafe Right

      case 3:
          
        PORTB=B11011101; // Pins 7-2
        PORTD=B10101100; // Pins 13-8
        
        //Run for the duration of 'increment'
        delay(increment_time*1000);
        
      break;

      // Rotation Left
      case 4:

        PORTB=B11011101; // Pins 7-2
        PORTD=B01110100; // Pins 13-8
        
        //Run for the duration of 'increment'
        delay(increment_time*1000);
        break;


      //Rotation Right

      case 5:
          
        PORTB=B11101011; // Pins 7-2
        PORTD=B10101100; // Pins 13-8
        
        //Run for the duration of 'increment'
        delay(increment_time*1000);
        
      break;
    }
      
   }
}
