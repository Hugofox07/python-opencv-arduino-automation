import cv2 as cv 

image = cv.imread("lidar1.jpeg")

cv.imshow("Minha imagem", image)

cv.waitKey(0)
cv.destroyAllWindows()