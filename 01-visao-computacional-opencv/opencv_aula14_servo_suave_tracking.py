# OpenCV
import cv2 as cv

# Numpy
import numpy as np

# Serial
import serial

# Tempo
import time


# -----------------------------------
# CONEXÃO ARDUINO
# -----------------------------------

arduino = serial.Serial(
    'COM4',
    9600
)

# Espera Arduino iniciar
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

    # Tamanho tela
    altura, largura, _ = frame.shape


    # -----------------------------------
    # BLUR
    # -----------------------------------

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


    # -----------------------------------
    # COR VERMELHA
    # -----------------------------------

    lower_red1 = np.array([0, 150, 100])
    upper_red1 = np.array([10, 255, 255])

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

    mask = cv.GaussianBlur(
        mask,
        (9, 9),
        0
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
    # OBJETO ENCONTRADO
    # -----------------------------------

    if len(contours) > 0:

        # Maior contorno
        largest_contour = max(
            contours,
            key=cv.contourArea
        )

        # Área
        area = cv.contourArea(
            largest_contour
        )

        # Ignora ruído
        if area > 2000:

            # Círculo
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
            # CONVERTE POSIÇÃO EM ÂNGULO
            # -----------------------------------

            angulo = int(
                (center_x * 180) / largura
            )


            # -----------------------------------
            # ENVIA PARA ARDUINO
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
                (255, 255, 255),
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
        "Servo Tracking Suave",
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