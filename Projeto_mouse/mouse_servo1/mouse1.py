import cv2 as cv 
import serial
import time

# ==========================================
# SERIAL
# ==========================================

arduino = serial.Serial('COM4', 115200)

time.sleep(2)

# ==========================================
# CAMERA
# ==========================================

largura = 640
altura = 480

cap = cv.VideoCapture(0)

cap.set(cv.CAP_PROP_FRAME_WIDTH, largura)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, altura)

# ==========================================
# VARIAVEIS
# ==========================================

angulo = 90
ultimo_envio = 90

# ==========================================
# MOUSE
# ==========================================

def mover_mouse(event, x, y, flags, param):

    global angulo

    if event == cv.EVENT_MOUSEMOVE:

        # Converte posição do mouse
        angulo = int((x / largura) * 180)

        angulo = max(0, min(180, angulo))

# ==========================================
# JANELA
# ==========================================

cv.namedWindow("Camera")

cv.setMouseCallback("Camera", mover_mouse)

# ==========================================
# LOOP
# ==========================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Linha central
    cv.line(
        frame,
        (largura // 2, 0),
        (largura // 2, altura),
        (0, 255, 0),
        2
    )

    # Texto
    cv.putText(
        frame,
        f"Angulo: {angulo}",
        (20, 40),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Só envia se diferença for maior
    if abs(angulo - ultimo_envio) >= 2:

        arduino.write(f"{angulo}\n".encode())

        ultimo_envio = angulo

    cv.imshow("Camera", frame)

    tecla = cv.waitKey(1)

    if tecla == 27:
        break

cap.release()

cv.destroyAllWindows()