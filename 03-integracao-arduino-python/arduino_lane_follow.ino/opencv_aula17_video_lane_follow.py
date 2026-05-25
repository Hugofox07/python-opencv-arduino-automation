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
# ABRE VÍDEO
# -----------------------------------

video = cv.VideoCapture(
     "souces\estrada3.mp4"
)


# -----------------------------------
# LOOP
# -----------------------------------

while True:

    # Lê frame vídeo
    ret, frame = video.read()

    # Se acabou vídeo
    if not ret:
        break


    # -----------------------------------
    # REDIMENSIONA
    # -----------------------------------

    frame = cv.resize(
        frame,
        (640, 480)
    )

    altura, largura, _ = frame.shape


    # -----------------------------------
    # REGIÃO INTERESSE
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


    # Servo padrão
    angulo = 90


    # -----------------------------------
    # DETECTOU FAIXA
    # -----------------------------------

    if len(contours) > 0:

        largest = max(
            contours,
            key=cv.contourArea
        )

        area = cv.contourArea(
            largest
        )

        if area > 1000:

            # Centro faixa
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
                # CONVERTE PARA ÂNGULO
                # -----------------------------------

                angulo = int(
                    (cx * 180) / largura
                )

                angulo = max(
                    40,
                    min(140, angulo)
                )


    # -----------------------------------
    # ENVIA SERVO
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
        "Video Lane Following",
        frame
    )


    # -----------------------------------
    # VELOCIDADE VÍDEO
    # -----------------------------------

    if cv.waitKey(30) == ord('q'):
        break


# Fecha vídeo
video.release()

# Fecha janelas
cv.destroyAllWindows()