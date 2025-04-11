from ultralytics import YOLO
import cv2
import pyttsx3  # For optional voice output

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # You can use yolov8n.pt or yolov8s.pt (smaller = faster)

# Start webcam
cap = cv2.VideoCapture(0)
engine = pyttsx3.init()

print("[INFO] Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect objects
    results = model(frame, stream=True)

    # Draw boxes and labels
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

            # Optional: Speak the detected object
            engine.say(f"I see a {label}")
            engine.runAndWait()

    cv2.imshow("Smart Glasses - Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
