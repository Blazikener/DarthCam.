import cv2
import mediapipe as mp

# Initialize MediaPipe hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Finger tips landmarks (thumb is special)
finger_tips = [8, 12, 16, 20]

def get_hand_sign(landmarks):
    fingers = []

    # Thumb: compare x-coordinates (since it's sideways)
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other 4 fingers: tip higher than PIP joint (tip y < pip y)
    for tip_id in finger_tips:
        if landmarks[tip_id].y < landmarks[tip_id - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    total_fingers = sum(fingers)

    if fingers == [0, 0, 0, 0, 0]:
        return "Rock ✊"
    elif fingers == [1, 1, 1, 1, 1]:
        return "Palm 🖐️"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Scissors ✌️"
    elif fingers == [0, 1, 0, 0, 0]:
        return "Pointing 👉"
    else:
        return f"{total_fingers} fingers"

# Start webcam
cap = cv2.VideoCapture(0)
print("[INFO] Press 'q' to quit")

while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip for mirror effect
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            sign = get_hand_sign(hand_landmarks.landmark)

            cv2.putText(frame, f"Gesture: {sign}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Sign Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
