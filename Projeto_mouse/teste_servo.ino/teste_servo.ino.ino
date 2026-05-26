#include <Servo.h>

Servo servo;

void setup()
{
    servo.attach(9);
}

void loop()
{
    servo.write(60);
    delay(1000);

    servo.write(120);
    delay(1000);
}