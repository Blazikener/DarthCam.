from ultralytics import YOLO
import cv2
import pyttsx3
import time

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)
engine = pyttsx3.init()

last_spoken = ""
last_spoken_time = 0
speak_interval = 7  # seconds

print("[INFO] Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, stream=True)

    detected_labels = set()

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Draw rectangle and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} ({conf:.2f})", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            detected_labels.add(label)

    # Speak only one object if enough time has passed
    current_time = time.time()
    if detected_labels and current_time - last_spoken_time > speak_interval:
        to_speak = detected_labels.pop()
        if to_speak != last_spoken:
            engine.say(f"I see a {to_speak}")
            engine.runAndWait()
            last_spoken = to_speak
            last_spoken_time = current_time

    cv2.imshow("Smart Glasses - Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
