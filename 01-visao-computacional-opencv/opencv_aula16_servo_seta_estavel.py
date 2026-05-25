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
# CONTROLE ESTABILIDADE
# -----------------------------------

ultima_direcao = "CENTRO"

# Tempo último comando
ultimo_envio = time.time()

# Delay mínimo entre comandos
delay_comando = 0.3


# -----------------------------------
# LOOP PRINCIPAL
# -----------------------------------

while True:

    ret, frame = camera.read()

    frame = cv.flip(frame, 1)

    output = frame.copy()


    # -----------------------------------
    # CINZA
    # -----------------------------------

    gray = cv.cvtColor(
        frame,
        cv.COLOR_BGR2GRAY
    )


    # -----------------------------------
    # BLUR FORTE
    # -----------------------------------

    blur = cv.GaussianBlur(
        gray,
        (9, 9),
        0
    )


    # -----------------------------------
    # THRESHOLD
    # -----------------------------------

    _, thresh = cv.threshold(
        blur,
        120,
        255,
        cv.THRESH_BINARY_INV
    )


    # -----------------------------------
    # REMOVE RUÍDO
    # -----------------------------------

    thresh = cv.erode(
        thresh,
        None,
        iterations=2
    )

    thresh = cv.dilate(
        thresh,
        None,
        iterations=2
    )


    # -----------------------------------
    # CONTORNOS
    # -----------------------------------

    contours, _ = cv.findContours(
        thresh,
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )


    direcao = ultima_direcao


    # -----------------------------------
    # ANALISA OBJETOS
    # -----------------------------------

    for contour in contours:

        # Área maior para evitar ruído
        area = cv.contourArea(contour)

        if area > 7000:

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

            # Desenha
            cv.drawContours(
                output,
                [approx],
                -1,
                (0, 255, 0),
                3
            )


            # -----------------------------------
            # PONTOS
            # -----------------------------------

            pontos = approx.reshape(-1, 2)

            xs = pontos[:, 0]

            min_x = np.min(xs)

            max_x = np.max(xs)

            esquerda = np.sum(
                xs < (min_x + 30)
            )

            direita = np.sum(
                xs > (max_x - 30)
            )


            # -----------------------------------
            # DEAD ZONE
            # -----------------------------------

            diferenca = abs(
                esquerda - direita
            )


            # Se diferença pequena
            # mantém direção atual
            if diferenca < 2:

                direcao = ultima_direcao

            else:

                # DIREITA
                if esquerda < direita:

                    direcao = "DIREITA"

                # ESQUERDA
                else:

                    direcao = "ESQUERDA"

            break


    # -----------------------------------
    # ENVIA SERIAL COM DELAY
    # -----------------------------------

    agora = time.time()

    if agora - ultimo_envio > delay_comando:

        # Só envia se mudou
        if direcao != ultima_direcao:

            # DIREITA
            if direcao == "DIREITA":

                arduino.write(b'R')

            # ESQUERDA
            elif direcao == "ESQUERDA":

                arduino.write(b'L')

            # CENTRO
            else:

                arduino.write(b'C')

            # Atualiza memória
            ultima_direcao = direcao

            # Atualiza tempo
            ultimo_envio = agora


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
        "Servo Estavel",
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