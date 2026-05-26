#include <Servo.h>

Servo servoMotor;

int angulo = 90;

void setup()
{
    Serial.begin(115200);

    servoMotor.attach(9);

    servoMotor.write(90);

    delay(500);
}

void loop()
{
    if (Serial.available())
    {
        angulo = Serial.parseInt();

        angulo = constrain(angulo, 0, 180);

        servoMotor.write(angulo);
    }
}
