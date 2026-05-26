# =========================================================
# OpenCV
# =========================================================

import cv2 as cv

# =========================================================
# Numpy
# =========================================================

import numpy as np

# =========================================================
# Sistema
# =========================================================

import math
import time

# =========================================================
# Histórico
# =========================================================

from collections import deque

# =========================================================
# Arduino
# =========================================================

import serial


# =========================================================
# ARDUINO
# =========================================================

arduino = serial.Serial(
    'COM4',
    9600
)

time.sleep(2)

angulo_servo = 90

arduino.write(b'90\n')

time.sleep(2)


# =========================================================
# PARÂMETROS
# =========================================================

CANNY_LOW = 50
CANNY_HIGH = 150

HOUGH_THRESH = 40
MIN_LINE_LEN = 60
MAX_LINE_GAP = 150

ROI_TOP_RATIO = 0.55
ROI_BOTTOM_RATIO = 1.0

SMOOTH_FRAMES = 8


# =========================================================
# CORES
# =========================================================

COLOR_LANE = (0,255,100)
COLOR_CENTER = (255,255,255)
COLOR_STEER = (0,100,255)


# =========================================================
# HISTÓRICO
# =========================================================

left_history = deque(maxlen=SMOOTH_FRAMES)
right_history = deque(maxlen=SMOOTH_FRAMES)


# =========================================================
# ROI
# =========================================================

def region_of_interest(img, vertices):

    mask = np.zeros_like(img)

    cv.fillPoly(
        mask,
        vertices,
        255
    )

    return cv.bitwise_and(
        img,
        mask
    )


# =========================================================
# DESENHA LINHAS
# =========================================================

def draw_line(frame, line, color):

    if line is None:
        return

    try:

        x1, y1, x2, y2 = line

        cv.line(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            5
        )

    except:
        pass


# =========================================================
# MÉDIA DAS LINHAS
# =========================================================

def average_slope_intercept(frame, lines):

    left_fit = []
    right_fit = []

    if lines is None:
        return None, None

    for line in lines:

        x1, y1, x2, y2 = line.reshape(4)

        if x1 == x2:
            continue

        slope = (
            (y2 - y1) /
            (x2 - x1)
        )

        intercept = y1 - slope * x1

        # Ignora linhas ruins
        if abs(slope) < 0.5:
            continue

        if abs(slope) > 2.5:
            continue

        if slope < 0:

            left_fit.append(
                (slope, intercept)
            )

        else:

            right_fit.append(
                (slope, intercept)
            )

    h = frame.shape[0]

    y1 = h
    y2 = int(h * ROI_TOP_RATIO)

    # -----------------------------------
    # ESQUERDA
    # -----------------------------------

    left_line = None

    if len(left_fit) > 0:

        slope, intercept = np.mean(
            left_fit,
            axis=0
        )

        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)

        left_line = (x1, y1, x2, y2)

    # -----------------------------------
    # DIREITA
    # -----------------------------------

    right_line = None

    if len(right_fit) > 0:

        slope, intercept = np.mean(
            right_fit,
            axis=0
        )

        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)

        right_line = (x1, y1, x2, y2)

    return left_line, right_line


# =========================================================
# SUAVIZA LINHAS
# =========================================================

def smooth_line(history, new_line):

    if new_line is not None:

        history.append(new_line)

    if len(history) == 0:
        return None

    avg = np.mean(
        history,
        axis=0
    ).astype(int)

    return tuple(avg)


# =========================================================
# ÂNGULO DIREÇÃO
# =========================================================

def compute_steering_angle(
    frame,
    left_line,
    right_line
):

    h, w = frame.shape[:2]

    center_x = w // 2

    # -----------------------------------
    # DUAS LINHAS
    # -----------------------------------

    if left_line is not None and right_line is not None:

        _, _, lx2, _ = left_line
        _, _, rx2, _ = right_line

        lane_center = (
            lx2 + rx2
        ) // 2

    # -----------------------------------
    # APENAS ESQUERDA
    # -----------------------------------

    elif left_line is not None:

        _, _, lx2, _ = left_line

        lane_center = lx2 + w // 4

    # -----------------------------------
    # APENAS DIREITA
    # -----------------------------------

    elif right_line is not None:

        _, _, rx2, _ = right_line

        lane_center = rx2 - w // 4

    else:

        return 0

    # -----------------------------------
    # OFFSET
    # -----------------------------------

    x_offset = lane_center - center_x

    y_offset = int(h * 0.35)

    angle_rad = math.atan(
        x_offset / y_offset
    )

    angle_deg = math.degrees(
        angle_rad
    )

    return angle_deg


