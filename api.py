"""
Flask API for Emotion Detection
Allows integration with other applications
"""

from flask import Flask, jsonify, Response, request
from emotion_detector import EmotionDetector
import cv2
import numpy as np
import json
from datetime import datetime
import threading

app = Flask(__name__)

# Global emotion detector instance
detector = EmotionDetector(analysis_interval=0.3, enable_detection=True)
cap = None
is_streaming = False
current_frame = None


def init_camera(camera_id=0):
    """Initialize camera"""
    global cap
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        return False
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    return True


def camera_stream():
    """Generate video stream frames"""
    global current_frame
    
    while is_streaming and cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Analyze frame
        frame = cv2.flip(frame, 1)
        detector.analyze_frame(frame)
        detector.update_fps()
        
        # Store current frame
        current_frame = frame
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200


@app.route('/api/emotion', methods=['GET'])
def get_emotion():
    """Get current emotion data"""
    return jsonify({
        "dominant_emotion": detector.dominant_emotion,
        "confidence": detector.dominant_confidence,
        "all_emotions": detector.current_emotions,
        "faces_detected": detector.faces_detected,
        "fps": detector.fps,
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/emotion/history', methods=['GET'])
def get_emotion_history():
    """Get emotion statistics"""
    limit = request.args.get('limit', 100, type=int)
    
    return jsonify({
        "current_stats": detector.get_stats(),
        "emotion_colors": detector.EMOTION_COLORS,
        "available_emotions": detector.ALL_EMOTIONS
    }), 200


@app.route('/api/stream/start', methods=['POST'])
def start_stream():
    """Start video stream"""
    global is_streaming
    
    camera_id = request.json.get('camera_id', 0) if request.is_json else 0
    
    if not init_camera(camera_id):
        return jsonify({"error": f"Failed to open camera {camera_id}"}), 400
    
    is_streaming = True
    
    return jsonify({
        "status": "streaming_started",
        "camera_id": camera_id,
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/stream/stop', methods=['POST'])
def stop_stream():
    """Stop video stream"""
    global is_streaming, cap
    
    is_streaming = False
    
    if cap:
        cap.release()
        cap = None
    
    return jsonify({
        "status": "streaming_stopped",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/video', methods=['GET'])
def video():
    """Stream video frames"""
    if not is_streaming:
        return jsonify({"error": "Streaming not started"}), 400
    
    return Response(
        camera_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    ), 200


@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    """Analyze emotion from uploaded image"""
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    
    try:
        # Read image from file
        file_bytes = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({"error": "Failed to decode image"}), 400
        
        # Analyze
        result = detector.analyze_frame(frame)
        
        return jsonify({
            "analysis": result,
            "emotion_colors": detector.EMOTION_COLORS,
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get configuration and available emotions"""
    return jsonify({
        "detector": {
            "analysis_interval": detector.analysis_interval,
            "enforce_detection": detector.enforce_detection
        },
        "emotions": {
            "available": detector.ALL_EMOTIONS,
            "colors": detector.EMOTION_COLORS
        },
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/config', methods=['PUT'])
def update_config():
    """Update detector configuration"""
    data = request.get_json()
    
    if 'analysis_interval' in data:
        detector.analysis_interval = float(data['analysis_interval'])
    
    return jsonify({
        "status": "configuration_updated",
        "config": {
            "analysis_interval": detector.analysis_interval,
            "enforce_detection": detector.enforce_detection
        },
        "timestamp": datetime.now().isoformat()
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
