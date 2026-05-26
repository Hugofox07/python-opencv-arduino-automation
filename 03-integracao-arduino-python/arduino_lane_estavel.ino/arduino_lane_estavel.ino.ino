#include <Servo.h>

Servo direcao;

int angulo = 90;

void setup()
{
    Serial.begin(9600);

    direcao.attach(9);

    direcao.write(90);

    delay(2000);
}

void loop()
{
    if (Serial.available())
    {
        angulo = Serial.parseInt();

        angulo = constrain(
            angulo,
            60,
            120
        );

        direcao.write(angulo);
    }
}