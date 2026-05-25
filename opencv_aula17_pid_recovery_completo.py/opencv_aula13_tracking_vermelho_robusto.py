# OpenCV
import cv2 as cv

# Numpy
import numpy as np

# Serial Arduino
import serial

# Tempo
import time


# -----------------------------------
# CONEXÃO ARDUINO
# -----------------------------------

arduino = serial.Serial('COM4', 9600)

time.sleep(2)


# -----------------------------------
# ABRE WEBCAM
# -----------------------------------

camera = cv.VideoCapture(0)


# -----------------------------------
# LOOP PRINCIPAL
# -----------------------------------

while True:

    # Captura imagem
    ret, frame = camera.read()

    # Espelha imagem
    frame = cv.flip(frame, 1)

    # Pega tamanho tela
    altura, largura, _ = frame.shape


    # -----------------------------------
    # DESFOQUE
    # -----------------------------------

    # Remove ruído da câmera
    frame_blur = cv.GaussianBlur(
        frame,
        (11, 11),
        0
    )


    # -----------------------------------
    # HSV
    # -----------------------------------

    hsv = cv.cvtColor(
        frame_blur,
        cv.COLOR_BGR2HSV
    )


    # -----------------------------------------------------------
    # VERMELHO MAIS RESTRITO PODE TROCAR POR OUTRAS CORES TAMBEM
    # -----------------------------------------------------------

    # Vermelho escuro
    lower_red1 = np.array([0, 150, 100])
    upper_red1 = np.array([10, 255, 255])

    # Vermelho claro
    lower_red2 = np.array([170, 150, 100])
    upper_red2 = np.array([180, 255, 255])


    # -----------------------------------
    # MÁSCARAS
    # -----------------------------------

    mask1 = cv.inRange(
        hsv,
        lower_red1,
        upper_red1
    )

    mask2 = cv.inRange(
        hsv,
        lower_red2,
        upper_red2
    )

    mask = mask1 + mask2


    # -----------------------------------
    # REMOVE RUÍDOS
    # -----------------------------------

    # Remove pequenos pontos
    mask = cv.erode(
        mask,
        None,
        iterations=2
    )

    # Recupera objeto
    mask = cv.dilate(
        mask,
        None,
        iterations=2
    )

    # Suaviza
    mask = cv.GaussianBlur(
        mask,
        (9, 9),
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
    # DIVISÃO TELA
    # -----------------------------------

    cv.line(
        frame,
        (largura // 3, 0),
        (largura // 3, altura),
        (255, 255, 255),
        2
    )

    cv.line(
        frame,
        (2 * largura // 3, 0),
        (2 * largura // 3, altura),
        (255, 255, 255),
        2
    )


    # -----------------------------------
    # SE ENCONTROU OBJETO
    # -----------------------------------

    if len(contours) > 0:

        # Maior contorno
        largest_contour = max(
            contours,
            key=cv.contourArea
        )

        # Área do objeto
        area = cv.contourArea(
            largest_contour
        )

        # FILTRO IMPORTANTE
        # Ignora objetos pequenos
        if area > 2000:

            # Círculo mínimo
            ((x, y), radius) = cv.minEnclosingCircle(
                largest_contour
            )

            center_x = int(x)
            center_y = int(y)

            radius = int(radius)


            # -----------------------------------
            # DESENHA OBJETO
            # -----------------------------------

            cv.circle(
                frame,
                (center_x, center_y),
                radius,
                (0, 255, 0),
                3
            )

            cv.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 0, 255),
                -1
            )


            # -----------------------------------
            # DECISÃO DIREÇÃO
            # -----------------------------------

            # ESQUERDA
            if center_x < largura // 3:

                direcao = "ESQUERDA"

                arduino.write(b'L')

            # CENTRO
            elif center_x < 2 * largura // 3:

                direcao = "CENTRO"

                arduino.write(b'C')

            # DIREITA
            else:

                direcao = "DIREITA"

                arduino.write(b'R')


            # -----------------------------------
            # TEXTO
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
    # JANELAS
    # -----------------------------------

    cv.imshow(
        "Mascara",
        mask
    )

    cv.imshow(
        "Tracking Vermelho",
        frame
    )


    # -----------------------------------
    # FECHAR
    # -----------------------------------

    if cv.waitKey(1) == ord('q'):
        break


# Fecha câmera
camera.release()

# Fecha janelas
cv.destroyAllWindows()