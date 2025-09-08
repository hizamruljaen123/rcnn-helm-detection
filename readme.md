# Helmet Detection using RCNN

## Introduction
Helmet detection is a computer vision task aimed at identifying whether a person is wearing a helmet or not.  
RCNN (Region-based Convolutional Neural Network) is widely used for object detection tasks by generating region proposals and classifying them with CNN.

## How It Works
1. Generate region proposals (candidate bounding boxes).
2. Extract features from each region using CNN.
3. Classify each region as "helmet" or "no helmet".
4. Refine bounding boxes.

## Python Implementation (Simplified)
Below is a simplified example using TensorFlow and Keras with Faster-RCNN pre-trained weights.

```python
import tensorflow as tf
import cv2
import numpy as np

# Load a pre-trained Faster R-CNN model (COCO dataset)
model = tf.saved_model.load("ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/saved_model")

# Load test image
image = cv2.imread("worker.jpg")
input_tensor = tf.convert_to_tensor([image], dtype=tf.uint8)

# Perform detection
detections = model(input_tensor)

# Extract results
boxes = detections["detection_boxes"][0].numpy()
scores = detections["detection_scores"][0].numpy()
classes = detections["detection_classes"][0].numpy().astype(int)

# Display detected helmets
for i in range(len(scores)):
    if scores[i] > 0.5:  # confidence threshold
        class_id = classes[i]
        y1, x1, y2, x2 = boxes[i]
        h, w, _ = image.shape
        cv2.rectangle(image, (int(x1*w), int(y1*h)), (int(x2*w), int(y2*h)), (0,255,0), 2)

cv2.imshow("Helmet Detection", image)
cv2.waitKey(0)
