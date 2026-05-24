// Biblioteca para controlar servo motor
#include <Servo.h>

// Cria objeto servo
Servo servoMotor;

// Variável que vai guardar
// o comando recebido do Python
char comando;

void setup()
{
    // Inicia comunicação serial
    // 9600 = velocidade comunicação
    Serial.begin(9600);

    // Servo conectado no pino 9
    servoMotor.attach(9);

    // Coloca servo no centro
    // 90 graus = posição central
    servoMotor.write(90);
}

void loop()
{
    // Verifica se chegou dado serial
    if (Serial.available())
    {
        // Lê caractere enviado pelo Python
        comando = Serial.read();

        // -------------------------
        // ESQUERDA
        // -------------------------

        // Se recebeu letra L
        if (comando == 'L')
        {
            // Move servo para esquerda
            servoMotor.write(30);
        }

        // -------------------------
        // CENTRO
        // -------------------------

        // Se recebeu letra C
        if (comando == 'C')
        {
            // Centraliza servo
            servoMotor.write(90);
        }

        // -------------------------
        // DIREITA
        // -------------------------

        // Se recebeu letra R
        if (comando == 'R')
        {
            // Move servo direita
            servoMotor.write(150);
        }
    }
}