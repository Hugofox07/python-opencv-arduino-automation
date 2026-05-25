import cv2 as cv 
import numpy as np

# Abre webcam
camera = cv.VideoCapture(0)

while True:

    # Captura frame
    ret, frame = camera.read()

    # Espelha imagem
    frame = cv.flip(frame, 1)

    # Converte para HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Vermelho possui duas faixas no HSV

    # Vermelho escuro
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    # Vermelho claro
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Cria máscaras
    mask1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)

    # Junta máscaras
    mask = mask1 + mask2

    # Remove ruídos
    mask = cv.GaussianBlur(mask, (5, 5), 0)

    # Procura contornos
    contours, _ = cv.findContours(
        mask,
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )

    # Se encontrou objeto
    if len(contours) > 0:

        # Pega maior contorno
        largest_contour = max(contours, key=cv.contourArea)

        # Área
        area = cv.contourArea(largest_contour)

        # Evita ruído pequeno
        if area > 500:

            # Calcula círculo
            ((x, y), radius) = cv.minEnclosingCircle(largest_contour)

            # Centro
            center = (int(x), int(y))

            # Desenha círculo
            cv.circle(
                frame,
                center,
                int(radius),
                (0, 255, 0),
                2
            )

            # Desenha ponto central
            cv.circle(
                frame,
                center,
                5,
                (0, 0, 255),
                -1
            )

            # Texto coordenadas
            cv.putText(
                frame,
                f'X:{int(x)} Y:{int(y)}',
                (int(x) - 40, int(y) - 20),
                cv.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

    # Mostra máscara
    cv.imshow("Mascara Vermelha", mask)

    # Mostra tracking
    cv.imshow("Tracking Vermelho", frame)

    # Sai com Q
    if cv.waitKey(1) == ord('q'):
        break

# Fecha câmera
camera.release()

# Fecha janelas
cv.destroyAllWindows()