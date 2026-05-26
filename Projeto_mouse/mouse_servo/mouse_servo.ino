#include <Servo.h>

Servo meuServo;

int angulo = 90;

void setup()
{
    Serial.begin(9600);

    meuServo.attach(9);

    meuServo.write(90);
}

void loop()
{
    if (Serial.available() > 0)
    {
        angulo = Serial.parseInt();

        angulo = constrain(angulo, 0, 180);

        meuServo.write(angulo);
    }
}