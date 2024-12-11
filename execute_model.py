from ultralytics import YOLO
import os

EXECUTE_INFERENCE = input('Point towards the .pt trained model you want to use')
IMAGESF = input('Point towards the folder where the images are stored')
LABELSF = input('Point towards the folder where you want the annotations to be stored: ')
if os.path.exists(EXECUTE_INFERENCE) and EXECUTE_INFERENCE.endswith(".pt"):
    print(f"The file '{EXECUTE_INFERENCE}' exists and ends with .pt ")
else:
    print(f"The file '{EXECUTE_INFERENCE}' either does not exist or does not end with .pt and is probally not a reconized YOLO model")

# Load the model
model = YOLO(rf'{EXECUTE_INFERENCE}')
for i in os.listdir(IMAGESF):
    file_name, file_extension = os.path.splitext(i)
    # Define the confidence threshold (e.g., 0.5)
    conf_threshold = 0.5

    # Run inference with the specified confidence threshold
    results = model(rf"{IMAGESF}\{file_name}{file_extension}", conf=conf_threshold)

    
    result = results[0]  # Get the first result
    boxes = result.boxes.xywh.cpu().numpy()  # Box coordinates (x_center, y_center, width, height)
    confidences = result.boxes.conf.cpu().numpy()  # Confidence scores
    classes = result.boxes.cls.cpu().numpy().astype(int)  # Class ids

    # Output text file path
    output_txt_file = rf"{LABELSF}\{file_name}.txt"

    # Write the results to the text file in YOLO format
    with open(output_txt_file, 'w') as f:
        for i, box in enumerate(boxes):
            f.write(f"{classes[i]} {box[0]} {box[1]} {box[2]} {box[3]} {confidences[i]}\n")

# Optionally, show the image with detections
result.show()
