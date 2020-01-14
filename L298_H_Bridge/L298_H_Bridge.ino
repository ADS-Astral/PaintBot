/**
 * Basic script for running 2 L298 H-Bridges
 * using 2-13 arduino digital pins for control of the H-Bridges and
 * leaving digital pins 0 & 1 for serial communication.
 */

// Fixed constants are used here to set pin numbers:

//Front Left Motor
const int EN_A = 2;      // Pin to enable motor 1
const int M1_1 = 3;       // motor1 direction pin (HIGH = FWD)
const int M1_2 = 4;       // motor1 direction pin (HIGH = REV)

//Front Right Motor
const int EN_B = 7;      // Pin to enable motor 2
const int M2_1 = 5;       // motor1 direction pin (HIGH = FWD)
const int M2_2 = 6;       // motor1 direction pin (HIGH = REV)

//Back Left Motor
const int EN_A1 = 8;      // Pin to enable motor 1
const int M3_1 = 9;       // motor1 direction pin (HIGH = FWD)
const int M3_2 = 10;       // motor1 direction pin (HIGH = REV)

//Back Right Motor
const int EN_B1 = 13;      // Pin to enable motor 2
const int M4_1 = 11;       // motor1 direction pin (HIGH = FWD)
const int M4_2 = 12;       // motor1 direction pin (HIGH = REV)

float increment_time = 0; // time in seconds


// variables will change:

String incomingByte; // for incoming serial data
int motorState = 0;

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
    pinMode(0, OUTPUT);

    Serial.begin(57600); // opens serial port, sets data rate to 9600 bps
}


void loop() {

    digitalWrite(0, HIGH);
    // Read serial until terminator; convert input to int for switch statement.
    // Switch controls direction of the vehicle.

    if (Serial.available() > 0) {
        // read the incoming byte:
        incomingByte = Serial.readStringUntil('Q');
//        incomingByte = Serial.readString();
        motorState = incomingByte.toInt();

        // say what you got:
        Serial.print(motorState);

        switch (motorState) {

            default: // Stop
                //Front Left
                digitalWrite(EN_A, HIGH);
                digitalWrite(M1_1, LOW);
                digitalWrite(M1_2, LOW);

                //Front Right
                digitalWrite(EN_B, HIGH);
                digitalWrite(M2_1, LOW);
                digitalWrite(M2_2, LOW);

                //Back Left
                digitalWrite(EN_A1, HIGH);
                digitalWrite(M3_1, LOW);
                digitalWrite(M3_2, LOW);

                //Back Right
                digitalWrite(EN_B1, HIGH);
                digitalWrite(M4_1, LOW);
                digitalWrite(M4_2, LOW);
                break;

            case 1: // Forward

                //Front Left
                digitalWrite(EN_A, HIGH);
                digitalWrite(M1_1, HIGH);
                digitalWrite(M1_2, LOW);

                //Front Right
                digitalWrite(EN_B, HIGH);
                digitalWrite(M2_1, HIGH);
                digitalWrite(M2_2, LOW);

                //Back Left
                digitalWrite(EN_A1, HIGH);
                digitalWrite(M3_1, HIGH);
                digitalWrite(M3_2, LOW);

                //Back Right
                digitalWrite(EN_B1, HIGH);
                digitalWrite(M4_1, HIGH);
                digitalWrite(M4_2, LOW);

                //Run for the duration of 'increment'
//                delay(increment_time*1000);
                break;

            case 2: // Reverse

                //Front Left
                digitalWrite(EN_A, HIGH);
                digitalWrite(M1_1, LOW);
                digitalWrite(M1_2, HIGH);

                //Front Right
                digitalWrite(EN_B, HIGH);
                digitalWrite(M2_1, LOW);
                digitalWrite(M2_2, HIGH);

                //Back Left
                digitalWrite(EN_A1, HIGH);
                digitalWrite(M3_1, LOW);
                digitalWrite(M3_2, HIGH);

                //Back Right
                digitalWrite(EN_B1, HIGH);
                digitalWrite(M4_1, LOW);
                digitalWrite(M4_2, HIGH);

                //Run for the duration of 'increment'
                //delay(increment_time*1000);

                break;

            case 666: // Default all motors activated
                //Front Left
                digitalWrite(EN_A, HIGH);

                //Front Right
                digitalWrite(EN_B, HIGH);

                //Back Left
                digitalWrite(EN_A1, HIGH);

                //Back Right
                digitalWrite(EN_B1, HIGH);


                //Run for the duration of 'increment'
                //delay(increment_time*1000);

                break;
        }
        delay(increment_time * 1000);
    }
}