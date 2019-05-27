
void loadGcodeCommands(int commands[][4]) {
  // Clear current commands
  for (int i = 0; i < numCommands; i++) {
    for (int j = 0; j < 3; j++) {
      commands[i][j] = 0;
    }
  }

  // Load new commands
  int commandId = 0;
  if (Serial.available()) {
    Serial.println("Reading command");
    while (1) {
      char command = Serial.read();
      Serial.print(command);
      if (command == '\n') {
        break;
      } else if (command == ' ') {
        commandId++;
      } else if ((command == 'x') || (command == 'y') || (command == 'z') || (command == 'r') || (command == 's') || (command == 'd')) {
        commands[commandId][0] = command;
        while (!Serial.available()) {}
        commands[commandId][1] = Serial.read() - '0';
        while (!Serial.available()) {}
        commands[commandId][2] = Serial.read() - '0';
        while (!Serial.available()) {}
        commands[commandId][3] = Serial.read() - '0';
        Serial.println("Loaded number");
      } else {
        Serial.println("What is this");
        break;
      }
    }
  }
}

void printCommands(int commands[][4]) {
  for (int i = 0; i < numCommands; i++) {
    if (commands[i][0] > 0) {
      Serial.print(char(commands[i][0]));
      Serial.print(commands[i][1]);
      Serial.print(commands[i][2]);
      Serial.print(commands[i][3]);
      Serial.print(' ');
    }
  }
  Serial.print('\n');
}
