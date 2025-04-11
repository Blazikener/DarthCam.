import face_recognition
import cv2
import pickle
import os

FACE_DIR = "known_faces"
os.makedirs(FACE_DIR, exist_ok=True)

def save_face_encoding(name):
    cap = cv2.VideoCapture(0)
    st, frame = cap.read()
    cap.release()
    
    encodings = face_recognition.face_encodings(frame)
    if encodings:
        encoding = encodings[0]
        with open(f"{FACE_DIR}/{name}.pkl", "wb") as f:
            pickle.dump(encoding, f)
        return f"Face saved for {name}"
    return "No face detected!"

def recognize_face():
    cap = cv2.VideoCapture(0)
    st, frame = cap.read()
    cap.release()

    current_encodings = face_recognition.face_encodings(frame)
    if not current_encodings:
        return "No face detected"

    current_encoding = current_encodings[0]
    for file in os.listdir(FACE_DIR):
        with open(f"{FACE_DIR}/{file}", "rb") as f:
            known_encoding = pickle.load(f)
            match = face_recognition.compare_faces([known_encoding], current_encoding)
            if match[0]:
                return f"Login successful: {file[:-4]}"
    return "Face not recognized"
'''if __name__ == "__main__":
    print("[1] Signup")
    print("[2] Login")
    choice = input("Select: ")
    if choice == "1":
        name = input("Enter name: ")
        print(save_face_encoding(name))
    else:
        print(recognize_face())'''
