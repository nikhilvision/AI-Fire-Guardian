from ultralytics import YOLO
import cv2
import torch
import numpy as np
import winsound

model = YOLO("yolov8n.pt")
model.to("cuda")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 2 != 0:
        continue

    results = model(frame, imgsz=480)
    annotated_frame = results[0].plot()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_fire = np.array([0, 50, 50])
    upper_fire = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower_fire, upper_fire)

    fire_pixels = cv2.countNonZero(mask)

    if fire_pixels > 4000:
        cv2.putText(annotated_frame, "FIRE SUSPECTED!", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        winsound.Beep(800, 200)

    cv2.imshow("AI Fire Guardian", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()