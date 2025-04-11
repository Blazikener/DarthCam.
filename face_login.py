import cv2
import mediapipe as mp
import pickle

# Load the trained model
with open("face_knn_model.pkl", "rb") as f:
    model = pickle.load(f)

# Init MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Start webcam
cap = cv2.VideoCapture(0)
print("📷 Looking for face...")

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        for landmarks in result.multi_face_landmarks:
            data = []
            for lm in landmarks.landmark:
                data.extend([lm.x, lm.y, lm.z])

            # Predict the name using KNN
            name = model.predict([data])[0]
            print(f"✅ Login Successful! Welcome, {name}")
            cap.release()
            cv2.destroyAllWindows()
            exit()

    cv2.imshow("Face Login", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
