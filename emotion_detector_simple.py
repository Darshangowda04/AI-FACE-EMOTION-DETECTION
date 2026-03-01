"""
Simplified Emotion Detector - OpenCV Only Version
Uses basic face detection without DeepFace dependency
"""

import cv2
import numpy as np
import time
from typing import Dict, Tuple, Optional


class SimplifiedEmotionDetector:
    """Simplified emotion detector using OpenCV cascade classifiers"""
    
    # Emotion color mapping (BGR format)
    EMOTION_COLORS = {
        "neutral": (200, 200, 200),     # Gray
        "happy": (0, 255, 0),           # Green
        "calm": (100, 200, 255),        # Light blue
        "intense": (0, 0, 255),         # Red
        "focus": (200, 100, 0),         # Blue-green
    }
    
    ALL_EMOTIONS = list(EMOTION_COLORS.keys())
    
    def __init__(self, analysis_interval: float = 0.5, enable_detection: bool = True):
        """Initialize detector"""
        self.analysis_interval = analysis_interval
        self.enforce_detection = enable_detection
        self.last_analysis_time = 0
        
        # Load cascade classifiers
        cascade_path = cv2.data.haarcascades
        self.face_cascade = cv2.CascadeClassifier(
            cascade_path + 'haarcascade_frontalface_default.xml'
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cascade_path + 'haarcascade_eye.xml'
        )
        self.smile_cascade = cv2.CascadeClassifier(
            cascade_path + 'haarcascade_smile.xml'
        )
        
        # Current emotion state
        self.current_emotions: Dict[str, float] = {e: 0.0 for e in self.ALL_EMOTIONS}
        self.dominant_emotion: str = "neutral"
        self.dominant_confidence: float = 0.0
        self.faces_detected: int = 0
        
        # Frame processing
        self.frame_count = 0
        self.fps = 0
        self.last_fps_time = time.time()
    
    def detect_face_features(self, frame: np.ndarray) -> Dict:
        """Detect faces and facial features"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        self.faces_detected = len(faces)
        
        features = {
            "faces": faces,
            "eyes": [],
            "smiles": [],
            "mouth_opening": []
        }
        
        # For each face, detect eyes and smile
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            # Detect eyes
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            features["eyes"].append(len(eyes))
            
            # Detect smile
            smiles = self.smile_cascade.detectMultiScale(roi_gray)
            features["smiles"].append(len(smiles))
            
            # Estimate mouth opening (simple approach: check brightness)
            lower_face = roi_gray[h//2:, :]
            avg_brightness = np.mean(lower_face)
            features["mouth_opening"].append(avg_brightness)
        
        return features
    
    def analyze_emotions_from_features(self, features: Dict) -> None:
        """Analyze emotions based on detected features"""
        
        if self.faces_detected == 0:
            # No face detected - neutral
            self.current_emotions = {e: 0.0 for e in self.ALL_EMOTIONS}
            self.current_emotions["neutral"] = 100.0
            self.dominant_emotion = "neutral"
            self.dominant_confidence = 100
            return
        
        # Initialize emotions
        emotions = {e: 20.0 for e in self.ALL_EMOTIONS}  # Base level
        
        # Analyze features
        has_eyes = sum(features["eyes"]) > 0
        has_smiles = sum(features["smiles"]) > 0
        avg_mouth_brightness = np.mean(features["mouth_opening"]) if features["mouth_opening"] else 128
        
        # Simple emotion logic
        if has_smiles and has_eyes:
            # Smiling with visible eyes = HAPPY
            emotions["happy"] = 80.0
            emotions["neutral"] = 20.0
            emotions["calm"] = 10.0
            emotions["intense"] = 5.0
            emotions["focus"] = 10.0
        elif has_eyes and avg_mouth_brightness < 100:
            # Eyes open, dark mouth = FOCUS
            emotions["focus"] = 70.0
            emotions["intense"] = 20.0
            emotions["neutral"] = 20.0
            emotions["calm"] = 10.0
            emotions["happy"] = 10.0
        elif avg_mouth_brightness > 150:
            # Bright mouth area = possibly open mouth = surprise/intense
            emotions["intense"] = 60.0
            emotions["focus"] = 20.0
            emotions["neutral"] = 20.0
            emotions["calm"] = 10.0
            emotions["happy"] = 10.0
        else:
            # Default = calm/neutral
            emotions["calm"] = 50.0
            emotions["neutral"] = 30.0
            emotions["focus"] = 15.0
            emotions["happy"] = 5.0
            emotions["intense"] = 5.0
        
        # Normalize to percentages
        total = sum(emotions.values())
        self.current_emotions = {e: (emotions[e] / total) * 100 for e in self.ALL_EMOTIONS}
        
        # Find dominant
        self.dominant_emotion = max(self.ALL_EMOTIONS, 
                                   key=lambda e: self.current_emotions[e])
        self.dominant_confidence = int(self.current_emotions[self.dominant_emotion])
    
    def analyze_frame(self, frame: np.ndarray) -> Dict:
        """Analyze a single frame"""
        current_time = time.time()
        
        # Check if enough time passed
        if current_time - self.last_analysis_time < self.analysis_interval:
            return {
                "emotions": self.current_emotions.copy(),
                "dominant_emotion": self.dominant_emotion,
                "dominant_confidence": self.dominant_confidence,
                "faces_detected": self.faces_detected,
                "analyzed": False
            }
        
        try:
            # Detect features
            features = self.detect_face_features(frame)
            
            # Analyze emotions
            self.analyze_emotions_from_features(features)
            
            self.last_analysis_time = current_time
            
            return {
                "emotions": self.current_emotions.copy(),
                "dominant_emotion": self.dominant_emotion,
                "dominant_confidence": self.dominant_confidence,
                "faces_detected": self.faces_detected,
                "analyzed": True
            }
        
        except Exception as e:
            return {
                "emotions": self.current_emotions.copy(),
                "dominant_emotion": self.dominant_emotion,
                "dominant_confidence": self.dominant_confidence,
                "faces_detected": 0,
                "analyzed": False,
                "error": str(e)
            }
    
    def get_emotion_color(self, emotion: str) -> Tuple[int, int, int]:
        """Get BGR color for emotion"""
        return self.EMOTION_COLORS.get(emotion, (200, 200, 200))
    
    def get_dominant_color(self) -> Tuple[int, int, int]:
        """Get color for dominant emotion"""
        return self.get_emotion_color(self.dominant_emotion)
    
    def update_fps(self):
        """Update FPS counter"""
        self.frame_count += 1
        current_time = time.time()
        
        if current_time - self.last_fps_time >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.last_fps_time = current_time
    
    def get_stats(self) -> Dict:
        """Get current statistics"""
        from datetime import datetime
        return {
            "timestamp": datetime.now().isoformat(),
            "dominant_emotion": self.dominant_emotion,
            "confidence": self.dominant_confidence,
            "all_emotions": self.current_emotions.copy(),
            "faces_detected": self.faces_detected,
            "fps": self.fps
        }
