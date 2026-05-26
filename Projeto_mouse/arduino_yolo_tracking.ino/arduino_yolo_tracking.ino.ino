#include <Servo.h>

Servo servo;

int angulo = 90;

void setup()
{
    Serial.begin(9600);

    servo.attach(9);

    servo.write(90);

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

        servo.write(angulo);
    }
}