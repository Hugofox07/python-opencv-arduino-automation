import cv2 as cv
import numpy as np

# abrir camera
camera = cv.VideoCapture(0)

while True:

    # capturar imagem da camera
    ret, frame = camera.read()

    # converter imagem para formato HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # faixa de cor vermelha (parte 1)
    vermelho1_min = np.array([0,120,70])
    vermelho1_max = np.array([10,255,255])

    # faixa de cor vermelha (parte 2)
    vermelho2_min = np.array([170,120,70])
    vermelho2_max = np.array([180,255,255])

    # criar máscaras
    mask1 = cv.inRange(hsv, vermelho1_min, vermelho1_max)

    mask2 = cv.inRange(hsv, vermelho2_min, vermelho2_max)

    # juntar máscaras
    mascara = mask1 + mask2

    # aplicar máscara na imagem
    resultado = cv.bitwise_and(frame, frame, mask=mascara)

    # mostrar imagem normal
    cv.imshow("Camera", frame)

    # mostrar apenas vermelho detectado
    cv.imshow("Vermelho detectado", resultado)

    # sair pressionando ESC
    if cv.waitKey(1) == 27:
        break

camera.release()

cv.destroyAllWindows()