#include <Servo.h>

Servo meuServo;

int angulo = 90;

void setup()
{
    Serial.begin(115200);

    meuServo.attach(9);

    meuServo.write(90);

    delay(500);
}

void loop()
{
    if (Serial.available())
    {
        angulo = Serial.parseInt();

        angulo = constrain(angulo, 0, 180);

        meuServo.write(angulo);
    }
}