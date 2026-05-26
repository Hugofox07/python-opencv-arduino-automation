import cv2
import numpy as np
import serial
import time

# =========================================
# SERIAL
# =========================================

arduino = serial.Serial('COM4', 115200)

time.sleep(2)

# =========================================
# CAMERA
# =========================================

largura = 640
altura = 480

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, largura)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, altura)

# =========================================
# VARIAVEIS
# =========================================

angulo = 90
ultimo_angulo = 90

# =========================================
# LOOP
# =========================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Espelha imagem
    frame = cv2.flip(frame, 1)

    # =====================================
    # CONVERTE BGR → HSV
    # =====================================

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # =====================================
    # COR VERMELHA
    # =====================================

    vermelho_baixo1 = np.array([0, 120, 70])
    vermelho_alto1 = np.array([10, 255, 255])

    vermelho_baixo2 = np.array([170, 120, 70])
    vermelho_alto2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, vermelho_baixo1, vermelho_alto1)
    mask2 = cv2.inRange(hsv, vermelho_baixo2, vermelho_alto2)

    mascara = mask1 + mask2

    # =====================================
    # REMOVE RUIDOS
    # =====================================

    mascara = cv2.erode(mascara, None, iterations=2)
    mascara = cv2.dilate(mascara, None, iterations=2)

    # =====================================
    # CONTORNOS
    # =====================================

    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # =====================================
    # SE ENCONTROU OBJETO
    # =====================================

    if len(contornos) > 0:

        maior = max(contornos, key=cv2.contourArea)

        area = cv2.contourArea(maior)

        # Ignora objetos pequenos
        if area > 1000:

            x, y, w, h = cv2.boundingRect(maior)

            # Centro do objeto
            cx = x + w // 2
            cy = y + h // 2

            # Desenha
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

            cv2.circle(frame, (cx, cy), 5, (255,0,0), -1)

            # =================================
            # CONVERTE POSICAO → ANGULO
            # =================================

            angulo = int((cx / largura) * 180)

            angulo = max(0, min(180, angulo))

            # =================================
            # ENVIA PARA ARDUINO
            # =================================

            if abs(angulo - ultimo_angulo) >= 2:

                arduino.write(f"{angulo}\n".encode())

                ultimo_angulo = angulo

            # =================================
            # TEXTO
            # =================================

            cv2.putText(
                frame,
                f"Angulo: {angulo}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

    # Linha central
    cv2.line(
        frame,
        (largura//2, 0),
        (largura//2, altura),
        (255,255,255),
        2
    )

    cv2.imshow("Tracking Vermelho", frame)

    tecla = cv2.waitKey(1)

    if tecla == 27:
        break

cap.release()

cv2.destroyAllWindows()