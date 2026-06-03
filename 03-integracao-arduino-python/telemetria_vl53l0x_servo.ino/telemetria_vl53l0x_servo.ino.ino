// Biblioteca do Servo
#include <Servo.h>

// Biblioteca do sensor laser
#include "Adafruit_VL53L0X.h"

// Cria objeto servo
Servo servo1;

// Cria objeto sensor laser
Adafruit_VL53L0X lox = Adafruit_VL53L0X();

void setup()
{
  // Inicializa comunicação serial
  Serial.begin(115200);

  // Servo conectado no pino 9
  servo1.attach(9);

  // Servo inicia centralizado
  servo1.write(90);

  // Inicializa sensor VL53L0X
  if (!lox.begin())
  {
    Serial.println("ERRO_SENSOR");

    while(1);
  }
}

void loop()
{
  // Estrutura usada pelo sensor
  VL53L0X_RangingMeasurementData_t measure;

  // Faz leitura da distância
  lox.rangingTest(&measure, false);

  // Se leitura válida
  if(measure.RangeStatus != 4)
  {
    // Envia distância para Python
    Serial.println(
      measure.RangeMilliMeter
    );
  }

  // Recebe ângulo vindo do Python
  if(Serial.available())
  {
    int angulo = Serial.parseInt();

    // Garante ângulo válido
    if(angulo >= 0 && angulo <= 180)
    {
      servo1.write(angulo);
    }
  }

  delay(100);
}