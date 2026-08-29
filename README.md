# YOLOv5 Self-Driving Object Detection

## Project Overview

This project demonstrates real-time object detection for self-driving vehicle perception using the YOLOv5 deep learning model.

The system uses YOLOv5 to identify objects in road and traffic scenes. It demonstrates object detection on a static traffic image, a real-world traffic video, and a webcam stream. Detected objects are highlighted using bounding boxes along with confidence scores.

The project demonstrates how computer vision can be used as a perception component in autonomous driving systems, where identifying surrounding vehicles, pedestrians, and other objects is important for understanding the road environment.

## Problem Statement

Self-driving vehicles need to continuously understand their surrounding environment in order to make safe decisions. Object detection is an important part of this perception process because it helps identify vehicles, pedestrians, traffic-related objects, and other elements present in the road scene.

This project uses YOLOv5 for real-time object detection and demonstrates its application using static images, webcam input, and real-world traffic video.

## Objectives

* Implement object detection using YOLOv5.
* Use the YOLOv5s pre-trained model for detection.
* Detect objects in a static traffic image.
* Perform real-time detection using a webcam.
* Detect objects in a real-world traffic video.
* Display bounding boxes around detected objects.
* Display confidence scores for detected objects.
* Demonstrate the use of object detection for self-driving vehicle perception.

## Technologies Used

* Python
* YOLOv5
* PyTorch
* OpenCV
* Google Colab
* Jupyter Notebook

## Model

The project uses the YOLOv5s pre-trained model.

YOLOv5 is a real-time object detection framework capable of detecting multiple objects in an image or video frame.

The model used in this project is trained on the COCO dataset and can detect common object categories such as:

* Person
* Car
* Motorcycle
* Bus
* Truck
* Bicycle
* Traffic light
* Stop sign
* And other common objects

## Project Workflow

```text
Input Image / Video / Webcam
            |
            v
       YOLOv5s Model
            |
            v
     Object Detection
            |
            v
Bounding Boxes + Confidence Scores
            |
            v
       Detection Output
```

## Project Inputs

The project includes the following input files:

* `traffic_image.jpeg` - Static traffic image used for object detection.
* `road_traffic_video.mp4` - Real-world road traffic video used for video-based object detection.

Webcam input is captured directly through the computer camera during the webcam detection section.

## Detection Tasks

### 1. Static Image Detection

A traffic image is provided as input to the YOLOv5 model. The model detects objects present in the image and displays bounding boxes with their corresponding confidence scores.

### 2. Webcam Detection

The system accesses the webcam and performs object detection on the live camera stream. Detected objects are displayed in real time with bounding boxes and confidence scores.

### 3. Traffic Video Detection

A real-world traffic video is processed frame by frame using YOLOv5. Objects detected in the video are highlighted with bounding boxes and confidence scores.

This demonstrates how object detection can be applied to dynamic road scenes for self-driving vehicle perception.

## Confidence Score

The confidence score represents how confident the YOLOv5 model is that a detected object belongs to a particular class.

For example:

```text
person 0.95
```

means that the model has assigned a confidence score of approximately 95% to that detection.

## Repository Structure

```text
YOLOv5_Self_Driving_Object_Detection/
|
|-- YOLOv5_Self_Driving_Object_Detection.ipynb
|-- README.md
|-- traffic_image.jpeg
|-- road_traffic_video.mp4
```

## Notebook

The complete implementation is available in:

`YOLOv5_Self_Driving_Object_Detection.ipynb`

The notebook contains the setup, model loading, image detection, webcam detection, and traffic video detection steps.

## How to Run

### Google Colab

1. Open `YOLOv5_Self_Driving_Object_Detection.ipynb` in Google Colab.
2. Run the notebook cells sequentially.
3. Install the required YOLOv5 dependencies when prompted by the notebook.
4. Load the YOLOv5s model.
5. Provide the required input image or video.
6. Run the detection cells.
7. For webcam detection, allow camera access when requested.
8. View the detection results produced by the model.

## Results

The project successfully demonstrates:

* Object detection on traffic images.
* Real-time object detection using a webcam.
* Object detection on road traffic video.
* Bounding boxes around detected objects.
* Confidence scores for detected objects.

These results demonstrate the potential use of YOLOv5 as a computer vision component in autonomous driving perception systems.

## Applications

Object detection systems similar to this project can be used in:

* Autonomous vehicles
* Advanced Driver Assistance Systems (ADAS)
* Traffic monitoring
* Road safety systems
* Pedestrian detection
* Vehicle detection
* Intelligent transportation systems

## Limitations

* The project uses a pre-trained YOLOv5 model rather than a custom-trained model.
* Detection performance depends on the quality and conditions of the input image or video.
* Performance can vary depending on available hardware.
* The project demonstrates object detection as a perception component and does not implement complete autonomous vehicle control or decision-making.

## Future Improvements

The project can be extended by:

* Training YOLOv5 on a custom road-traffic dataset.
* Adding more specialized traffic-related classes.
* Improving detection performance in difficult weather and lighting conditions.
* Integrating object tracking.
* Adding distance estimation for detected objects.
* Integrating the detection system with autonomous driving decision-making modules.

## Conclusion

This project demonstrates the application of YOLOv5 for real-time object detection in self-driving vehicle perception scenarios. By processing static images, webcam streams, and real-world traffic videos, the project shows how deep learning and computer vision can be used to identify and localize objects in road environments.

The implementation provides a practical introduction to using YOLOv5 for autonomous driving perception and real-time computer vision applications.

## Author

Developed as an AI and Machine Learning project using Python, YOLOv5, PyTorch, and OpenCV.

