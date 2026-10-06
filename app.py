import os
import cv2
import uuid
import torch
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import subprocess
import imageio_ffmpeg
import time

from ultralytics import YOLO

app = FastAPI(title="YOLOv5 Self-Driving Object Detection API")

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load YOLO model using the modern ultralytics package (supports YOLOv5s)
print("Loading YOLOv5 model...")
try:
    model = YOLO('yolov5s.pt')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

# Ensure outputs directory exists
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def cleanup_old_files():
    """Removes output files older than 2 minutes to save space."""
    now = time.time()
    for f in os.listdir(OUTPUT_DIR):
        filepath = os.path.join(OUTPUT_DIR, f)
        if os.path.isfile(filepath):
            # 120 seconds = 2 minutes
            if now - os.path.getmtime(filepath) > 120:
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Failed to delete {filepath}: {e}")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/api/detect/image")
async def detect_image(file: UploadFile = File(...)):
    cleanup_old_files()
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    content = await file.read()
    nparr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform inference (RGB not strictly required for YOLOv8/v5 ultralytics API as it handles BGR natively)
    results = model(img)
    
    # Render results on image (plot returns a BGR image array)
    output_img_bgr = results[0].plot()
    
    # Save output image
    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(OUTPUT_DIR, filename)
    cv2.imwrite(filepath, output_img_bgr)
    
    return {"url": f"/outputs/{filename}", "type": "image"}

@app.post("/api/detect/video")
async def detect_video(file: UploadFile = File(...)):
    cleanup_old_files()

    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video.")

    # Save uploaded video
    input_filename = f"input_{uuid.uuid4().hex}.mp4"
    input_filepath = os.path.join(OUTPUT_DIR, input_filename)
    with open(input_filepath, "wb") as f:
        f.write(await file.read())
        
    output_filename = f"output_{uuid.uuid4().hex}.mp4"
    output_filepath = os.path.join(OUTPUT_DIR, output_filename)
    
    # Open video
    cap = cv2.VideoCapture(input_filepath)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    if fps == 0 or fps > 60:
        fps = 30 # Default to 30 if cannot determine
        
    # Use mp4v codec which is standard in OpenCV. 
    # Note: Modern browsers might not play mp4v inline directly, so we offer a download link.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_filepath, fourcc, fps, (width, height))
    
    frame_count = 0
    # Process max 150 frames to avoid long timeouts during inference for this demo
    max_frames = 150 
    
    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Inference (ultralytics handles BGR)
        results = model(frame)
        
        # plot returns a BGR image array
        output_frame = results[0].plot()
        
        out.write(output_frame)
        frame_count += 1
            
    cap.release()
    out.release()
    
    # Transcode the mp4v video to h264 for web browser compatibility using imageio-ffmpeg
    final_output_filename = f"final_{output_filename}"
    final_output_filepath = os.path.join(OUTPUT_DIR, final_output_filename)
    
    try:
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        subprocess.run([
            ffmpeg_exe, 
            "-y", 
            "-i", output_filepath, 
            "-vcodec", "libx264", 
            "-f", "mp4", 
            final_output_filepath
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Optionally remove the original intermediate file
        os.remove(output_filepath)
        
        output_filename = final_output_filename
    except Exception as e:
        print(f"Error during ffmpeg transcode: {e}")
        # fallback to the original if transcoding failed
    
    return {"url": f"/outputs/{output_filename}", "type": "video"}

@app.get("/outputs/{filename}")
def get_output(filename: str):
    filepath = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(filepath):
        # determine media type
        if filename.endswith(".mp4"):
            media_type = "video/mp4"
        else:
            media_type = "image/jpeg"
        return FileResponse(filepath, media_type=media_type)
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
