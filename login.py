import cv2
import pickle

# Load the trained recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")

# Load label map
with open("labels.pickle", 'rb') as f:
    labels = pickle.load(f)

# Load Haar cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Open webcam
cam = cv2.VideoCapture(0)
print("Looking for face...")

logged_in = False

while True:
    ret, frame = cam.read()
    if not ret:
        print("Camera error")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        id_, conf = recognizer.predict(roi_gray)

        if 45 <= conf <= 85 and not logged_in:
            name = labels.get(id_, "Unknown")
            print(f"Login successful! Welcome, {name}")
            logged_in = True
            cam.release()
            cv2.destroyAllWindows()
            exit()
        else:
            print("Face not recognized.")

    if cv2.waitKey(20) & 0xFF == 27:  # ESC key to exit
        break

cam.release()
cv2.destroyAllWindows()
