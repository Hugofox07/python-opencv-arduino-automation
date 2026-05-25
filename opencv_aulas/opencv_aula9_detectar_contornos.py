import cv2 as cv 

# abrir camera
camera = cv.VideoCapture(0)

while True:

    # capturar imagem da camera
    ret, frame = camera.read()

    # converter imagem para escala de cinza
    cinza = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # detectar bordas da imagem
    bordas = cv.Canny(cinza, 50, 150)

    # encontrar contornos dos objetos
    contornos, _ = cv.findContours(
        bordas,
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )

    # desenhar contornos encontrados
    cv.drawContours(
        frame,
        contornos,
        -1,
        (0,255,0),
        2
    )

    # mostrar imagem com contornos
    cv.imshow("Objetos detectados", frame)

    # sair ao pressionar ESC
    if cv.waitKey(1) == 27:
        break

# liberar camera
camera.release()

# fechar janelas
cv.destroyAllWindows()

