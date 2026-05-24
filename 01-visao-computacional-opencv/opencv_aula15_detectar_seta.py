# OpenCV
import cv2 as cv

# Numpy
import numpy as np


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

    # Copia imagem
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


    # -----------------------------------
    # ANALISA CONTORNOS
    # -----------------------------------

    for contour in contours:

        # Área do objeto
        area = cv.contourArea(contour)

        # Ignora ruído
        if area > 3000:

            # Aproxima formato
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
            # PEGA PONTOS
            # -----------------------------------

            pontos = approx.reshape(-1, 2)

            # Lista posições X
            xs = pontos[:, 0]

            # Menor X
            min_x = np.min(xs)

            # Maior X
            max_x = np.max(xs)

            # Conta pontos próximos esquerda
            esquerda = np.sum(xs < (min_x + 20))

            # Conta pontos próximos direita
            direita = np.sum(xs > (max_x - 20))


            # -----------------------------------
            # DECIDE DIREÇÃO
            # -----------------------------------

            if esquerda < direita:

                direcao = "DIREITA"

            else:

                direcao = "ESQUERDA"


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
        "Deteccao Seta",
        output
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