#include <Servo.h>

Servo servoPan;    // Servo horizontal
Servo servoTilt;   // Servo vertical

int motorBomba = 6; // Pino motor bomba (PWM ou digital)

int anguloPan = 90;
int anguloTilt = 90;

void setup() {
    Serial.begin(9600);

    servoPan.attach(9);
    servoTilt.attach(10);

    pinMode(motorBomba, OUTPUT);
    digitalWrite(motorBomba, LOW); // bomba desligada

    // Inicializa servos no centro
    servoPan.write(90);
    servoTilt.write(90);
}

void loop() {
    if (Serial.available()) {
        // Comando recebido exemplo: "120,60,1\n"
        String comando = Serial.readStringUntil('\n');

        int index1 = comando.indexOf(',');
        int index2 = comando.lastIndexOf(',');

        if (index1 > 0 && index2 > index1) {
            anguloPan = comando.substring(0, index1).toInt();
            anguloTilt = comando.substring(index1 + 1, index2).toInt();
            int bomba = comando.substring(index2 + 1).toInt();

            anguloPan = constrain(anguloPan, 0, 180);
            anguloTilt = constrain(anguloTilt, 0, 180);

            servoPan.write(anguloPan);
            servoTilt.write(anguloTilt);

            if (bomba == 1) {
                digitalWrite(motorBomba, HIGH);
            } else {
                digitalWrite(motorBomba, LOW);
            }
        }
    }
}