import cv2
import mediapipe as mp
import numpy as np
import pickle
import os
import time

# Setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
os.makedirs("faces_data", exist_ok=True)

name = input("Enter your name: ").strip()
samples = []
cap = cv2.VideoCapture(0)

sample_limit = 20
print(f"📸 Capturing {sample_limit} samples automatically...")
time.sleep(2)

count = 0
start_time = time.time()

while count < sample_limit:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        for landmarks in result.multi_face_landmarks:
            data = []
            for lm in landmarks.landmark:
                data.extend([lm.x, lm.y, lm.z])
            samples.append(data)
            count += 1
            print(f"✅ Captured sample {count}/{sample_limit}")
            time.sleep(0.3)  # Wait a bit to get slightly different poses

    # Show preview
    cv2.putText(frame, f"Capturing: {count}/{sample_limit}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Auto Face Capture", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        print("❌ Cancelled")
        break

cap.release()
cv2.destroyAllWindows()

# Save the captured samples
with open(f"faces_data/{name}.pkl", "wb") as f:
    pickle.dump(samples, f)

print(f"\n🎉 Done! Saved {len(samples)} samples for {name}")
