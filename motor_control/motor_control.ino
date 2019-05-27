#include <AccelStepper.h>
#include <Servo.h>

const int numCommands = 10;
int commands[numCommands][4];

long stepperPositionOffset[4] = {};
long stepperPositions[4] = {};
// XYZ - stepper motors
AccelStepper stepperX(AccelStepper::FULL4WIRE, 22, 24, 26, 28);
AccelStepper stepperY(AccelStepper::FULL4WIRE, 30, 32, 34, 36);
AccelStepper stepperZ(AccelStepper::FULL4WIRE, 38, 40, 42, 44);
AccelStepper stepperR(AccelStepper::FULL4WIRE, 46, 48, 50, 52);
AccelStepper* steppers[4] = {&stepperX, &stepperY, &stepperZ, &stepperR};
int stepperPins[4][4] = {{22, 24, 26, 28}, {30, 32, 34, 36}, {38, 40, 42, 44}, {46, 48, 50, 52}};

// Rotation and swing - servo motors
Servo servoSwing;
int servoCurrentLocation = 0;
int servoNewLocation = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Begin");

  // Set up XYZ steppers
  stepperX.setMaxSpeed(120);
  stepperX.setAcceleration(100);
  stepperY.setMaxSpeed(120);
  stepperY.setAcceleration(100);
  stepperZ.setMaxSpeed(120);
  stepperZ.setAcceleration(100);
  stepperR.setMaxSpeed(20);
  stepperR.setAcceleration(20);

  // Set up swing servo
  servoSwing.attach(31);
  zeroMotors();
}

void zeroMotors() {
  servoSwing.write(0);
  delay(1000);
}

void printCurrentPosition() {
    Serial.print(-stepperX.currentPosition());
    Serial.print(' ');
    Serial.print(stepperY.currentPosition()/10);
    Serial.print(' ');
    Serial.print(stepperZ.currentPosition());
    Serial.print(' ');
    Serial.print(stepperR.currentPosition());
    Serial.print(' ');
    Serial.print(servoCurrentLocation);
    Serial.print('\n');
}

void loop() {
  unsigned long servoMoveStartTime = millis();

  // Load new commands
  loadGcodeCommands(commands);
  
  if (commands[0][0] != 0) {
    printCommands(commands);
  }
  
  for (int i = 0; i < numCommands; i++) {
    if (commands[i][0] != 0) {
      char command = char(commands[i][0]);
      int num = commands[i][1]*100+commands[i][2]*10+commands[i][3];
      if (command == 's') {
        if (0 <= num && num < 180) {
          Serial.println("Moving servo");
          Serial.println(num);
          servoSwing.write(num);
          servoNewLocation = num;
        } else {
          Serial.println("Invalid number to servo position, which should range from 0 to 179");
          Serial.println(num);
        }
      } else if (command == 'x') {
        Serial.println("Moving stepper X");
        Serial.println(num);
        stepperX.moveTo(-num);
      } else if (command == 'y') {
        Serial.println("Moving stepper Y");
        Serial.println(num);
        stepperY.moveTo(num*10);
      } else if (command == 'z') {
        Serial.println("Moving stepper Z");
        Serial.println(num);
        stepperZ.moveTo(num);
      } else if (command == 'r') {
        Serial.println("Moving stepper R");
        Serial.println(num);
        stepperR.moveTo(num);
      } else if (command == 'p') {
        delay(5000);
        Serial.println("Resume");
      } else if (command == 'g') {
        // pass. Will return current position later
      } else if (command == 'd') {
        Serial.println("Moving stepper Y");
        Serial.println(-num);
        stepperY.moveTo(-num*10);
      } else {
        Serial.println("Unknown command");
        Serial.println(command);
      }
    }
  }

  unsigned long printStart = millis();
  // Wait for stepper motors to reach destination
  while((abs(stepperX.distanceToGo()) > 0) || (abs(stepperY.distanceToGo()) > 0) || (abs(stepperZ.distanceToGo()) > 0) || (abs(stepperR.distanceToGo()) > 0)) {
    for (int i = 0; i < 4; i++) {
      if (abs(steppers[i]->distanceToGo()) > 0) {
        steppers[i]->run();
 
        // Turn off motor driver to prevent over-heating
        if (steppers[i]->distanceToGo() == 0) {
          delay(20);
          for (int j = 0; j < 4; j++) {
            digitalWrite(stepperPins[i][j], 0);
          }
        }
      }
    }

    if (millis()-printStart > 500) {
      // Serial.println("Waiting for steppers");
      printStart = millis();
    }
  }

  // Wait for servo motor to reach destination. Servo swings through 180 degrees in 1 seconds
  while (millis()-servoMoveStartTime < (abs((servoNewLocation-servoCurrentLocation)*1000.0/180))) {
    // Serial.println("Waiting for servo");
    delay(10);
  }
  servoCurrentLocation = servoNewLocation;

  if (commands[0][0] != 0) {
    Serial.println("Command finished");
    printCurrentPosition();
  }

  delay(10);
}
