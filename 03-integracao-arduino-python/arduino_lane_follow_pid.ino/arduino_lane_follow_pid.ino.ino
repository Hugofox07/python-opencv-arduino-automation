// Biblioteca servo
#include <Servo.h>

// Servo direção
Servo direcao;

// Ângulo inicial
int angulo = 90;

void setup()
{
    // Serial
    Serial.begin(9600);

    // Servo pino 9
    direcao.attach(9);

    // -----------------------------------
    // CENTRALIZA SERVO
    // -----------------------------------

    direcao.write(90);

    // Espera servo estabilizar
    delay(2000);
}

void loop()
{
    // -----------------------------------
    // RECEBE SERIAL
    // -----------------------------------

    if (Serial.available())
    {
        // Lê ângulo
        angulo = Serial.parseInt();

        // Limites
        angulo = constrain(
            angulo,
            50,
            130
        );

        // Move servo
        direcao.write(angulo);
    }
}