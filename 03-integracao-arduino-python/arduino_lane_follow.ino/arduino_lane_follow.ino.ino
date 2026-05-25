// Biblioteca servo
#include <Servo.h>

// Servo direção
Servo direcao;

// Ângulo
int angulo = 90;

void setup()
{
    // Comunicação serial
    Serial.begin(9600);

    // Servo pino 9
    direcao.attach(9);

    // Centro
    direcao.write(90);
}

void loop()
{
    // Se chegou serial
    if (Serial.available())
    {
        // Lê ângulo
        angulo = Serial.parseInt();

        // Limita ângulo
        angulo = constrain(
            angulo,
            40,
            140
        );

        // Move servo
        direcao.write(angulo);
    }
}