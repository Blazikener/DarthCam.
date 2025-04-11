import os
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras import layers, models, Input, Model
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode = True, max_num_hands = 1, min_detection_confidence = 0.4)

def extract_hand_landmarks(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return np.zeros(42)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.append(lm.x)
                landmarks.append(lm.y)
            return np.array(landmarks)
    return np.zeros(42)

def load_and_preprocess_image(image_path, img_size = (224, 224)):
    image = cv2.imread(image_path)
    if image is None:
        image = np.zeros((img_size[0], img_size[1], 3), dtype = np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, img_size)
    image = preprocess_input(image) 
    return image

data_dir = 'E:/asl_dataset'
images = []
landmarks = []
labels = []

for label_dir in os.listdir(data_dir):
    if label_dir.isdigit(): 
        continue

    label_path = os.path.join(data_dir, label_dir)
    if os.path.isdir(label_path):
        for file in os.listdir(label_path):
            file_path = os.path.join(label_path, file)
            if os.path.isfile(file_path):
                img = load_and_preprocess_image(file_path)
                lm = extract_hand_landmarks(file_path)
                images.append(img)
                landmarks.append(lm)
                labels.append(label_dir)

images = np.array(images)
landmarks = np.array(landmarks)
labels = np.array(labels)
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)
num_classes = len(label_encoder.classes_)
labels_categorical = to_categorical(labels_encoded, num_classes)
np.save('classes.npy', label_encoder.classes_)
X_img_train, X_img_test, X_lm_train, X_lm_test, y_train, y_test = train_test_split(images, landmarks, labels_categorical, test_size = 0.2, random_state = 42)
base_model = EfficientNetB0(include_top = False, input_shape = (224,224,3), pooling = 'avg')
base_model.trainable = False

image_input = Input(shape = (224,224,3), name = 'image_input')
x1 = base_model(image_input)
x1 = layers.BatchNormalization()(x1)

landmark_input = Input(shape = (42,), name = 'landmark_input')
x2 = layers.Dense(64, activation = 'relu')(landmark_input)
x2 = layers.BatchNormalization()(x2)
x2 = layers.Dropout(0.3)(x2)

combined = layers.concatenate([x1, x2])
combined = layers.Dense(128, activation = 'relu')(combined)
combined = layers.BatchNormalization()(combined)
combined = layers.Dropout(0.4)(combined)
output = layers.Dense(num_classes, activation = 'softmax')(combined)

model = Model(inputs = [image_input, landmark_input], outputs = output)
model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
model.summary()
history = model.fit(
    {'image_input': X_img_train, 'landmark_input': X_lm_train},
    y_train,
    epochs = 10,
    batch_size = 32,
    validation_data = (
        {'image_input': X_img_test, 'landmark_input': X_lm_test},
        y_test
    )
)
import sklearn
print(sklearn.__version__)
model.save('Sign_language_detector.h5')








