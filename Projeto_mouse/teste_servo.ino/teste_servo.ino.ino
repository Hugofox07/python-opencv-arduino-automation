#include <Servo.h>

Servo meuServo; 
int pinoServo = 9; // Pino digital onde o fio de sinal está conectado

void setup() {
  meuServo.attach(pinoServo);   // Inicializa o servo no pino definido
  meuServo.write(90);           // Posiciona o motor no centro (90 graus)
  delay(1000);                  // Aguarda 1 segundo para dar tempo do motor chegar ao centro
  meuServo.detach();            // Desliga o sinal do servo. Agora você pode girá-lo manualmente!
}

void loop() {
  // O código principal fica vazio, pois o motor já foi centralizado e liberado.
}