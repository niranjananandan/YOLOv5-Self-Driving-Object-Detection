# YOLOv5 Self-Driving Object Detection 🚗

## Project Overview

This project demonstrates real-time object detection for self-driving vehicle perception using the YOLOv5 deep learning model. 

It now includes a **beautiful, fully-functional web application** built with Streamlit, allowing users to easily upload images and videos, adjust confidence thresholds, and instantly view the AI's detection results right in their browser.

The system uses YOLOv5 to identify objects in road and traffic scenes, highlighting detected objects (like vehicles, pedestrians, traffic lights, etc.) using bounding boxes along with confidence scores.

## Live Demo & Deployment

The web application is designed to be easily deployed for free on **Streamlit Community Cloud**.

**To deploy your own instance:**
1. Fork or push this repository to your GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **New app**, select this repository, choose `main` branch, and set the main file path to `app.py`.
4. Click **Deploy!**

## Features

* **Streamlit Web Interface:** A sleek, dark-mode web UI for seamless interaction.
* **Image Detection:** Upload static traffic images and instantly get bounding boxes and confidence scores.
* **Video Detection:** Upload real-world traffic videos and watch the AI process them frame-by-frame with a real-time progress bar.
* **Adjustable Confidence:** A slider to tweak the model's confidence threshold on the fly.
* **Jupyter/Colab Notebooks:** Original exploratory notebooks are still included for training and testing.

## Technologies Used

* Python
* Streamlit (Web UI)
* YOLOv5 (Ultralytics)
* PyTorch
* OpenCV (Headless)
* FFmpeg (Video Encoding)

## How to Run Locally

You can run this web application on your own machine.

### Prerequisites

Make sure you have Python 3.8+ installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/YOLOv5-Self-Driving-Object-Detection.git
   cd YOLOv5-Self-Driving-Object-Detection
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```
   *The application will open automatically in your web browser at `http://localhost:8501`.*

## Repository Structure

```text
YOLOv5_Self_Driving_Object_Detection/
|-- app.py                                   # The main Streamlit web application
|-- requirements.txt                         # Dependencies for the web app
|-- YOLOv5_Self_Driving_Object_Detection.ipynb # Original Colab Notebook
|-- traffic_image.jpeg                       # Sample image
|-- road_traffic_video.mp4                   # Sample video
|-- .gitignore                               # Git ignore file (excludes heavy model weights)
```

## Future Improvements

* Add a live webcam feed feature directly inside the Streamlit web app.
* Train YOLOv5 on a custom road-traffic dataset for better accuracy.
* Add distance estimation for detected objects.

## Conclusion

This project demonstrates the application of YOLOv5 for real-time object detection in self-driving vehicle perception scenarios, now made accessible to anyone through a modern web interface.

## Author

Developed as an AI and Machine Learning project using Python, Streamlit, YOLOv5, PyTorch, and OpenCV.
