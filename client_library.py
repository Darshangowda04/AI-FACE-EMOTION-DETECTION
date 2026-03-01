"""
Emotion Detection Client Library
Use this module to integrate emotion detection into your own applications
"""

import cv2
import numpy as np
from emotion_detector import EmotionDetector
from visualizer import EmotionVisualizer
from typing import Dict, Tuple, Optional
import requests
import json


class EmotionDetectionClient:
    """
    Client for using emotion detection in your own applications
    
    Example Usage:
    ```
    # Direct usage (local)
    client = EmotionDetectionClient(mode='local')
    
    # Or use remote API
    client = EmotionDetectionClient(mode='remote', api_url='http://localhost:5000')
    
    # Analyze frame
    result = client.detect_emotion(frame)
    ```
    """
    
    def __init__(self, mode: str = 'local', api_url: str = 'http://localhost:5000'):
        """
        Initialize client
        
        Args:
            mode: 'local' or 'remote'
            api_url: API endpoint for remote mode
        """
        self.mode = mode
        self.api_url = api_url
        
        if mode == 'local':
            self.detector = EmotionDetector()
            self.visualizer = EmotionVisualizer(self.detector.EMOTION_COLORS)
        else:
            self._check_api_health()
    
    def _check_api_health(self) -> bool:
        """Check if remote API is available"""
        try:
            response = requests.get(f"{self.api_url}/api/health", timeout=2)
            return response.status_code == 200
        except:
            raise ConnectionError(f"Cannot connect to API at {self.api_url}")
    
    def detect_emotion(self, frame: np.ndarray) -> Dict:
        """
        Detect emotion in a frame
        
        Args:
            frame: Input image (BGR format)
            
        Returns:
            Dictionary with emotion detection results
        """
        if self.mode == 'local':
            return self.detector.analyze_frame(frame)
        else:
            # Upload to API
            _, buffer = cv2.imencode('.jpg', frame)
            files = {'image': buffer.tobytes()}
            
            try:
                response = requests.post(
                    f"{self.api_url}/api/analyze",
                    files={'image': buffer.tobytes()},
                    timeout=5
                )
                
                if response.status_code == 200:
                    return response.json()['analysis']
                else:
                    return {"error": "API error"}
            except Exception as e:
                return {"error": str(e)}
    
    def get_current_emotion(self) -> Dict:
        """Get current emotion from API"""
        if self.mode == 'local':
            return {
                "emotion": self.detector.dominant_emotion,
                "confidence": self.detector.dominant_confidence,
                "all_emotions": self.detector.current_emotions
            }
        else:
            try:
                response = requests.get(f"{self.api_url}/api/emotion", timeout=2)
                return response.json()
            except Exception as e:
                return {"error": str(e)}
    
    def visualize_frame(self, frame: np.ndarray) -> np.ndarray:
        """Add emotion visualization to frame"""
        if self.mode == 'local':
            return self.visualizer.render_complete_hud(
                frame,
                emotion=self.detector.dominant_emotion,
                confidence=self.detector.dominant_confidence,
                all_emotions=self.detector.current_emotions,
                emotion_colors=self.detector.EMOTION_COLORS,
                faces_detected=self.detector.faces_detected,
                fps=self.detector.fps
            )
        return frame
    
    def start_stream(self) -> bool:
        """Start remote streaming"""
        if self.mode == 'remote':
            try:
                response = requests.post(
                    f"{self.api_url}/api/stream/start",
                    json={"camera_id": 0},
                    timeout=5
                )
                return response.status_code == 200
            except Exception as e:
                print(f"Error starting stream: {e}")
                return False
        return True
    
    def stop_stream(self) -> bool:
        """Stop remote streaming"""
        if self.mode == 'remote':
            try:
                response = requests.post(f"{self.api_url}/api/stream/stop", timeout=5)
                return response.status_code == 200
            except Exception as e:
                print(f"Error stopping stream: {e}")
                return False
        return True


