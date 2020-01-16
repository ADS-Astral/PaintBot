
//Front Left Motor
const int EN_A  = 2;       // Pin to enable motor 1
const int M1_1  = 3;       // motor1 direction pin (HIGH = FWD)
const int M1_2  = 4;       // motor1 direction pin (HIGH = REV)
//Front Right Motor
const int EN_B  = 7;       // Pin to enable motor 2
const int M2_1  = 5;       // motor1 direction pin (HIGH = FWD)
const int M2_2  = 6;       // motor1 direction pin (HIGH = REV)
//Back Left Motor
const int EN_A1 = 8;       // Pin to enable motor 1
const int M3_1  = 9;       // motor1 direction pin (HIGH = FWD)
const int M3_2  = 10;      // motor1 direction pin (HIGH = REV)
//Back Right Motor
const int EN_B1 = 13;      // Pin to enable motor 2
const int M4_1  = 11;      // motor1 direction pin (HIGH = FWD)
const int M4_2  = 12;      // motor1 direction pin (HIGH = REV)

// States (or directions) of the motor
const int STATE_STOP        = 0;
const int STATE_FORWARD     = 1;
const int STATE_BACKWARD    = 2;
const int STATE_LEFT        = 3;
const int STATE_RIGHT       = 4;


void setup() { // todo: bypass writing pins using PORTB

    // Initialize the L298-H Bridge pins as outputs:
    pinMode(EN_A,   OUTPUT);
    pinMode(M1_1,   OUTPUT);
    pinMode(M1_2,   OUTPUT);
    pinMode(EN_B,   OUTPUT);
    pinMode(M2_1,   OUTPUT);
    pinMode(M2_2,   OUTPUT);
    pinMode(EN_A1,  OUTPUT);
    pinMode(M3_1,   OUTPUT);
    pinMode(M3_2,   OUTPUT);
    pinMode(EN_B1,  OUTPUT);
    pinMode(M4_1,   OUTPUT);
    pinMode(M4_2,   OUTPUT);
    pinMode(0,      OUTPUT);

    // Open serial port to particular data rate in BPS
    Serial.begin(9600);
    Serial.println("H-Bridge Motor Control ready!");
    Serial.flush();
}


void loop() {

    if (Serial.available()) {

        // Fetch incoming byte as state
        char state = Serial.read();
        // Transmit state of motor
        Serial.print(state);

        switch (state) { // Switch controls direction of the vehicle.

            default:
            case STATE_STOP: {
                // Front Left
                digitalWrite(EN_A, HIGH);
                digitalWrite(M1_1, LOW);
                digitalWrite(M1_2, LOW);
                // Front Right
                digitalWrite(EN_B, HIGH);
                digitalWrite(M2_1, LOW);
                digitalWrite(M2_2, LOW);
                // Back Left
                digitalWrite(EN_A1, HIGH);
                digitalWrite(M3_1, LOW);
                digitalWrite(M3_2, LOW);
                // Back Right
                digitalWrite(EN_B1, HIGH);
                digitalWrite(M4_1, LOW);
                digitalWrite(M4_2, LOW);
                break;
            }
            case STATE_FORWARD: {
                // Front Left
                digitalWrite(EN_A, HIGH);
                digitalWrite(M1_1, HIGH);
                digitalWrite(M1_2, LOW);
                // Front Right
                digitalWrite(EN_B, HIGH);
                digitalWrite(M2_1, HIGH);
                digitalWrite(M2_2, LOW);
                // Back Left
                digitalWrite(EN_A1, HIGH);
                digitalWrite(M3_1, HIGH);
                digitalWrite(M3_2, LOW);
                // Back Right
                digitalWrite(EN_B1, HIGH);
                digitalWrite(M4_1, HIGH);
                digitalWrite(M4_2, LOW);
                break;
            }
            case STATE_BACKWARD: {
                // Front Left
                digitalWrite(EN_A, HIGH);
                digitalWrite(M1_1, LOW);
                digitalWrite(M1_2, HIGH);
                // Front Right
                digitalWrite(EN_B, HIGH);
                digitalWrite(M2_1, LOW);
                digitalWrite(M2_2, HIGH);
                // Back Left
                digitalWrite(EN_A1, HIGH);
                digitalWrite(M3_1, LOW);
                digitalWrite(M3_2, HIGH);
                // Back Right
                digitalWrite(EN_B1, HIGH);
                digitalWrite(M4_1, LOW);
                digitalWrite(M4_2, HIGH);
                break;
            }
            case STATE_LEFT: {
                // Front Left
                digitalWrite(EN_A, HIGH);
                digitalWrite(M1_1, LOW);
                digitalWrite(M1_2, HIGH);
                // Front Right
                digitalWrite(EN_B, HIGH);
                digitalWrite(M2_1, HIGH);
                digitalWrite(M2_2, LOW);
                // Back Left
                digitalWrite(EN_A1, HIGH);
                digitalWrite(M3_1, HIGH);
                digitalWrite(M3_2, LOW);
                // Back Right
                digitalWrite(EN_B1, HIGH);
                digitalWrite(M4_1, LOW);
                digitalWrite(M4_2, HIGH);
                break;
            }
            case STATE_RIGHT: {
                // Front Left
                digitalWrite(EN_A, HIGH);
                digitalWrite(M1_1, HIGH);
                digitalWrite(M1_2, LOW);
                // Front Right
                digitalWrite(EN_B, HIGH);
                digitalWrite(M2_1, LOW);
                digitalWrite(M2_2, HIGH);
                // Back Left
                digitalWrite(EN_A1, HIGH);
                digitalWrite(M3_1, LOW);
                digitalWrite(M3_2, HIGH);
                // Back Right
                digitalWrite(EN_B1, HIGH);
                digitalWrite(M4_1, HIGH);
                digitalWrite(M4_2, LOW);
                break;
            }
        }
    }
    delay(100); // delay for 1/10 of a second
}
