import sys

print("Python version:", sys.version)

---CELL---

!pip --version

---CELL---

!git --version

---CELL---

!nvidia-smi

---CELL---

!git clone https://github.com/ultralytics/yolov5.git

---CELL---

!pip install -r yolov5/requirements.txt

---CELL---

!python yolov5/detect.py --help

---CELL---

!python yolov5/detect.py \
    --source yolov5/data/images/bus.jpg \
    --weights yolov5s.pt \
    --conf 0.25

---CELL---

from pathlib import Path
from IPython.display import Image, display

# Find the latest YOLOv5 detection folder
detect_dir = Path("yolov5/runs/detect")

folders = sorted(
    [folder for folder in detect_dir.iterdir() if folder.is_dir()],
    key=lambda x: x.stat().st_mtime
)

latest_folder = folders[-1]

# Find the detected image
images = list(latest_folder.glob("*.jpg")) + list(latest_folder.glob("*.jpeg")) + list(latest_folder.glob("*.png"))

print("Result folder:", latest_folder)
print("Detected image:", images[0].name)

display(Image(filename=str(images[0])))

---CELL---

from google.colab import files

uploaded = files.upload()

---CELL---

!python yolov5/detect.py \
    --source traffic_image.jpeg \
    --weights yolov5s.pt \
    --conf 0.25

---CELL---

from IPython.display import Image, display

result_path = "yolov5/runs/detect/exp2/traffic_image.jpeg"

display(Image(filename=result_path))

---CELL---

from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode

def take_photo(filename='webcam.jpg', quality=0.8):
    js = Javascript('''
    async function takePhoto(quality) {
      const div = document.createElement('div');

      const video = document.createElement('video');
      video.style.display = 'block';

      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);

      video.srcObject = stream;
      await video.play();

      await new Promise((resolve) => setTimeout(resolve, 1000));

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      canvas.getContext('2d').drawImage(video, 0, 0);

      stream.getVideoTracks()[0].stop();
      div.remove();

      return canvas.toDataURL('image/jpeg', quality);
    }
    ''')

    display(js)
    data = eval_js('takePhoto({})'.format(quality))

    binary = b64decode(data.split(',')[1])

    with open(filename, 'wb') as f:
        f.write(binary)

    return filename

---CELL---

from IPython.display import Image, display

filename = take_photo('webcam.jpg', quality=0.8)

print("Photo captured successfully:", filename)

display(Image(filename=filename))

---CELL---



---CELL---

!python yolov5/detect.py \
    --source webcam.jpg \
    --weights yolov5s.pt \
    --conf 0.25

---CELL---

from pathlib import Path
from IPython.display import Image, display

detect_dir = Path("yolov5/runs/detect")

folders = sorted(
    [folder for folder in detect_dir.iterdir() if folder.is_dir()],
    key=lambda x: x.stat().st_mtime
)

latest_folder = folders[-1]

result_images = (
    list(latest_folder.glob("*.jpg")) +
    list(latest_folder.glob("*.jpeg")) +
    list(latest_folder.glob("*.png"))
)

print("Result folder:", latest_folder)
display(Image(filename=str(result_images[0])))

---CELL---

from google.colab import files

uploaded_video = files.upload()

---CELL---

!python yolov5/detect.py \
    --source road_traffic_video.mp4 \
    --weights yolov5s.pt \
    --conf 0.25

---CELL---

from pathlib import Path

detect_dir = Path("yolov5/runs/detect")

folders = sorted(
    [folder for folder in detect_dir.iterdir() if folder.is_dir()],
    key=lambda x: x.stat().st_mtime
)

latest_folder = folders[-1]

print("Latest result folder:", latest_folder)

video_files = (
    list(latest_folder.glob("*.mp4")) +
    list(latest_folder.glob("*.avi")) +
    list(latest_folder.glob("*.mov"))
)

if video_files:
    print("Output video:", video_files[0])
else:
    print("No output video found.")

---CELL---

import subprocess

video_path = str(video_files[0])

result = subprocess.run(
    ["ffprobe", "-v", "error",
     "-show_entries", "format=duration,size",
     "-of", "default=noprint_wrappers=1",
     video_path],
    capture_output=True,
    text=True
)

print("Video:", video_path)
print(result.stdout)

---CELL---

import subprocess

input_video = str(video_files[0])
output_video = "road_traffic_detected_playable.mp4"

subprocess.run([
    "ffmpeg",
    "-y",
    "-i", input_video,
    "-c:v", "libx264",
    "-preset", "fast",
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    output_video
], check=True)

print("Converted successfully:", output_video)

---CELL---

from IPython.display import Video, display

display(Video("road_traffic_detected_playable.mp4", embed=True))

---CELL---

