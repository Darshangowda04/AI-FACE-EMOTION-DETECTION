"""
Core Emotion Detection Module
Real-time face expression recognition with DeepFace
"""

import cv2
import numpy as np
from deepface import DeepFace
import time
from datetime import datetime
from typing import Dict, Tuple, Optional, List
import threading
import json


class EmotionDetector:
    """Main emotion detection class for real-time face expression recognition"""
    
    # Emotion color mapping (BGR format)
    EMOTION_COLORS = {
        "angry": (0, 0, 255),           # Red
        "disgust": (0, 165, 255),       # Orange
        "fear": (128, 0, 128),          # Purple
        "happy": (0, 255, 0),           # Green
        "neutral": (200, 200, 200),     # Gray
        "sad": (255, 0, 0),             # Blue
        "surprise": (0, 255, 255)       # Yellow
    }
    
    ALL_EMOTIONS = list(EMOTION_COLORS.keys())
    
    def __init__(self, analysis_interval: float = 0.5, enable_detection: bool = True):
        """
        Initialize emotion detector
        
        Args:
            analysis_interval: Seconds between emotion analysis (for performance)
            enable_detection: Whether to enforce face detection
        """
        self.analysis_interval = analysis_interval
        self.enforce_detection = enable_detection
        self.last_analysis_time = 0
        
        # Current emotion state
        self.current_emotions: Dict[str, float] = {e: 0.0 for e in self.ALL_EMOTIONS}
        self.dominant_emotion: str = "neutral"
        self.dominant_confidence: float = 0.0
        self.faces_detected: int = 0
        
        # Frame processing
        self.frame_count = 0
        self.fps = 0
        self.last_fps_time = time.time()
        
    def analyze_frame(self, frame: np.ndarray) -> Dict:
        """
        Analyze a single frame for emotions
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Dictionary with emotion analysis results
        """
        current_time = time.time()
        
        # Check if enough time has passed since last analysis
        if current_time - self.last_analysis_time < self.analysis_interval:
            return {
                "emotions": self.current_emotions,
                "dominant_emotion": self.dominant_emotion,
                "dominant_confidence": self.dominant_confidence,
                "faces_detected": self.faces_detected,
                "analyzed": False
            }
        
        try:
            # Detect faces and analyze emotions
            results = DeepFace.analyze(
                frame,
                actions=["emotion"],
                enforce_detection=self.enforce_detection,
                silent=True
            )
            
            self.faces_detected = len(results)
            
            if results:
                # Aggregate emotions from all detected faces
                aggregated_emotions = {e: 0.0 for e in self.ALL_EMOTIONS}
                
                for result in results:
                    if "emotion" in result:
                        for emotion, score in result["emotion"].items():
                            if emotion in aggregated_emotions:
                                aggregated_emotions[emotion] += score
                
                # Average across faces
                if self.faces_detected > 0:
                    for emotion in aggregated_emotions:
                        aggregated_emotions[emotion] /= self.faces_detected
                
                self.current_emotions = aggregated_emotions
                
                # Find dominant emotion
                self.dominant_emotion = max(self.ALL_EMOTIONS, 
                                           key=lambda e: self.current_emotions[e])
                self.dominant_confidence = int(self.current_emotions[self.dominant_emotion])
            
            self.last_analysis_time = current_time
            
            return {
                "emotions": self.current_emotions.copy(),
                "dominant_emotion": self.dominant_emotion,
                "dominant_confidence": self.dominant_confidence,
                "faces_detected": self.faces_detected,
                "analyzed": True
            }
            
        except Exception as e:
            # If analysis fails, return cached values
            return {
                "emotions": self.current_emotions.copy(),
                "dominant_emotion": self.dominant_emotion,
                "dominant_confidence": self.dominant_confidence,
                "faces_detected": 0,
                "analyzed": False,
                "error": str(e)
            }
    
    def get_emotion_color(self, emotion: str) -> Tuple[int, int, int]:
        """Get BGR color for specific emotion"""
        return self.EMOTION_COLORS.get(emotion, (200, 200, 200))
    
    def get_dominant_color(self) -> Tuple[int, int, int]:
        """Get BGR color for dominant emotion"""
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
        """Get current emotion statistics"""
        return {
            "timestamp": datetime.now().isoformat(),
            "dominant_emotion": self.dominant_emotion,
            "confidence": self.dominant_confidence,
            "all_emotions": self.current_emotions.copy(),
            "faces_detected": self.faces_detected,
            "fps": self.fps
        }
