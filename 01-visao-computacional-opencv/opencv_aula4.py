import cv2 as cv 

camera = cv.VideoCapture(0) # Aqui tambem pode usar camera ip cpm o endereço 

while True:
    ret, frame = camera.read()
    
    cv.imshow("Camera", frame)
    
    # ESC para desligar a camera 
    if cv.waitKey(1) == 27:
        break

camera.release()
cv.destroyAllWindows()
    