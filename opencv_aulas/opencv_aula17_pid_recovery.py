# OpenCV
import cv2 as cv

# Numpy
import numpy as np

# Serial Arduino
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

# Espera Arduino iniciar
time.sleep(2)


# -----------------------------------
# CENTRALIZA SERVO
# -----------------------------------

arduino.write(b'90\n')

# Espera servo estabilizar
time.sleep(2)


# -----------------------------------
# ABRE VIDEO
# -----------------------------------

video = cv.VideoCapture(
    "souces/estrada2.mp4"
)


# -----------------------------------
# PID
# -----------------------------------

Kp = 0.15
Ki = 0.0005
Kd = 0.08


# -----------------------------------
# VARIÁVEIS PID
# -----------------------------------

erro_anterior = 0
erro_integral = 0


# -----------------------------------
# ÂNGULO ATUAL
# -----------------------------------

angulo = 90


# -----------------------------------
# LOOP PRINCIPAL
# -----------------------------------

while True:

    # Lê frame
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
        60,
        255
    ])


    # Máscara
    mask = cv.inRange(
        hsv,
        lower_white,
        upper_white
    )


    # -----------------------------------
    # FILTROS
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


    # -----------------------------------
    # SEM FAIXA
    # VOLTA CENTRO
    # -----------------------------------

    if len(contours) == 0:

        # Recuperação suave
        if angulo < 90:
            angulo += 2

        elif angulo > 90:
            angulo -= 2


    # -----------------------------------
    # DETECTOU FAIXA
    # -----------------------------------

    else:

        # Maior contorno
        largest = max(
            contours,
            key=cv.contourArea
        )

        # Área
        area = cv.contourArea(
            largest
        )


        # Ignora ruído
        if area > 1000:

            # -----------------------------------
            # MOMENTOS
            # -----------------------------------

            M = cv.moments(
                largest
            )

            if M["m00"] != 0:

                # Centro faixa
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

                # Linha centro
                cv.line(
                    roi,
                    (largura // 2, 0),
                    (largura // 2, roi.shape[0]),
                    (255, 0, 0),
                    2
                )


                # -----------------------------------
                # ERRO
                # -----------------------------------

                erro = cx - (
                    largura // 2
                )


                # -----------------------------------
                # PID
                # -----------------------------------

                proporcional = erro

                erro_integral += erro

                derivativo = (
                    erro - erro_anterior
                )

                pid = (
                    (Kp * proporcional)
                    +
                    (Ki * erro_integral)
                    +
                    (Kd * derivativo)
                )

                erro_anterior = erro


                # -----------------------------------
                # CONVERTE PID
                # PARA ÂNGULO
                # -----------------------------------

                angulo = int(
                    90 + pid
                )


                # -----------------------------------
                # LIMITES
                # -----------------------------------

                angulo = max(
                    50,
                    min(130, angulo)
                )


    # -----------------------------------
    # ENVIA SERIAL
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

    cv.putText(
        frame,
        'PID RECOVERY',
        (20, 80),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )


    # -----------------------------------
    # JANELAS
    # -----------------------------------

    cv.imshow(
        "Mascara",
        mask
    )

    cv.imshow(
        "Lane Following PID",
        frame
    )


    # -----------------------------------
    # CONTROLE VELOCIDADE
    # -----------------------------------

    if cv.waitKey(30) == ord('q'):
        break


# Fecha vídeo
video.release()

# Fecha janelas
cv.destroyAllWindows()