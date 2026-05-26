import cv2 as cv
import numpy as np

print("OpenCV instalado com sucesso! Versão:", cv.__version__)

# Cria uma imagem preta de 400x400 pixels para testar a janela gráfica
imagem_teste = np.zeros((400, 400, 3), dtype="uint8")

cv.imshow("Teste OpenCV", imagem_teste)
cv.waitKey(0)  # Espera você apertar qualquer tecla para fechar
cv.destroyAllWindows()