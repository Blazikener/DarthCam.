import cv2
import os

# Create user folder
name = input("Enter your name: ").strip()
user_dir = os.path.join('users', name)
if not os.path.exists(user_dir):
    os.makedirs(user_dir)

cam = cv2.VideoCapture(0)
cv2.namedWindow("Capturing Face Data")

print("Collecting face data... Press 'q' to stop.")

img_count = 0
while True:
    ret, frame = cam.read()
    if not ret:
        break

    cv2.imshow("Capturing Face Data", frame)

    # Save every few frames
    if img_count < 30:
        img_path = os.path.join(user_dir, f"{name}_{img_count}.jpg")
        cv2.imwrite(img_path, frame)
        img_count += 1
    if img_count==30:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
print(f"[INFO] Collected {img_count} images for {name}")
