#include <Servo.h>
#include "Adafruit_VL53L0X.h"

Servo servo1;
Adafruit_VL53L0X lox = Adafruit_VL53L0X();

int angulo = 90;

void setup()
{
  Serial.begin(115200);

  servo1.attach(9);
  servo1.write(angulo);

  while(!Serial)
  {
    delay(1);
  }

  if (!lox.begin())
  {
    Serial.println("Erro VL53L0X");
    while(1);
  }
}

void loop()
{
  // Recebe ângulo do Python
  if (Serial.available())
  {
    angulo = Serial.parseInt();

    if (angulo >= 0 && angulo <= 180)
    {
      servo1.write(angulo);
    }
  }

  // Mede distância
  VL53L0X_RangingMeasurementData_t measure;

  lox.rangingTest(&measure, false);

  if (measure.RangeStatus != 4)
  {
    Serial.print("DIST:");
    Serial.println(measure.RangeMilliMeter);
  }

  delay(50);
}