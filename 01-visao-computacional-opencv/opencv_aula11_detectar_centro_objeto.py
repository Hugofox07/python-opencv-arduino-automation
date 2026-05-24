import cv2 as cv 

# Abre webcam
camera = cv.VideoCapture(0)

while True:

    # Captura frame
    ret, frame = camera.read()

    # Converte para cinza
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Suaviza imagem
    blur = cv.GaussianBlur(gray, (5, 5), 0)

    # Detecta bordas
    edges = cv.Canny(blur, 50, 150)

    # Procura contornos
    contours, hierarchy = cv.findContours(
        edges,
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )

    # Percorre objetos encontrados
    for contour in contours:

        # Calcula área
        area = cv.contourArea(contour)

        # Ignora objetos pequenos
        if area > 500:

            # Retângulo do objeto
            x, y, w, h = cv.boundingRect(contour)

            # Calcula centro do objeto
            center_x = int(x + w / 2)
            center_y = int(y + h / 2)

            # Desenha retângulo
            cv.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            # Desenha centro
            cv.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 0, 255),
                -1
            )

            # Texto coordenadas
            cv.putText(
                frame,
                f'X:{center_x} Y:{center_y}',
                (x, y - 10),
                cv.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # Mostra imagem
    cv.imshow("Centro do Objeto", frame)

    # Sai com Q
    if cv.waitKey(1) == ord('q'):
        break

# Fecha câmera
camera.release()

# Fecha janelas
cv.destroyAllWindows()