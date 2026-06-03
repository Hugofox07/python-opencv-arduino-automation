import cv2
import serial
import time

arduino = serial.Serial("COM4", 115200)
time.sleep(2)

servo = 90

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    h, w, _ = frame.shape

    centro_tela = w // 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5
    )

    for (x, y, fw, fh) in faces:

        cx = x + fw // 2

        erro = cx - centro_tela

        if erro > 30:
            servo -= 2

        elif erro < -30:
            servo += 2

        servo = max(0, min(180, servo))

        arduino.write(f"{servo}\n".encode())

        cv2.rectangle(
            frame,
            (x, y),
            (x + fw, y + fh),
            (0, 255, 0),
            2
        )

    # Ler telemetria do laser
    distancia = "Sem leitura"

    if arduino.in_waiting:
        distancia = arduino.readline().decode(
            errors="ignore"
        ).strip()

    cv2.putText(
        frame,
        f"Servo: {servo}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        distancia,
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.imshow("Telemetria Inteligente", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()