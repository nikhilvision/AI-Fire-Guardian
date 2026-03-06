from ultralytics import YOLO
import cv2
import winsound
import time
import requests

# TELEGRAM SETTINGS
BOT_TOKEN = "8665305199:AAHkbDMiZk6EE5uTyR6YKX25JGI0StgwioE"
CHAT_ID = "1700533563"

# Load trained YOLO model
model = YOLO("runs/detect/train7/weights/best.pt")

# Start webcam
cap = cv2.VideoCapture(0)

# Alert cooldown
last_alert_time = 0
cooldown = 10

def send_telegram_alert(image_path):
    # Send message
    msg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(msg_url, data={
        "chat_id": CHAT_ID,
        "text": "🚨 FIRE ALERT DETECTED!"
    })

    # Send photo
    photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as img:
        requests.post(photo_url,
                      data={"chat_id": CHAT_ID},
                      files={"photo": img})

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection
    results = model(frame, conf=0.3)

    fire_detected = False

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if "fire" in label.lower():
                fire_detected = True

    if fire_detected:
        current_time = time.time()

        if current_time - last_alert_time > cooldown:
            print("🔥 FIRE DETECTED!")

            # Alarm
            winsound.Beep(2000, 800)

            # Save screenshot
            filename = f"fire_{int(current_time)}.jpg"
            cv2.imwrite(filename, frame)

            # Send Telegram alert
            send_telegram_alert(filename)

            last_alert_time = current_time

    # Show detection window
    annotated = results[0].plot()
    cv2.imshow("AI Fire Guardian", annotated)

    # Exit with Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()