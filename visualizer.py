"""
Visualization and UI Module
Handles all visual rendering with color-coded emotions
"""

import cv2
import numpy as np
from typing import Tuple, Optional


class EmotionVisualizer:
    """Handles all visualization and rendering of emotion data"""
    
    # UI Constants
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_THICK = cv2.FONT_HERSHEY_DUPLEX
    
    def __init__(self, emotion_colors: dict):
        """
        Initialize visualizer
        
        Args:
            emotion_colors: Dictionary mapping emotions to BGR colors
        """
        self.emotion_colors = emotion_colors
        self.emotions_list = list(emotion_colors.keys())
    
    def draw_header(self, frame: np.ndarray, title: str = "AI EMOTION DETECTOR") -> np.ndarray:
        """Draw top header bar"""
        h, w = frame.shape[:2]
        
        # Header background
        cv2.rectangle(frame, (0, 0), (w, 50), (20, 20, 20), -1)
        cv2.rectangle(frame, (0, 0), (w, 50), (100, 100, 100), 2)
        
        # Title text
        cv2.putText(frame, title, (15, 35),
                   self.FONT_THICK, 1.2, (0, 255, 255), 2)
        
        return frame
    
    def draw_main_emotion_box(self, frame: np.ndarray, 
                             emotion: str, confidence: int,
                             color: Tuple[int, int, int]) -> np.ndarray:
        """Draw central emotion display box"""
        h, w = frame.shape[:2]
        
        box_w, box_h = 300, 120
        x = w // 2 - box_w // 2
        y = h // 2 - box_h // 2
        
        # Outer glow effect
        cv2.rectangle(frame, (x - 4, y - 4), (x + box_w + 4, y + box_h + 4),
                     color, 3)
        
        # Inner box
        cv2.rectangle(frame, (x, y), (x + box_w, y + box_h),
                     (30, 30, 30), -1)
        cv2.rectangle(frame, (x, y), (x + box_w, y + box_h),
                     color, 3)
        
        # Emotion label background
        cv2.rectangle(frame, (x, y - 40), (x + box_w, y),
                     color, -1)
        
        # Emotion text
        label = f"{emotion.upper()}"
        text_size = cv2.getTextSize(label, self.FONT_THICK, 1.5, 2)[0]
        text_x = x + (box_w - text_size[0]) // 2
        cv2.putText(frame, label, (text_x, y - 10),
                   self.FONT_THICK, 1.5, (255, 255, 255), 2)
        
        # Confidence percentage
        conf_text = f"{confidence}%"
        conf_size = cv2.getTextSize(conf_text, self.FONT_THICK, 2, 3)[0]
        conf_x = x + (box_w - conf_size[0]) // 2
        cv2.putText(frame, conf_text, (conf_x, y + box_h // 2 + 20),
                   self.FONT_THICK, 2, color, 3)
        
        return frame
    
    def draw_emotion_bars(self, frame: np.ndarray, 
                         emotions: dict, dominant: str) -> np.ndarray:
        """Draw emotion percentage bars on the side"""
        h, w = frame.shape[:2]
        
        panel_x = 20
        panel_y = 70
        line_height = 32
        bar_width = 220
        bar_height = 20
        
        # Title
        cv2.putText(frame, "EMOTION ANALYSIS", (panel_x, panel_y - 10),
                   self.FONT, 0.8, (255, 255, 255), 2)
        
        # Draw bars for each emotion
        for i, emotion in enumerate(self.emotions_list):
            y_pos = panel_y + (i * line_height)
            score = emotions.get(emotion, 0.0)
            bar_fill = int((score / 100.0) * bar_width)
            
            # Emotion name
            color = self.emotion_colors[emotion]
            cv2.putText(frame, f"{emotion.upper():10s}", (panel_x, y_pos + 18),
                       self.FONT, 0.7, color, 2)
            
            # Bar background
            cv2.rectangle(frame, (panel_x + 140, y_pos),
                         (panel_x + 140 + bar_width, y_pos + bar_height),
                         (50, 50, 50), -1)
            
            # Bar border
            cv2.rectangle(frame, (panel_x + 140, y_pos),
                         (panel_x + 140 + bar_width, y_pos + bar_height),
                         color if emotion == dominant else (100, 100, 100), 1)
            
            # Bar fill
            bar_color = color if emotion == dominant else (100, 150, 150)
            thickness = -1 if emotion == dominant else 2
            cv2.rectangle(frame, (panel_x + 140, y_pos),
                         (panel_x + 140 + bar_fill, y_pos + bar_height),
                         bar_color, thickness)
            
            # Percentage text
            pct_text = f"{int(score)}%"
            cv2.putText(frame, pct_text, (panel_x + 140 + bar_width + 10, y_pos + 16),
                       self.FONT, 0.6, (200, 200, 200), 1)
        
        return frame
    
    def draw_stats_panel(self, frame: np.ndarray, 
                        faces_detected: int, fps: int) -> np.ndarray:
        """Draw statistics panel"""
        h, w = frame.shape[:2]
        
        panel_y = h - 50
        
        # Background
        cv2.rectangle(frame, (0, panel_y), (w, h), (20, 20, 20), -1)
        cv2.rectangle(frame, (0, panel_y), (w, h), (100, 100, 100), 1)
        
        # Stats text
        stats_text = f"FACES: {faces_detected}  |  FPS: {fps}  |  Press 'Q' to quit"
        cv2.putText(frame, stats_text, (20, h - 15),
                   self.FONT, 0.7, (0, 255, 255), 1)
        
        return frame
    
    def draw_face_detection_boxes(self, frame: np.ndarray, 
                                 face_locations: list) -> np.ndarray:
        """Draw bounding boxes around detected faces"""
        for (x, y, w, h) in face_locations:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Small label
            cv2.putText(frame, "FACE", (x + 5, y - 5),
                       self.FONT, 0.5, (0, 255, 0), 1)
        
        return frame
    
    def render_complete_hud(self, frame: np.ndarray,
                           emotion: str,
                           confidence: int,
                           all_emotions: dict,
                           emotion_colors: dict,
                           faces_detected: int,
                           fps: int) -> np.ndarray:
        """
        Render complete HUD with all visualizations
        
        Args:
            frame: Input frame
            emotion: Dominant emotion
            confidence: Confidence percentage
            all_emotions: Dictionary of all emotion scores
            emotion_colors: Color mapping
            faces_detected: Number of faces detected
            fps: Current FPS
            
        Returns:
            Annotated frame
        """
        color = emotion_colors.get(emotion, (200, 200, 200))
        
        # Draw components
        frame = self.draw_header(frame)
        frame = self.draw_main_emotion_box(frame, emotion, confidence, color)
        frame = self.draw_emotion_bars(frame, all_emotions, emotion)
        frame = self.draw_stats_panel(frame, faces_detected, fps)
        
        return frame
