# por que usar cinza:reduz processamento.
#robôs usam para: detectar obstáculos,detectar objetos,detectar bordas

import cv2 as cv 

imagem = cv.imread("lidar1.jpeg")

# converter para preto e branco
cinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

cv.imshow("Original", imagem)

cv.imshow("Cinza", cinza)

cv.waitKey(0)

cv.destroyAllWindows()

