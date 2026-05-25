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

time.sleep(2)


# -----------------------------------
# WEBCAM
# -----------------------------------

camera = cv.VideoCapture(0)


# -----------------------------------
# LOOP
# -----------------------------------

while True:

    # Captura frame
    ret, frame = camera.read()

    # Espelha
    frame = cv.flip(frame, 1)

    # Tamanho
    altura, largura, _ = frame.shape


    # -----------------------------------
    # REGIÃO INTERESSE
    # Parte inferior da imagem
    # -----------------------------------

    roi = frame[
        altura // 2:altura,
        0:largura
    ]


    # -----------------------------------
    # HSV
    # -----------------------------------

    hsv = cv.cvtColor(
        roi,
        cv.COLOR_BGR2HSV
    )


    # -----------------------------------
    # DETECÇÃO BRANCO
    # -----------------------------------

    lower_white = np.array([
        0,
        0,
        180
    ])

    upper_white = np.array([
        180,
        50,
        255
    ])


    # Máscara
    mask = cv.inRange(
        hsv,
        lower_white,
        upper_white
    )


    # -----------------------------------
    # REMOVE RUÍDOS
    # -----------------------------------

    mask = cv.GaussianBlur(
        mask,
        (5, 5),
        0
    )

    mask = cv.erode(
        mask,
        None,
        iterations=2
    )

    mask = cv.dilate(
        mask,
        None,
        iterations=2
    )


    # -----------------------------------
    # CONTORNOS
    # -----------------------------------

    contours, _ = cv.findContours(
        mask,
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )


    # Servo central
    angulo = 90


    # -----------------------------------
    # SE ENCONTROU FAIXA
    # -----------------------------------

    if len(contours) > 0:

        # Maior faixa
        largest = max(
            contours,
            key=cv.contourArea
        )

        area = cv.contourArea(
            largest
        )

        # Ignora ruído
        if area > 1000:

            # Centro da faixa
            M = cv.moments(largest)

            if M["m00"] != 0:

                cx = int(
                    M["m10"] / M["m00"]
                )

                cy = int(
                    M["m01"] / M["m00"]
                )


                # -----------------------------------
                # DESENHA
                # -----------------------------------

                cv.circle(
                    roi,
                    (cx, cy),
                    8,
                    (0, 0, 255),
                    -1
                )


                # -----------------------------------
                # CONVERTE POSIÇÃO
                # EM ÂNGULO
                # -----------------------------------

                angulo = int(
                    (cx * 180) / largura
                )

                # Limita
                angulo = max(
                    40,
                    min(140, angulo)
                )


    # -----------------------------------
    # ENVIA ARDUINO
    # -----------------------------------

    comando = f"{angulo}\n"

    arduino.write(
        comando.encode()
    )


    # -----------------------------------
    # TEXTO
    # -----------------------------------

    cv.putText(
        frame,
        f'Angulo: {angulo}',
        (20, 40),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )


    # -----------------------------------
    # MOSTRA
    # -----------------------------------

    cv.imshow(
        "Mascara",
        mask
    )

    cv.imshow(
        "Lane Following",
        frame
    )


    # -----------------------------------
    # FECHA
    # -----------------------------------

    if cv.waitKey(1) == ord('q'):
        break


# Fecha câmera
camera.release()

# Fecha janelas
cv.destroyAllWindows()