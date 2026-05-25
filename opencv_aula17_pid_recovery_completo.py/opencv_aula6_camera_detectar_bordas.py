import cv2 as cv

# 1. Inicia a captura da câmera
camera = cv.VideoCapture(0)

if not camera.isOpened():
    print("Erro ao abrir a câmera")
    exit()

while True:
    # 2. Lê o frame atual da câmera
    ret, frame = camera.read()
    
    # Se houver erro na captura, para o loop
    if not ret:
        break

    # 3. Processamento (DEVE ser dentro do loop para vídeo)
    # Converte o frame atual para cinza
    cinza = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Detecta bordas no frame atual
    # Ajustei para 50 e 150 para um contorno mais limpo
    bordas = cv.Canny(cinza, 50, 150)

    # 4. Mostra os resultados em tempo real
    cv.imshow("Camera Original", frame)
    cv.imshow("Bordas Detectadas", bordas)
    
    # Pressione 'ESC' para sair
    if cv.waitKey(25) & 0xFF == ord('q'):  # press Q to quit
        break

# 5. Limpeza total
camera.release()
cv.destroyAllWindows()


# mostra imagem original
cv.imshow("Imagem original", camera)

# mostra bordas detectadas
cv.imshow("Bordas detectadas", bordas)

# espera pressionar tecla
cv.waitKey(0)

# fecha janelas
camera.release()
cv.destroyAllWindows()