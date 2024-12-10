import os
import torch
from ultralytics import YOLO
import multiprocessing

# Set the environment variable
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


if torch.cuda.is_available():
    print("CUDA is available. PyTorch is using the GPU.")
else:
    print("CUDA is not available. PyTorch is using the CPU.")
# Clear any pre-existing cache
torch.cuda.empty_cache()

def train_model():
    # Load a pretrained YOLOv8 model (you can use 'yolov8n.pt', 'yolov8s.pt', etc.)
    model = YOLO("yolov8n.pt")  # Use your own pretrained model or variant

    # Make sure the model is running on CPU
    model.to(device)

    # Define the path to your custom dataset
    data_yaml = 'data.yaml'  # Points to your dataset and class information

    # Train the model on your custom dataset
    model.train(data=data_yaml, epochs=120, batch=4, imgsz=1280, project="runs/train", name="custom_yolov8")


if __name__ == '__main__':
    # This is required for Windows to handle multiprocessing correctly
    multiprocessing.set_start_method('spawn', force=True)

    # Run the training
    train_model()
