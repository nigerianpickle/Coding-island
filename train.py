from ultralytics import YOLO

# Load YOLOv11 nano model
model = YOLO("yolov11n")

# Train on your dataset
model.train(
    data="circle-1/data.yaml",
    epochs=50,
    imgsz=640,
    save=True
)

# The trained weights will be saved in 'runs/train/.../weights/best.pt'
