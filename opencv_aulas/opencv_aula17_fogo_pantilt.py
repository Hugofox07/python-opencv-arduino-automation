import cv2 as cv
import numpy as np
import serial
import time

# -----------------------------------
# CONEXÃO ARDUINO
# -----------------------------------
arduino = serial.Serial('COM4', 9600)
time.sleep(2)
# -----------------------------------
# CENTRALIZA SERVO
# -----------------------------------

arduino.write(b'90\n')

# Espera servo estabilizar
time.sleep(2)
# -----------------------------------
# ABRE CÂMERA
# -----------------------------------
camera = cv.VideoCapture(0)

# -----------------------------------
# LOOP PRINCIPAL
# -----------------------------------
while True:
    ret, frame = camera.read()
    frame = cv.flip(frame, 1)  # espelha

    altura, largura, _ = frame.shape

    # -----------------------------------
    # CONVERTE PARA HSV
    # -----------------------------------
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # -----------------------------------
    # FAIXAS DE COR PARA FOGO
    # Laranja/amarelo/vermelho típico do fogo
    # -----------------------------------
    lower_fire = np.array([0, 150, 150])
    upper_fire = np.array([35, 255, 255])

    mask = cv.inRange(hsv, lower_fire, upper_fire)

    # Suaviza e remove ruído
    mask = cv.GaussianBlur(mask, (7, 7), 0)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)

    # -----------------------------------
    # CONTORNOS
    # -----------------------------------
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    bomba = 0  # bomba desligada por padrão
    anguloPan = 90
    anguloTilt = 90

    if len(contours) > 0:
        largest = max(contours, key=cv.contourArea)
        area = cv.contourArea(largest)

        if area > 1000:  # ignora ruído pequeno
            ((x, y), radius) = cv.minEnclosingCircle(largest)
            center_x, center_y = int(x), int(y)

            # -----------------------------------
            # DESENHA OBJETO
            # -----------------------------------
            cv.circle(frame, (center_x, center_y), int(radius), (0, 255, 0), 3)
            cv.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            # -----------------------------------
            # CALCULA ÂNGULOS
            # -----------------------------------
            # 0-180 proporcional à largura/altura
            anguloPan = int((center_x * 180) / largura)
            anguloTilt = int((center_y * 180) / altura)

            bomba = 1  # aciona bomba se chama detectada

    # -----------------------------------
    # ENVIA PARA ARDUINO
    # -----------------------------------
    comando = f"{anguloPan},{anguloTilt},{bomba}\n"
    arduino.write(comando.encode())

    # -----------------------------------
    # MOSTRA RESULTADO
    # -----------------------------------
    cv.imshow("Mascara Fogo", mask)
    cv.imshow("Fogo Pantilt", frame)

    if cv.waitKey(1) == ord('q'):
        break

# Fecha câmera
camera.release()
cv.destroyAllWindows()