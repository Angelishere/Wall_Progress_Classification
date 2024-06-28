from ultralytics import YOLO
import numpy as np

# Load the YOLOv8 model with trained weights
model = YOLO('last.pt')

results = model('test_image3.jpg')  # predict on an image

names_dict = results[0].names

probs = results[0].probs.data.tolist()

print(names_dict)
print(probs)

print(names_dict[np.argmax(probs)])