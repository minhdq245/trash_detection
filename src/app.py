from flask import Flask, render_template, Response, request, jsonify
import cv2
import time
from src.model.yolo import WasteDetector  # Update import path
import numpy as np
import os
import base64

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static')

# Ưu tiên sử dụng MODEL_URL từ environment variable
model_path = os.environ.get('MODEL_URL', 'https://drive.google.com/file/d/1b4E85lAa3_NVCXkre5Mty-0Z7DUaAmjl/view?usp=sharing')
if not model_path:
    model_path = os.path.join(os.path.dirname(__file__), 'model', 'best.pt')
    
try:
    print("Initializing model from:", model_path)
    detector = WasteDetector(model_path)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    raise RuntimeError(f"Failed to load model: {str(e)}")

@app.after_request
def add_security_headers(response):
    response.headers['Permissions-Policy'] = 'camera=self'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    return response

def get_camera():
    max_retries = 3
    for attempt in range(max_retries):
        for camera_id in range(2):
            try:
                camera = cv2.VideoCapture(camera_id)
                if camera.isOpened():
                    # Test read a frame
                    ret, frame = camera.read()
                    if ret:
                        return camera
                camera.release()
            except Exception as e:
                print(f"Camera {camera_id} attempt {attempt + 1} failed: {str(e)}")
                if camera:
                    camera.release()
        time.sleep(1)  # Wait before retry
    raise RuntimeError("Could not start camera after multiple attempts")

def generate_frames():
    camera = None
    while True:
        try:
            if camera is None:
                camera = get_camera()
            
            success, frame = camera.read()
            if not success:
                raise RuntimeError("Failed to read frame")
            
            detections = detector.detect_objects(frame)
            frame = detector.draw_detections(frame, detections)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                raise RuntimeError("Failed to encode frame")
                
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
                   
        except Exception as e:
            print(f"Stream error: {str(e)}")
            if camera:
                camera.release()
                camera = None
            time.sleep(1)  # Wait before reconnecting
            continue

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    try:
        return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Camera error: {str(e)}")
        return "Camera error", 500

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.json
        # Decode base64 image
        img_data = data['image'].split(',')[1]
        img_bytes = base64.b64decode(img_data)
        img_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        
        # Detect objects
        detections = detector.detect_objects(img)
        
        return jsonify({
            'status': 'success',
            'detections': detections
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)