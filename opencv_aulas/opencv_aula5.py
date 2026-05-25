import cv2 as cv 

image = cv.imread("lidar1.jpeg")
# Salva a imagem 
cv.imwrite("nova_imagem.jpg", image)

# informações da imagem
print("Formato:")
print(image.shape)

cv.imshow("Imagem", image)

cv.waitKey(0)

cv.destroyAllWindows()
