from roboflow import Roboflow
import cv2
import time

rf = Roboflow(api_key="LKMNlvypynSJUmpg6Wf9")
project = rf.workspace().project("circle-9po6m-sw919")
model = project.version(1).model

cap = cv2.VideoCapture(0)

FRAME_W = 416   # smaller = faster
FRAME_H = 416
CENTER_X = FRAME_W // 2
CENTER_Y = FRAME_H // 2
THRESHOLD = 40

last_predictions = []
frame_count = 0
INFER_EVERY = 3  # run detection every 3 frames

print("🚀 Faster Roboflow running... ESC to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (FRAME_W, FRAME_H))

    # Only run Roboflow every N frames
    if frame_count % INFER_EVERY == 0:
        start = time.time()
        result = model.predict(frame, confidence=40, overlap=30).json()
        last_predictions = result["predictions"]
        fps = 1 / (time.time() - start)
    frame_count += 1

    # Draw cached predictions (smooth display)
    if len(last_predictions) > 0:
        pred = last_predictions[0]
        cx = pred["x"]
        cy = pred["y"]
        w = pred["width"]
        h = pred["height"]

        top_left = (int(cx - w/2), int(cy - h/2))
        bottom_right = (int(cx + w/2), int(cy + h/2))

        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        cv2.circle(frame, (int(cx), int(cy)), 5, (0, 0, 255), -1)

        # Movement guidance
        error_x = cx - CENTER_X
        error_y = cy - CENTER_Y

        if error_x > THRESHOLD: print("MOVE RIGHT")
        elif error_x < -THRESHOLD: print("MOVE LEFT")

        if error_y > THRESHOLD: print("MOVE DOWN")
        elif error_y < -THRESHOLD: print("MOVE UP")

    cv2.putText(frame, f"Cloud FPS: {fps:.1f}", (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Fast Roboflow", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