# =========================================================
# PROCESSA FRAME
# =========================================================

def process_frame(frame):

    global angulo_servo

    h, w = frame.shape[:2]

    # =====================================================
    # CINZA
    # =====================================================

    gray = cv.cvtColor(
        frame,
        cv.COLOR_BGR2GRAY
    )

    # =====================================================
    # BLUR
    # =====================================================

    blur = cv.GaussianBlur(
        gray,
        (5,5),
        0
    )

    # =====================================================
    # CANNY
    # =====================================================

    edges = cv.Canny(
        blur,
        CANNY_LOW,
        CANNY_HIGH
    )

    # =====================================================
    # ROI
    # =====================================================

    vertices = np.array([[
        (int(w * 0.05), h),
        (int(w * 0.40), int(h * ROI_TOP_RATIO)),
        (int(w * 0.60), int(h * ROI_TOP_RATIO)),
        (int(w * 0.95), h)
    ]], dtype=np.int32)

    masked = region_of_interest(
        edges,
        vertices
    )

    # =====================================================
    # HOUGH
    # =====================================================

    lines = cv.HoughLinesP(
        masked,
        1,
        np.pi / 180,
        HOUGH_THRESH,
        minLineLength=MIN_LINE_LEN,
        maxLineGap=MAX_LINE_GAP
    )

    # =====================================================
    # LINHAS MÉDIAS
    # =====================================================

    left_raw, right_raw = average_slope_intercept(
        frame,
        lines
    )

    left_line = smooth_line(
        left_history,
        left_raw
    )

    right_line = smooth_line(
        right_history,
        right_raw
    )

    # =====================================================
    # DESENHA
    # =====================================================

    draw_line(
        frame,
        left_line,
        COLOR_LANE
    )

    draw_line(
        frame,
        right_line,
        COLOR_LANE
    )

    # =====================================================
    # ÂNGULO
    # =====================================================

    angle = compute_steering_angle(
        frame,
        left_line,
        right_line
    )

    # =====================================================
    # DEAD ZONE
    # =====================================================

    if abs(angle) < 4:

        angle = 0

    # =====================================================
    # CONVERTE PARA SERVO
    # =====================================================

    alvo = int(
        90 + angle
    )

    alvo = max(
        60,
        min(120, alvo)
    )

    # =====================================================
    # SUAVIZAÇÃO SERVO
    # =====================================================

    velocidade = 2

    if angulo_servo < alvo:

        angulo_servo += velocidade

    elif angulo_servo > alvo:

        angulo_servo -= velocidade

    # =====================================================
    # SERIAL
    # =====================================================

    comando = f"{angulo_servo}\n"

    arduino.write(
        comando.encode()
    )

    time.sleep(0.02)

    # =====================================================
    # LINHA CENTRO
    # =====================================================

    cv.line(
        frame,
        (w//2, h),
        (w//2, int(h*ROI_TOP_RATIO)),
        COLOR_CENTER,
        2
    )

    # =====================================================
    # TEXTO
    # =====================================================

    cv.putText(
        frame,
        f'Servo: {angulo_servo}',
        (20,40),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,255),
        2
    )

    cv.putText(
        frame,
        f'Angle: {angle:.1f}',
        (20,80),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        2
    )

    return frame


# =========================================================
# MAIN
# =========================================================

def main():

    cap = cv.VideoCapture(
        "souces/Lane Detection.mp4"
    )

    if not cap.isOpened():

        print("Erro ao abrir vídeo")
        return

    while True:

        ret, frame = cap.read()

        if not ret:

            cap.set(
                cv.CAP_PROP_POS_FRAMES,
                0
            )

            continue

        frame = cv.resize(
            frame,
            (1280,720)
        )

        result = process_frame(
            frame
        )

        cv.imshow(
            "Lane Detection Estavel",
            result
        )

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    cv.destroyAllWindows()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    main()