class EmotionCallback:
    """
    Base class for custom emotion detection callbacks
    
    Example:
    ```
    class MyCallback(EmotionCallback):
        def on_emotion_change(self, emotion, confidence):
            print(f"Emotion: {emotion} ({confidence}%)")
    
    callback = MyCallback()
    processor.add_callback(callback)
    ```
    """
    
    def on_emotion_detected(self, emotion: str, confidence: int, 
                           all_emotions: Dict[str, float]):
        """Called when emotion is detected"""
        pass
    
    def on_emotion_change(self, emotion: str, confidence: int):
        """Called when dominant emotion changes"""
        pass
    
    def on_no_face_detected(self):
        """Called when no faces are detected"""
        pass


class EmotionProcessor:
    """
    Stream processor with emotion callbacks
    
    Example:
    ```
    processor = EmotionProcessor(camera_id=0)
    processor.add_callback(MyCallback())
    processor.run()
    ```
    """
    
    def __init__(self, camera_id: int = 0, analysis_interval: float = 0.5):
        """Initialize processor"""
        self.detector = EmotionDetector(analysis_interval=analysis_interval)
        self.visualizer = EmotionVisualizer(self.detector.EMOTION_COLORS)
        self.cap = cv2.VideoCapture(camera_id)
        self.callbacks: list = []
        self.last_emotion = None
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera {camera_id}")
    
    def add_callback(self, callback: EmotionCallback):
        """Add emotion detection callback"""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback: EmotionCallback):
        """Remove callback"""
        self.callbacks.remove(callback)
    
    def _trigger_callbacks(self, emotion: str, confidence: int, 
                          all_emotions: Dict[str, float]):
        """Trigger all registered callbacks"""
        for callback in self.callbacks:
            callback.on_emotion_detected(emotion, confidence, all_emotions)
            
            if emotion != self.last_emotion:
                callback.on_emotion_change(emotion, confidence)
                self.last_emotion = emotion
    
    def run(self, show_display: bool = True):
        """
        Run emotion processor
        
        Args:
            show_display: Show visualization window
        """
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                
                # Analyze
                result = self.detector.analyze_frame(frame)
                self.detector.update_fps()
                
                # Trigger callbacks
                if result.get('analyzed'):
                    self._trigger_callbacks(
                        self.detector.dominant_emotion,
                        self.detector.dominant_confidence,
                        self.detector.current_emotions
                    )
                
                # Display
                if show_display:
                    frame = self.visualizer.render_complete_hud(
                        frame,
                        emotion=self.detector.dominant_emotion,
                        confidence=self.detector.dominant_confidence,
                        all_emotions=self.detector.current_emotions,
                        emotion_colors=self.detector.EMOTION_COLORS,
                        faces_detected=self.detector.faces_detected,
                        fps=self.detector.fps
                    )
                    
                    cv2.imshow("Emotion Detection", frame)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()


# Helper functions

def detect_emotion_in_image(image_path: str) -> Dict:
    """
    Detect emotion in an image file
    
    Args:
        image_path: Path to image file
        
    Returns:
        Emotion detection results
    """
    frame = cv2.imread(image_path)
    if frame is None:
        return {"error": f"Failed to load image: {image_path}"}
    
    detector = EmotionDetector()
    return detector.analyze_frame(frame)


def get_emotion_percentage(all_emotions: Dict[str, float], emotion: str) -> float:
    """Get percentage for specific emotion"""
    return all_emotions.get(emotion, 0.0)


def get_sorted_emotions(all_emotions: Dict[str, float]) -> list:
    """Get emotions sorted by confidence (highest first)"""
    return sorted(all_emotions.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    # Example: Use emotion detection in your app
    
    class MyCallback(EmotionCallback):
        def on_emotion_detected(self, emotion, confidence, all_emotions):
            print(f"[DETECTED] {emotion}: {confidence}%")
        
        def on_emotion_change(self, emotion, confidence):
            print(f"[CHANGED] Dominant emotion: {emotion} ({confidence}%)")
    
    # Create processor
    processor = EmotionProcessor(camera_id=0)
    processor.add_callback(MyCallback())
    
    # Run
    print("Starting emotion processing...")
    processor.run(show_display=True)
