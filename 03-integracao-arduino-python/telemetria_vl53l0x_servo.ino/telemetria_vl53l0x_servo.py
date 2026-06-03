# ==========================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# ==========================================

import cv2 as cv
import serial
import time
from collections import deque

# ==========================================
# CONEXÃO COM O ARDUINO
# ==========================================

arduino = serial.Serial("COM4", 115200)

# Aguarda Arduino iniciar
time.sleep(2)

# ==========================================
# ABRE A WEBCAM
# ==========================================

cap = cv.VideoCapture(0)

# ==========================================
# VARIÁVEIS DO SISTEMA
# ==========================================

# Guarda as últimas 5 leituras do sensor
leituras = deque(maxlen=5)

# Distância inicial
distancia = 0

# Ângulo inicial do servo
angulo = 90

# Estado do sistema
mensagem = "INICIANDO..."

# ==========================================
# LOOP PRINCIPAL
# ==========================================

while True:

    # Captura imagem da webcam
    ret, frame = cap.read()

    if not ret:
        break

    # ==========================================
    # LEITURA DA SERIAL
    # ==========================================

    if arduino.in_waiting:

        try:

            dado = arduino.readline().decode().strip()

            distancia_recebida = int(dado)

            # Adiciona leitura à lista
            leituras.append(distancia_recebida)

            # Calcula média das últimas leituras
            distancia = int(
                sum(leituras) / len(leituras)
            )

        except:
            pass

    # ==========================================
    # LÓGICA DE CONTROLE DO SERVO
    # ==========================================

    # Menor que 10 cm
    if distancia < 100:

        angulo = 0

        mensagem = "OBJETO PERTO -> ESQUERDA"

    # Maior que 20 cm
    elif distancia > 200:

        angulo = 180

        mensagem = "OBJETO LONGE -> DIREITA"

    # Entre 10 e 20 cm
    else:

        angulo = 90

        mensagem = "DISTANCIA IDEAL"

    # ==========================================
    # ENVIA COMANDO AO ARDUINO
    # ==========================================

    arduino.write(f"{angulo}\n".encode())

    # ==========================================
    # DESENHA BARRA DE DISTÂNCIA
    # ==========================================

    barra = min(int(distancia / 3), 300)

    # Moldura da barra
    cv.rectangle(
        frame,
        (20, 180),
        (320, 210),
        (255, 255, 255),
        2
    )

    # Preenchimento da barra
    cv.rectangle(
        frame,
        (20, 180),
        (20 + barra, 210),
        (0, 255, 0),
        -1
    )

    # ==========================================
    # EXIBE DISTÂNCIA
    # ==========================================

    cv.putText(
        frame,
        f"Distancia: {distancia} mm",
        (20, 40),
        cv.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # ==========================================
    # EXIBE ÂNGULO DO SERVO
    # ==========================================

    cv.putText(
        frame,
        f"Servo: {angulo} graus",
        (20, 80),
        cv.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # ==========================================
    # EXIBE ESTADO DO SISTEMA
    # ==========================================

    cv.putText(
        frame,
        mensagem,
        (20, 120),
        cv.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    # ==========================================
    # EXIBE INSTRUÇÃO DE SAÍDA
    # ==========================================

    cv.putText(
        frame,
        "ESC = SAIR",
        (20, 260),
        cv.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # ==========================================
    # MOSTRA A JANELA
    # ==========================================

    cv.imshow(
        "Sistema de Telemetria - Hugo",
        frame
    )

    # ==========================================
    # FECHA COM ESC
    # ==========================================

    tecla = cv.waitKey(1)

    if tecla == 27:
        break

# ==========================================
# FINALIZAÇÃO
# ==========================================

cap.release()

arduino.close()

cv.destroyAllWindows()