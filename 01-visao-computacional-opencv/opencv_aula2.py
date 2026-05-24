import cv2 as cv 

image = cv.imread("lidar1.jpeg")

# informações da imagem
print("Formato:")
print(image.shape)
print(image[0,0])

cv.imshow("Imagem", image)

cv.waitKey(0)

cv.destroyAllWindows()
