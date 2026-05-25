import cv2 as cv
import numpy as np 

# abre camera
camera = cv.VideoCapture(0)

if not camera.isOpened():
    print("Erro ao abrir a câmera")
    exit()

while True:

 # captura imagem da camera    
    ret, frame = camera.read()
    
     # Se houver erro na captura, para o loop
    if not ret:
        break
    
    # converte imagem para formato HSV
    # HSV é melhor para detectar cores
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
     # faixa de cor do fogo (aproximada)
    cor_min = np.array([0,120,150])
    cor_max = np.array([35,255,255]) 
    
     # cria máscara mostrando apenas a cor do fogo
    mascara = cv.inRange(hsv, cor_min, cor_max)
    
     # aplica máscara na imagem original
    resultado = cv.bitwise_and(frame, frame, mask=mascara)
    
     # mostra imagem normal
    cv.imshow("camera", frame )
    
    # mostra imagem normal
    cv.imshow("Camera", frame)

    # mostra areas detectadas (possivel fogo)
    cv.imshow("Fogo detectado", resultado)

    # sair ao pressionar ESC
    if cv.waitKey(1) == 27:
        break

# libera camera
camera.release()

# fecha janelas
cv.destroyAllWindows()
    
    