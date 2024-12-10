from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")  # pretrained YOLO11n model

# Run batched inference on a list of images
results = model(["bus.jpg"])  # return a list of Results objects
results[0].show()  # display to screen