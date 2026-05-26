import cv2 as cv

cap = cv.VideoCapture("sources/estrada1.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv.imshow("Video", frame)

    if cv.waitKey(25) & 0xFF == ord('q'):  # press Q to quit
        break

cap.release()
cv.destroyAllWindows()