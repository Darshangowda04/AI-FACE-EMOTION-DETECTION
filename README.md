# AI Face Emotion Detection 🎭

A real-time, production-ready AI face emotion detection system with advanced visualization, color-coded emotions, and API integration for easy adoption in other applications.

## Features ✨

- **Real-time Face Expression Recognition** - Detects 7 different emotions
- **Color-Coded Emotions** - Each emotion has a unique color for quick visual identification
- **High Performance** - Optimized with configurable analysis intervals (0.3-1.0 seconds)
- **Beautiful HUD Interface** - Professional, modern visualization
- **Multi-face Detection** - Handles multiple faces in a single frame
- **REST API** - Easy integration with other applications
- **Emotion Statistics** - Track and save emotion data over time
- **Flexible Configuration** - Customize colors, emotions, and detection parameters

## Supported Emotions 🎨

| Emotion | Color | RGB |
|---------|-------|-----|
| Angry | Red | (0, 0, 255) |
| Disgust | Orange | (0, 165, 255) |
| Fear | Purple | (128, 0, 128) |
| Happy | Green | (0, 255, 0) |
| Neutral | Gray | (200, 200, 200) |
| Sad | Blue | (255, 0, 0) |
| Surprise | Yellow | (0, 255, 255) |

## Installation 📦

### Prerequisites
- Python 3.7+
- Webcam (for real-time detection)

### Setup

1. **Clone or create the project directory**
```bash
cd ai-face-emotion-detection
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install required packages**
```bash
pip install -r requirements.txt
```

## Usage 🚀

### 1. Real-time Emotion Detection (Desktop App)

**Basic Usage:**
```bash
python app.py
```

**With Options:**
```bash
# Specify camera ID
python app.py --camera 0

# Set analysis interval (seconds)
python app.py --interval 0.3

# Save emotion statistics to file
python app.py --save-logs
```

**In-App Keyboard Controls:**
- **Q** - Quit application
- **S** - Save current statistics to JSON file

**Output Example:**
```
============================================================
AI FACE EMOTION DETECTION - Real-time
============================================================
Press 'Q' to quit
Press 'S' to save current statistics
============================================================
```

### 2. REST API Server

**Start the API server:**
```bash
python api.py
```

The API will be available at `http://localhost:5000`

### 3. API Endpoints

#### Health Check
```bash
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-01T10:30:00.000000"
}
```

#### Get Current Emotion
```bash
GET /api/emotion
```

**Response:**
```json
{
  "dominant_emotion": "happy",
  "confidence": 85,
  "all_emotions": {
    "angry": 2.5,
    "disgust": 1.2,
    "fear": 0.8,
    "happy": 85.3,
    "neutral": 8.2,
    "sad": 1.5,
    "surprise": 0.5
  },
  "faces_detected": 1,
  "fps": 30,
  "timestamp": "2026-03-01T10:30:00.000000"
}
```

#### Start Video Stream
```bash
POST /api/stream/start
Content-Type: application/json

{
  "camera_id": 0
}
```

#### Stream Video Feed
```bash
GET /api/video
```

Streams MJPEG video with real-time emotion detection.

#### Stop Video Stream
```bash
POST /api/stream/stop
```

#### Analyze Uploaded Image
```bash
POST /api/analyze
Content-Type: multipart/form-data

[image file]
```

#### Get Configuration
```bash
GET /api/config
```

#### Update Configuration
```bash
PUT /api/config
Content-Type: application/json

{
  "analysis_interval": 0.5,
  "enforce_detection": true
}
```

## Integration with Other Apps 🔗

### Python Flask App Example

```python
import requests
import json

# Start streaming
requests.post('http://localhost:5000/api/stream/start')

# Get emotion data
response = requests.get('http://localhost:5000/api/emotion')
emotion_data = response.json()

print(f"Emotion: {emotion_data['dominant_emotion']}")
print(f"Confidence: {emotion_data['confidence']}%")

# Stop streaming
requests.post('http://localhost:5000/api/stream/stop')
```

### JavaScript/Node.js Example

```javascript
// Start streaming
await fetch('http://localhost:5000/api/stream/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ camera_id: 0 })
});

// Get emotion data
const response = await fetch('http://localhost:5000/api/emotion');
const data = await response.json();

console.log(`Emotion: ${data.dominant_emotion}`);
console.log(`Confidence: ${data.confidence}%`);

// Display video stream
const videoElement = document.getElementById('emotion-video');
videoElement.src = 'http://localhost:5000/api/video';
```

