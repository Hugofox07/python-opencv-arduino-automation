# =====================================================
# OpenCV
# =====================================================

import cv2 as cv

# =====================================================
# YOLO
# =====================================================

from ultralytics import YOLO

# =====================================================
# CARREGA MODELO
# =====================================================

model = YOLO("yolov8n.pt")

# =====================================================
# CÂMERA
# =====================================================

cap = cv.VideoCapture(0)

# =====================================================
# LOOP
# =====================================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    altura, largura = frame.shape[:2]

    centro_tela_x = largura // 2
    centro_tela_y = altura // 2

    # Linha vertical
    cv.line(
        frame,
        (centro_tela_x, 0),
        (centro_tela_x, altura),
        (255,255,255),
        2
    )

    # Linha horizontal
    cv.line(
        frame,
        (0, centro_tela_y),
        (largura, centro_tela_y),
        (255,255,255),
        2
    )

    # ==========================================
    # YOLO
    # ==========================================

    results = model(
        frame,
        conf=0.5,
        imgsz=320
    )

    # ==========================================
    # PERCORRE RESULTADOS
    # ==========================================

    for r in results:

        for box in r.boxes:

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            confianca = float(
                box.conf[0]
            )

            classe = int(
                box.cls[0]
            )

            nome = model.names[
                classe
            ]

            # Centro do objeto
            centro_x = (
                x1 + x2
            ) // 2

            centro_y = (
                y1 + y2
            ) // 2

            # Caixa
            cv.rectangle(
                frame,
                (x1,y1),
                (x2,y2),
                (0,255,0),
                2
            )

            # Centro do objeto
            cv.circle(
                frame,
                (centro_x, centro_y),
                5,
                (0,0,255),
                -1
            )

            texto = (
                f"{nome} "
                f"{confianca:.2f}"
            )

            cv.putText(
                frame,
                texto,
                (x1, y1 - 10),
                cv.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2
            )

            # Coordenadas
            cv.putText(
                frame,
                f"X:{centro_x} Y:{centro_y}",
                (x1, y2 + 20),
                cv.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,255),
                2
            )

            # Terminal
            print(
                f"Objeto: {nome} | "
                f"Conf: {confianca:.2f} | "
                f"Centro: ({centro_x},{centro_y})"
            )

    cv.imshow(
        "YOLO Aula 21",
        frame
    )

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv.destroyAllWindows()