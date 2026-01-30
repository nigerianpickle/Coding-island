from roboflow import Roboflow
import cv2
import os
from dotenv import load_dotenv

# ======= Load API key from .env =========


# ======= Setup Roboflow ========
print("Loading Roboflow workspace...")
rf = Roboflow(api_key="LKMNlvypynSJUmpg6Wf9")
ws = rf.workspace()
print(f"Workspace: {ws.name}")

# Use your exact project ID (without workspace prefix)
project = ws.project("circle-9po6m-sw919")
model = project.version(1).model
print(f"Loaded project: {project.name}")

# ======= Video capture ========
cap = cv2.VideoCapture(0)
FRAME_W = 640
FRAME_H = 480
CENTER_X = FRAME_W // 2
CENTER_Y = FRAME_H // 2
THRESHOLD = 40  # pixels for movement commands

print("Starting detection... Press ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (FRAME_W, FRAME_H))
    cv2.imwrite("temp.jpg", frame)  # Roboflow needs an image file

    # ======= Get predictions from Roboflow =======
    result = model.predict("temp.jpg", confidence=40, overlap=30).json()

    if len(result["predictions"]) > 0:
        pred = result["predictions"][0]
        cx = pred["x"]
        cy = pred["y"]
        w = pred["width"]
        h = pred["height"]

        # ======= Draw bounding box & center =======
        top_left = (int(cx - w/2), int(cy - h/2))
        bottom_right = (int(cx + w/2), int(cy + h/2))
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        cv2.circle(frame, (int(cx), int(cy)), 5, (0, 0, 255), -1)

        # ======= Print detection confirmation =======
        print(f"✅ Circle detected at ({cx:.1f}, {cy:.1f})")

        # ======= Movement directions =======
        error_x = cx - CENTER_X
        error_y = cy - CENTER_Y

        if error_x > THRESHOLD:
            print("MOVE RIGHT")
        elif error_x < -THRESHOLD:
            print("MOVE LEFT")

        if error_y > THRESHOLD:
            print("MOVE DOWN")
        elif error_y < -THRESHOLD:
            print("MOVE UP")

    else:
        print("❌ No circle detected")

    # ======= Show webcam feed =======
    cv2.imshow("Circle Detection", frame)
    if cv2.waitKey(1) == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
