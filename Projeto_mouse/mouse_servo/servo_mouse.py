import cv2 as cv 
import serial
import time

# =====================================
# CONEXAO SERIAL COM ARDUINO
# =====================================

arduino = serial.Serial('COM4', 9600)

time.sleep(2)

# =====================================
# VARIAVEIS
# =====================================

largura = 640
altura = 480

angulo = 90

# =====================================
# FUNCAO MOUSE
# =====================================

def mover_mouse(event, x, y, flags, param):

    global angulo

    # Converter posição X para ângulo
    angulo = int((x / largura) * 180)

    # Limitar
    angulo = max(0, min(180, angulo))

    # Enviar para Arduino
    arduino.write(f"{angulo}\n".encode())

    print("Angulo:", angulo)

# =====================================
# CAMERA
# =====================================

cap = cv.VideoCapture(0)

cap.set(3, largura)
cap.set(4, altura)

cv.namedWindow("Camera")

cv.setMouseCallback("Camera", mover_mouse)

# =====================================
# LOOP
# =====================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    cv.putText(
        frame,
        f"Angulo Servo: {angulo}",
        (20, 40),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv.imshow("Camera", frame)

    tecla = cv.waitKey(1)

    if tecla == 27:
        break

cap.release()

cv.destroyAllWindows()