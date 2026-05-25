# OpenCV
import cv2 as cv

# Numpy
import numpy as np

# Serial
import serial

# Tempo
import time


# -----------------------------------
# ARDUINO
# -----------------------------------

arduino = serial.Serial(
    'COM4',
    9600
)

# Espera inicialização
time.sleep(2)
# -----------------------------------
# CENTRALIZA SERVO
# -----------------------------------

arduino.write(b'90\n')

# Espera servo estabilizar
time.sleep(2)


# -----------------------------------
# WEBCAM
# -----------------------------------

camera = cv.VideoCapture(0)


# -----------------------------------
# LOOP PRINCIPAL
# -----------------------------------

while True:

    # Captura frame
    ret, frame = camera.read()

    # Espelha imagem
    frame = cv.flip(frame, 1)

    # Cópia imagem
    output = frame.copy()


    # -----------------------------------
    # ESCALA DE CINZA
    # -----------------------------------

    gray = cv.cvtColor(
        frame,
        cv.COLOR_BGR2GRAY
    )


    # -----------------------------------
    # BLUR
    # -----------------------------------

    blur = cv.GaussianBlur(
        gray,
        (5, 5),
        0
    )


    # -----------------------------------
    # THRESHOLD
    # -----------------------------------

    _, thresh = cv.threshold(
        blur,
        100,
        255,
        cv.THRESH_BINARY_INV
    )


    # -----------------------------------
    # CONTORNOS
    # -----------------------------------

    contours, _ = cv.findContours(
        thresh,
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )


    # Direção padrão
    direcao = "CENTRO"


    # -----------------------------------
    # ANALISA OBJETOS
    # -----------------------------------

    for contour in contours:

        # Área
        area = cv.contourArea(contour)

        # Ignora ruído
        if area > 3000:

            # Aproxima forma
            epsilon = 0.02 * cv.arcLength(
                contour,
                True
            )

            approx = cv.approxPolyDP(
                contour,
                epsilon,
                True
            )

            # Desenha contorno
            cv.drawContours(
                output,
                [approx],
                -1,
                (0, 255, 0),
                3
            )


            # -----------------------------------
            # PONTOS DA FORMA
            # -----------------------------------

            pontos = approx.reshape(-1, 2)

            xs = pontos[:, 0]

            min_x = np.min(xs)

            max_x = np.max(xs)

            esquerda = np.sum(
                xs < (min_x + 20)
            )

            direita = np.sum(
                xs > (max_x - 20)
            )


            # -----------------------------------
            # DECISÃO
            # -----------------------------------

            # DIREITA
            if esquerda < direita:

                direcao = "DIREITA"

                arduino.write(b'R')

            # ESQUERDA
            else:

                direcao = "ESQUERDA"

                arduino.write(b'L')


            # Sai após detectar
            break


    # -----------------------------------
    # SEM SETA
    # -----------------------------------

    if direcao == "CENTRO":

        arduino.write(b'C')


    # -----------------------------------
    # TEXTO
    # -----------------------------------

    cv.putText(
        output,
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
        "Threshold",
        thresh
    )

    cv.imshow(
        "Servo Seta",
        output
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