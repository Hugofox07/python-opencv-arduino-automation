# OpenCV
import cv2 as cv

# Biblioteca matemática
import numpy as np

# Comunicação serial com Arduino
import serial

# Biblioteca tempo
import time


# -----------------------------------
# CONEXÃO COM ARDUINO
# -----------------------------------

# Porta serial do Arduino
# Troque COM3 pela sua porta
arduino = serial.Serial('COM4', 9600)

# Espera Arduino inicializar
time.sleep(2)


# -----------------------------------
# ABRE WEBCAM
# -----------------------------------

camera = cv.VideoCapture(0)


# -----------------------------------
# LOOP PRINCIPAL
# -----------------------------------

while True:

    # Captura frame da câmera
    ret, frame = camera.read()

    # Espelha imagem
    # Igual câmera selfie
    frame = cv.flip(frame, 1)

    # Pega tamanho da imagem
    altura, largura, _ = frame.shape


    # -----------------------------------
    # CONVERSÃO HSV
    # -----------------------------------

    # Converte BGR para HSV
    hsv = cv.cvtColor(
        frame,
        cv.COLOR_BGR2HSV
    )


    # -----------------------------------
    # FAIXAS DE COR VERMELHA
    # -----------------------------------

    # Vermelho escuro
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    # Vermelho claro
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])


    # -----------------------------------
    # CRIA MÁSCARAS
    # -----------------------------------

    # Detecta faixa 1
    mask1 = cv.inRange(
        hsv,
        lower_red1,
        upper_red1
    )

    # Detecta faixa 2
    mask2 = cv.inRange(
        hsv,
        lower_red2,
        upper_red2
    )

    # Junta máscaras
    mask = mask1 + mask2


    # -----------------------------------
    # REMOVE RUÍDOS
    # -----------------------------------

    # Blur suaviza imagem
    mask = cv.GaussianBlur(
        mask,
        (5, 5),
        0
    )


    # -----------------------------------
    # PROCURA CONTORNOS
    # -----------------------------------

    contours, _ = cv.findContours(
        mask,
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )


    # -----------------------------------
    # DESENHA DIVISÕES DA TELA
    # -----------------------------------

    # Linha esquerda
    cv.line(
        frame,
        (largura // 3, 0),
        (largura // 3, altura),
        (255, 255, 255),
        2
    )

    # Linha direita
    cv.line(
        frame,
        (2 * largura // 3, 0),
        (2 * largura // 3, altura),
        (255, 255, 255),
        2
    )


    # -----------------------------------
    # VERIFICA SE EXISTE OBJETO
    # -----------------------------------

    if len(contours) > 0:

        # Pega maior contorno
        largest_contour = max(
            contours,
            key=cv.contourArea
        )

        # Calcula área
        area = cv.contourArea(
            largest_contour
        )

        # Ignora ruídos pequenos
        if area > 500:

            # Calcula círculo do objeto
            ((x, y), radius) = cv.minEnclosingCircle(
                largest_contour
            )

            # Centro do objeto
            center_x = int(x)
            center_y = int(y)


            # -----------------------------------
            # DESENHA CÍRCULO
            # -----------------------------------

            cv.circle(
                frame,
                (center_x, center_y),
                int(radius),
                (0, 255, 0),
                2
            )


            # -----------------------------------
            # DECISÃO DE DIREÇÃO
            # -----------------------------------

            # ESQUERDA
            if center_x < largura // 3:

                direcao = "ESQUERDA"

                # Envia comando serial
                arduino.write(b'L')


            # CENTRO
            elif center_x < 2 * largura // 3:

                direcao = "CENTRO"

                # Envia comando serial
                arduino.write(b'C')


            # DIREITA
            else:

                direcao = "DIREITA"

                # Envia comando serial
                arduino.write(b'R')


            # -----------------------------------
            # ESCREVE TEXTO
            # -----------------------------------

            cv.putText(
                frame,
                direcao,
                (50, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )


    # -----------------------------------
    # MOSTRA IMAGEM
    # -----------------------------------

    cv.imshow(
        "Servo Tracking",
        frame
    )


    # -----------------------------------
    # FECHA PROGRAMA
    # -----------------------------------

    if cv.waitKey(1) == ord('q'):
        break


# Fecha câmera
camera.release()

# Fecha janelas
cv.destroyAllWindows()