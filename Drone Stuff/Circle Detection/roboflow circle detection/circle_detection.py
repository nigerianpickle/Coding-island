from roboflow import Roboflow
import cv2

rf = Roboflow(api_key="LKMNlvypynSJUmpg6Wf9")
ws = rf.workspace()
project = ws.project("circle-9po6m-sw919")  # <-- use your exact project ID
model = project.version(1).model

cap = cv2.VideoCapture(0)  # webcam

FRAME_W = 640
FRAME_H = 480
CENTER_X = FRAME_W // 2
CENTER_Y = FRAME_H // 2
THRESHOLD = 40  # pixels

print("Starting circle detection... Press ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (FRAME_W, FRAME_H))
    cv2.imwrite("temp.jpg", frame)  # Roboflow API needs an image file

    # Get predictions from hosted Roboflow model
    result = model.predict("temp.jpg", confidence=40, overlap=30).json()

    if len(result["predictions"]) > 0:
        # Just take the first detection
        pred = result["predictions"][0]
        cx = pred["x"]
        cy = pred["y"]
        w = pred["width"]
        h = pred["height"]

        print(f"Circle center: ({cx:.1f}, {cy:.1f}) | size: ({w:.1f}x{h:.1f})")

        # Simulated drone movement
        error_x = cx - CENTER_X
        error_y = cy - CENTER_Y
        box_area = w * h

        if error_x > THRESHOLD:
            print("MOVE RIGHT")
        elif error_x < -THRESHOLD:
            print("MOVE LEFT")

        if error_y > THRESHOLD:
            print("MOVE DOWN")
        elif error_y < -THRESHOLD:
            print("MOVE UP")

        if box_area < 7000:
            print("MOVE FORWARD")
        else:
            print("TARGET REACHED")

    # Show webcam feed
    cv2.imshow("Circle Detection", frame)
    if cv2.waitKey(1) == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
