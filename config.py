"""
Configuration file for Emotion Detection System
Customize colors, emotions, and detection parameters here
"""

import json

# Default Configuration
CONFIG = {
    "camera": {
        "device_id": 0,
        "width": 1280,
        "height": 720,
        "fps": 30
    },
    "detection": {
        "analysis_interval": 0.5,  # Seconds between analysis
        "enforce_detection": True,  # Require face detection
        "minimum_confidence": 0.5  # Minimum confidence threshold
    },
    "visualization": {
        "show_header": True,
        "show_emotion_box": True,
        "show_bars": True,
        "show_stats": True,
        "font_scale": 1.0,
        "box_thickness": 3
    },
    "emotions": {
        "enabled": [
            "angry",
            "disgust",
            "fear",
            "happy",
            "neutral",
            "sad",
            "surprise"
        ],
        "colors": {
            "angry": [0, 0, 255],        # Red (BGR)
            "disgust": [0, 165, 255],    # Orange
            "fear": [128, 0, 128],       # Purple
            "happy": [0, 255, 0],        # Green
            "neutral": [200, 200, 200],  # Gray
            "sad": [255, 0, 0],          # Blue
            "surprise": [0, 255, 255]    # Yellow
        }
    },
    "api": {
        "host": "0.0.0.0",
        "port": 5000,
        "debug": False,
        "max_connections": 10
    },
    "logging": {
        "enabled": False,
        "log_file": "emotion_detection.log",
        "save_statistics": False,
        "stats_file": "emotion_stats.json"
    }
}


def load_config(filepath: str = None) -> dict:
    """
    Load configuration from JSON file
    
    Args:
        filepath: Path to config JSON file
        
    Returns:
        Configuration dictionary
    """
    if filepath:
        try:
            with open(filepath, 'r') as f:
                user_config = json.load(f)
                # Merge with defaults
                CONFIG.update(user_config)
        except FileNotFoundError:
            print(f"Config file not found: {filepath}")
    
    return CONFIG


def save_config(filepath: str = "config.json"):
    """Save current configuration to file"""
    with open(filepath, 'w') as f:
        json.dump(CONFIG, f, indent=4)
    print(f"Configuration saved to {filepath}")


if __name__ == "__main__":
    # Save default config
    save_config()
    print("Default configuration saved to config.json")
