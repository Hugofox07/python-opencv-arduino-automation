import cv2 as cv 
import numpy as np

# Abre webcam
camera = cv.VideoCapture(0)

while True:

    # Captura frame
    ret, frame = camera.read()

    # Espelha imagem
    frame = cv.flip(frame, 1)

    # Tamanho da tela
    altura, largura, _ = frame.shape

    # Converte para HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Faixas do vermelho
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Máscaras
    mask1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)

    # Junta máscaras
    mask = mask1 + mask2

    # Remove ruído
    mask = cv.GaussianBlur(mask, (5, 5), 0)

    # Procura contornos
    contours, _ = cv.findContours(
        mask,
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )

    # Linhas divisórias
    cv.line(frame, (largura // 3, 0),
             (largura // 3, altura),
             (255, 255, 255), 2)

    cv.line(frame, (2 * largura // 3, 0),
             (2 * largura // 3, altura),
             (255, 255, 255), 2)

    # Se encontrou objeto
    if len(contours) > 0:

        # Maior contorno
        largest_contour = max(contours, key=cv.contourArea)

        # Área
        area = cv.contourArea(largest_contour)

        # Ignora ruído
        if area > 500:

            # Centro do objeto
            ((x, y), radius) = cv.minEnclosingCircle(largest_contour)

            center_x = int(x)
            center_y = int(y)

            # Desenha círculo
            cv.circle(
                frame,
                (center_x, center_y),
                int(radius),
                (0, 255, 0),
                2
            )

            # Verifica posição
            if center_x < largura // 3:

                direcao = "ESQUERDA"

            elif center_x < 2 * largura // 3:

                direcao = "CENTRO"

            else:

                direcao = "DIREITA"

            # Mostra direção
            cv.putText(
                frame,
                direcao,
                (50, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

    # Mostra imagem
    cv.imshow("Tracking Direcao", frame)

    # Sai com Q
    if cv.waitKey(1) == ord('q'):
        break

# Fecha câmera
camera.release()

# Fecha janelas
cv.destroyAllWindows()