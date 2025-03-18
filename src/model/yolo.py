from ultralytics import YOLO
import cv2
import numpy as np
import os
import requests

class WasteDetector:
    def __init__(self, model_path='best.pt'):
        try:
            # Nếu model_path là URL, tải về
            if model_path.startswith('http'):
                print("Downloading model...")
                response = requests.get(model_path)
                model_path = 'best.pt'
                with open(model_path, 'wb') as f:
                    f.write(response.content)
                print("Model downloaded successfully!")

            self.model = YOLO(model_path)
            self.class_names = {
                0: 'Bottle',
                1: 'Paper',
                2: 'Cardboard',
                3: 'Detergent',
                4: 'Can/Canister',
                5: 'Glass'
            }
        except Exception as e:
            raise RuntimeError(f"Failed to load YOLO model: {str(e)}")
        
    def detect_objects(self, frame):
        # Perform detection
        results = self.model(frame)
        
        # Process results
        detected_objects = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = box.xyxy[0]
                # Get confidence
                confidence = box.conf[0]
                # Get class
                class_id = int(box.cls[0])
                
                detected_objects.append({
                    'box': [int(x1), int(y1), int(x2-x1), int(y2-y1)],
                    'confidence': float(confidence),
                    'class_id': class_id
                })
                
        return detected_objects

    def draw_detections(self, frame, detections):
        for det in detections:
            x, y, w, h = det['box']
            conf = det['confidence']
            class_id = det['class_id']
            
            # Lấy tên lớp
            class_name = self.class_names.get(class_id, 'Unknown')
            
            # Vẽ rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Vẽ label với tên lớp và độ chính xác
            label = f"{class_name} {conf:.2f}"
            
            # Tạo background cho text
            (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(frame, (x, y - 20), (x + label_w, y), (0, 255, 0), -1)
            
            # Vẽ text
            cv2.putText(frame, label, (x, y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
        return frame