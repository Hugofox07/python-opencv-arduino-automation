import cv2 as cv 

# Abre webcam
camera = cv.VideoCapture(0)

while True:

    # Captura frame
    ret, frame = camera.read()

    # Espelha imagem
    frame = cv.flip(frame, 1)

    # Pega tamanho da tela
    altura, largura, _ = frame.shape

    # Linha esquerda
    cv.line(
        frame,
        (largura // 2 - 150, altura),
        (largura // 2 - 50, altura // 2),
        (0, 255, 0),
        3
    )

    # Linha direita
    cv.line(
        frame,
        (largura // 2 + 150, altura),
        (largura // 2 + 50, altura // 2),
        (0, 255, 0),
        3
    )

    # Linha central
    cv.line(
        frame,
        (largura // 2, altura),
        (largura // 2, altura // 2),
        (0, 0, 255),
        2
    )

    # Texto
    cv.putText(
        frame,
        "Sistema de Re",
        (20, 40),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    # Mostra tela
    cv.imshow("Camera de Re", frame)

    # Sai com Q
    if cv.waitKey(1) == ord('q'):
        break

# Fecha camera
camera.release()

# Fecha janelas
cv.destroyAllWindows()