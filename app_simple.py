"""
Real-time Face Emotion Detection Application - Simplified Version
Main entry point that doesn't require DeepFace
"""

import cv2
import sys
import argparse
from emotion_detector_simple import SimplifiedEmotionDetector
from visualizer import EmotionVisualizer
import json
import os


class EmotionDetectionApp:
    """Main application for real-time emotion detection"""
    
    def __init__(self, camera_id: int = 0, analysis_interval: float = 0.5,
                 save_logs: bool = False):
        """Initialize the application"""
        self.detector = SimplifiedEmotionDetector(
            analysis_interval=analysis_interval,
            enable_detection=True
        )
        self.visualizer = EmotionVisualizer(self.detector.EMOTION_COLORS)
        
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera {camera_id}")
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.save_logs = save_logs
        self.emotion_history = []
    
    def process_frame(self, frame):
        """Process a single frame"""
        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        
        # Analyze emotions
        result = self.detector.analyze_frame(frame)
        
        # Update FPS
        self.detector.update_fps()
        
        # Save emotion data if enabled
        if self.save_logs and result.get("analyzed"):
            self.emotion_history.append(self.detector.get_stats())
        
        # Render visualization
        frame = self.visualizer.render_complete_hud(
            frame,
            emotion=self.detector.dominant_emotion,
            confidence=self.detector.dominant_confidence,
            all_emotions=self.detector.current_emotions,
            emotion_colors=self.detector.EMOTION_COLORS,
            faces_detected=self.detector.faces_detected,
            fps=self.detector.fps
        )
        
        return frame
    
    def run(self):
        """Main application loop"""
        print("=" * 60)
        print("AI FACE EMOTION DETECTION - Real-time (Simplified)")
        print("=" * 60)
        print("Press 'Q' to quit")
        print("Press 'S' to save current statistics")
        print("=" * 60)
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Failed to read frame from camera")
                    break
                
                # Process frame
                frame = self.process_frame(frame)
                
                # Display
                cv2.imshow("AI Face Emotion Detection", frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    print("\nQuitting application...")
                    break
                
                elif key == ord('s') or key == ord('S'):
                    self.save_statistics()
        
        finally:
            self.cleanup()
    
    def save_statistics(self):
        """Save emotion statistics to file"""
        if not self.emotion_history:
            print("No data to save")
            return
        
        filename = "emotion_stats.json"
        with open(filename, 'w') as f:
            json.dump(self.emotion_history, f, indent=2)
        
        print(f"Statistics saved to {filename}")
    
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        
        if self.save_logs and self.emotion_history:
            self.save_statistics()
        
        print("Application closed")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Real-time AI Face Emotion Detection (Simplified)"
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Camera device ID (default: 0)"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.5,
        help="Analysis interval in seconds (default: 0.5)"
    )
    parser.add_argument(
        "--save-logs",
        action="store_true",
        help="Save emotion data to file"
    )
    
    args = parser.parse_args()
    
    try:
        app = EmotionDetectionApp(
            camera_id=args.camera,
            analysis_interval=args.interval,
            save_logs=args.save_logs
        )
        app.run()
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
