import cv2 as cv 

# abrir camera
camera = cv.VideoCapture(0)

# capturar primeiro frame
ret, frame1 = camera.read()

# converter para cinza
frame1_cinza = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)

# reduzir ruído
frame1_cinza = cv.GaussianBlur(frame1_cinza, (5,5), 0)

while True:

    # capturar novo frame
    ret, frame2 = camera.read()

    # converter para cinza
    frame2_cinza = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)

    # reduzir ruído
    frame2_cinza = cv.GaussianBlur(frame2_cinza, (5,5), 0)

    # calcular diferença entre imagens
    diferenca = cv.absdiff(frame1_cinza, frame2_cinza)

    # transformar diferença em preto e branco
    _, movimento = cv.threshold(diferenca, 25, 255, cv.THRESH_BINARY)

    # mostrar movimento detectado
    cv.imshow("Movimento detectado", movimento)

    # atualizar frame anterior
    frame1_cinza = frame2_cinza

    # sair pressionando ESC
    if cv.waitKey(1) == 27:
        break

camera.release()

cv.destroyAllWindows()


    
