import cv2
import os
import numpy as np
import pickle

faces = []
labels = []
label_map = {}

data_path = 'users'
label_id = 0

for person_name in os.listdir(data_path):
    person_path = os.path.join(data_path, person_name)
    if not os.path.isdir(person_path):
        continue

    label_map[label_id] = person_name
    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            faces.append(img)
            labels.append(label_id)
    label_id += 1

if len(faces) == 0:
    print("No training images found.")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))
recognizer.save("face_model.yml")

with open("labels.pickle", "wb") as f:
    pickle.dump(label_map, f)

print("Training done with multiple images per user!")
