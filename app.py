import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import subprocess
import imageio_ffmpeg
from ultralytics import YOLO

# Page configuration
st.set_page_config(page_title="YOLOv5 Self-Driving Object Detection", page_icon="🚗", layout="wide")

# Load YOLO model
@st.cache_resource
def load_model():
    return YOLO('yolov5s.pt')

model = load_model()

# Custom CSS for aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff6b6b;
    }
    h1 {
        color: #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 YOLOv5 Self-Driving Object Detection")
st.markdown("Upload an image or video to detect objects using the YOLOv5 model. Perfect for self-driving vehicle perception!")

st.sidebar.header("Settings")
confidence = st.sidebar.slider("Confidence Threshold", min_value=0.0, max_value=1.0, value=0.25, step=0.05)

uploaded_file = st.file_uploader("Choose an image or video...", type=["jpg", "jpeg", "png", "mp4"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()
    
    if file_type in ["jpg", "jpeg", "png"]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(uploaded_file, use_container_width=True)
            
        if st.button("Detect Objects 🚀"):
            with st.spinner("Detecting..."):
                # Read image
                file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, 1)
                
                # Inference
                results = model(img, conf=confidence)
                
                # Plot results
                res_plotted = results[0].plot()
                # Convert BGR to RGB for Streamlit
                res_plotted_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
                
                with col2:
                    st.subheader("Detected Objects")
                    st.image(res_plotted_rgb, use_container_width=True)
                
    elif file_type == "mp4":
        st.video(uploaded_file)
        
        if st.button("Detect Objects 🚀"):
            with st.spinner("Processing video... This may take a while."):
                # Save uploaded video to temp file
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") 
                tfile.write(uploaded_file.read())
                
                # Process video
                cap = cv2.VideoCapture(tfile.name)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                if fps == 0: fps = 30
                
                out_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
                out = cv2.VideoWriter(out_file.name, fourcc, fps, (width, height))
                
                # Setup progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                if total_frames == 0 or total_frames > 300: 
                    total_frames = 150 # limit to avoid hanging the cloud app
                
                frame_count = 0
                while cap.isOpened() and frame_count < total_frames:
                    ret, frame = cap.read()
                    if not ret:
                        break
                        
                    results = model(frame, conf=confidence)
                    output_frame = results[0].plot()
                    out.write(output_frame)
                    
                    frame_count += 1
                    # Update progress
                    progress_bar.progress(frame_count / total_frames)
                    status_text.text(f"Processed {frame_count}/{total_frames} frames")
                        
                cap.release()
                out.release()
                
                # Transcode the mp4v video to h264 for web browser compatibility
                status_text.text("Finalizing video for web playback...")
                final_out_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                
                try:
                    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                    subprocess.run([
                        ffmpeg_exe, "-y", "-i", out_file.name, 
                        "-vcodec", "libx264", "-f", "mp4", final_out_file.name
                    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    st.success("Video processing complete!")
                    st.video(final_out_file.name)
                except Exception as e:
                    st.error(f"Error during video encoding: {e}")
