import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import os

# Load model
model = load_model("asl_image_model.h5")

# Labels (based on folder names from your training)
labels = sorted(os.listdir("E:/asl_dataset"))

# Image settings
IMG_SIZE = 64

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Draw a rectangle where the hand should be shown
    x1, y1, x2, y2 = 100, 100, 300, 300
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
    roi = frame[y1:y2, x1:x2]

    # Preprocess ROI for model
    img = cv2.resize(roi, (IMG_SIZE, IMG_SIZE))
    img = img.astype("float") / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)

    # Predict
    preds = model.predict(img)[0]
    max_idx = np.argmax(preds)
    label = labels[max_idx]
    confidence = preds[max_idx] * 100

    # Display prediction
    cv2.putText(frame, f"{label.upper()} ({confidence:.1f}%)", (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("ASL Sign Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
