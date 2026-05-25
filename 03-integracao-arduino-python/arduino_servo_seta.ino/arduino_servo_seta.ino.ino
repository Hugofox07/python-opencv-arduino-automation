// Biblioteca servo
#include <Servo.h>

// Cria servo
Servo servoMotor;

// Variável comando
char comando;

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
    // Verifica serial
    if (Serial.available())
    {
        // Lê caractere
        comando = Serial.read();

        // -------------------
        // ESQUERDA
        // -------------------

        if (comando == 'L')
        {
            servoMotor.write(30);
        }

        // -------------------
        // DIREITA
        // -------------------

        if (comando == 'R')
        {
            servoMotor.write(150);
        }

        // -------------------
        // CENTRO
        // -------------------

        if (comando == 'C')
        {
            servoMotor.write(90);
        }
    }
}