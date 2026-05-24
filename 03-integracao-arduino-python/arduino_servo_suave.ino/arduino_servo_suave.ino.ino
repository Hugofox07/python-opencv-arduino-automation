// Biblioteca servo
#include <Servo.h>

// Cria servo
Servo servoMotor;

// Variável ângulo
int angulo = 90;

void setup()
{
    // Serial
    Serial.begin(9600);

    // Servo no pino 9
    servoMotor.attach(9);

    // Centraliza servo
    servoMotor.write(90);
}

void loop()
{
    // Se chegou dado serial
    if (Serial.available())
    {
        // Lê ângulo enviado
        angulo = Serial.parseInt();

        // Limita ângulo
        angulo = constrain(
            angulo,
            0,
            180
        );

        // Move servo
        servoMotor.write(angulo);
    }
}