### cURL Examples

```bash
# Get current emotion
curl http://localhost:5000/api/emotion

# Start streaming
curl -X POST http://localhost:5000/api/stream/start

# Analyze image
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@path/to/image.jpg"
```

## Configuration 🔧

Edit `config.py` to customize:

- **Emotions**: Enable/disable specific emotions
- **Colors**: Change emotion color palette (BGR format)
- **Detection**: Adjust analysis intervals and confidence thresholds
- **API**: Configure host, port, and debug mode
- **Logging**: Enable emotion statistics saving

### Example Custom Configuration

```python
CONFIG = {
    "detection": {
        "analysis_interval": 0.3,  # Faster analysis
        "enforce_detection": True
    },
    "emotions": {
        "colors": {
            "happy": [0, 255, 0],     # Green
            "sad": [255, 0, 0],       # Blue
            # ... customize as needed
        }
    }
}
```

## Performance Optimization ⚡

The system uses several optimizations:

1. **Configurable Analysis Interval** - Analyze emotions every 0.3-1.0 seconds instead of every frame
2. **Frame Caching** - Reuse last analysis results between intervals
3. **Face Detection Efficiency** - Uses DeepFace's optimized detection
4. **FPS Limiting** - Runs at optimal 30 FPS

### Performance Tuning
```bash
# Slower but more accurate (analyze every 0.2 seconds)
python app.py --interval 0.2

# Faster for resource-limited systems (analyze every 1.0 seconds)
python app.py --interval 1.0
```

## File Structure 📁

```
ai-face-emotion-detection/
├── app.py                 # Main real-time application
├── emotion_detector.py    # Core emotion detection logic
├── visualizer.py          # UI and visualization
├── api.py                 # REST API server
├── config.py              # Configuration file
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Project Architecture 🏗️

### Module Overview

**emotion_detector.py** - Core detection engine
- Handles DeepFace analysis
- Manages emotion state
- Provides FPS tracking

**visualizer.py** - Visual components
- Renders HUD interface
- Color-coded emotion display
- Statistics panels

**app.py** - Standalone application
- Real-time webcam processing
- Keyboard controls
- Data logging

**api.py** - REST API server
- WebSocket video streaming
- Image upload analysis
- Configuration management

## Troubleshooting 🐛

### Camera not opening
- Check camera ID: `python app.py --camera 1`
- Verify camera permissions

### DeepFace errors
- Reinstall: `pip install --upgrade deepface`
- Check TensorFlow: `pip install --upgrade tensorflow`

### Poor emotion detection
- Ensure good lighting
- Better quality webcam
- Reduce analysis interval for more frequent updates

### API connection issues
- Check firewall settings
- Ensure port 5000 is available
- Try different host: `0.0.0.0` or `127.0.0.1`

## Requirements 📋

- Python 3.7+
- OpenCV 4.8+
- DeepFace 0.0.75+
- TensorFlow 2.14+
- Flask 3.0+
- NumPy 1.24+

See `requirements.txt` for exact versions.

## Advanced Features 🚀

### Custom Emotion Detection Models
```python
from emotion_detector import EmotionDetector

detector = EmotionDetector(
    analysis_interval=0.3,
    enable_detection=True
)

stats = detector.get_stats()
```

### Streaming to Multiple Clients
The API server supports multiple concurrent connections for streaming and emotion data.

### Emotion History Analysis
Statistics are automatically tracked and can be saved to JSON:
```bash
python app.py --save-logs
```

## Future Enhancements 🌟

- [ ] WebSocket support for real-time updates
- [ ] Machine learning model optimization
- [ ] Emotion transition tracking
- [ ] Multiple emotion detection per face
- [ ] Audio emotion detection (tone of voice)
- [ ] Emotion prediction models
- [ ] Dashboard UI for historical analysis
- [ ] Cloud integration

## License 📄

This project is provided as-is for educational and commercial use.

## Contributing 🤝

Feel free to fork and submit improvements!

## Support 💬

For issues or questions, check the troubleshooting section or review the code documentation.

---

**Happy Emotion Detection!** 🎉
