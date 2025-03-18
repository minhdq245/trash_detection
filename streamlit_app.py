import streamlit as st
from src.model.yolo import WasteDetector  # Update import path
import cv2
import os
from dotenv import load_dotenv

# Cấu hình page
st.set_page_config(
    page_title="Real-time Waste Detection",
    page_icon="♻️",
    layout="wide"
)

@st.cache_resource
def load_model():
    try:
        model_path = os.getenv('MODEL_URL', 'https://drive.google.com/file/d/1b4E85lAa3_NVCXkre5Mty-0Z7DUaAmjl/view?usp=sharing')
        print("Loading model from:", model_path)
        detector = WasteDetector(model_path)
        return detector
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def main():
    st.title("♻️ Real-time Waste Detection")
    st.write("This application detects and classifies waste items in real-time using your camera.")
    
    # Initialize model
    detector = load_model()
    if not detector:
        st.error("Failed to load model. Please check your internet connection and try again.")
        return

    # Camera controls
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        start = st.button('Start Camera', type='primary')
    with col2:
        stop = st.button('Stop Camera', type='secondary')
    
    # Create placeholder for video feed
    video_placeholder = st.empty()

    if start and not stop:
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("Could not access camera. Please check your camera connection.")
                return

            while cap.isOpened() and not stop:
                ret, frame = cap.read()
                if not ret:
                    st.error("Can't receive frame from camera")
                    break

                # Process frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                detections = detector.detect_objects(frame_rgb)
                processed_frame = detector.draw_detections(frame_rgb, detections)
                
                # Display frame
                video_placeholder.image(processed_frame, channels="RGB", use_column_width=True)

            cap.release()
        except Exception as e:
            st.error(f"Error accessing camera: {str(e)}")
        finally:
            if 'cap' in locals():
                cap.release()

if __name__ == "__main__":
    main()
