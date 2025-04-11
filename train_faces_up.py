import os
import pickle
from sklearn.neighbors import KNeighborsClassifier

X, y = [], []

for file in os.listdir("faces_data"):
    label = file.split(".")[0]
    with open(f"faces_data/{file}", "rb") as f:
        data = pickle.load(f)
        X.extend(data)
        y.extend([label] * len(data))

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)

with open("face_knn_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Face model trained and saved.")
