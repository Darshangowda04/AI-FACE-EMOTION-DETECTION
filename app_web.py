"""
Flask Web App for AI Face Emotion Detection with Real-time Camera Streaming
Deploy to Render, Heroku, or Railway for live emotion detection
"""

from flask import Flask, render_template, Response, jsonify, request
from emotion_detector_simple import SimplifiedEmotionDetector
from visualizer import EmotionVisualizer
from datetime import datetime
import cv2
import threading
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Global state
class EmotionDetectionState:
    def __init__(self):
        self.detector = SimplifiedEmotionDetector(analysis_interval=0.3)
        self.visualizer = EmotionVisualizer(self.detector.EMOTION_COLORS)
        self.cap = None
        self.is_running = False
        self.frame_lock = threading.Lock()
        self.current_frame = None
        self.emotion_history = []
        self.session_start = datetime.now()
        
    def start_camera(self):
        """Initialize camera"""
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.is_running = True
        
    def stop_camera(self):
        """Stop camera and cleanup"""
        self.is_running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None
    
    def get_frame(self):
        """Get current frame with emotion detection"""
        if not self.is_running or self.cap is None or not self.cap.isOpened():
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        frame = cv2.flip(frame, 1)
        
        # Analyze
        result = self.detector.analyze_frame(frame)
        self.detector.update_fps()
        
        # Record emotion
        self.emotion_history.append({
            "timestamp": datetime.now().isoformat(),
            "emotion": self.detector.dominant_emotion,
            "confidence": self.detector.dominant_confidence,
            "all_emotions": self.detector.current_emotions.copy()
        })
        
        # Render
        frame = self.visualizer.render_complete_hud(
            frame,
            emotion=self.detector.dominant_emotion,
            confidence=self.detector.dominant_confidence,
            all_emotions=self.detector.current_emotions,
            emotion_colors=self.detector.EMOTION_COLORS,
            faces_detected=self.detector.faces_detected,
            fps=self.detector.fps
        )
        
        # Encode frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        with self.frame_lock:
            self.current_frame = frame_bytes
        
        return frame_bytes

state = EmotionDetectionState()

def generate_frames():
    """Generate video frames"""
    state.start_camera()
    
    try:
        while state.is_running:
            frame = state.get_frame()
            if frame is None:
                continue
            
            # MJPEG format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        state.stop_camera()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/video_feed')
def video_feed():
    """Video streaming endpoint"""
    state.start_camera()
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/start', methods=['POST'])
def start_detection():
    """Start emotion detection"""
    state.start_camera()
    state.emotion_history = []
    state.session_start = datetime.now()
    return jsonify({"status": "started"})

@app.route('/api/stop', methods=['POST'])
def stop_detection():
    """Stop emotion detection"""
    state.stop_camera()
    return jsonify({"status": "stopped"})

@app.route('/api/stats')
def get_stats():
    """Get current statistics"""
    if not state.emotion_history:
        return jsonify({
            "total_frames": 0,
            "duration": 0,
            "emotions": {},
            "dominant_emotion": "N/A",
            "average_confidence": 0
        })
    
    # Calculate stats
    emotions_count = {}
    total_confidence = 0
    
    for entry in state.emotion_history:
        emotion = entry['emotion']
        emotions_count[emotion] = emotions_count.get(emotion, 0) + 1
        total_confidence += entry['confidence']
    
    # Get dominant
    dominant = max(emotions_count, key=emotions_count.get) if emotions_count else "N/A"
    
    # Calculate percentages
    emotions_percent = {}
    for emotion, count in emotions_count.items():
        emotions_percent[emotion] = round((count / len(state.emotion_history)) * 100, 2)
    
    duration = (datetime.now() - state.session_start).total_seconds()
    
    return jsonify({
        "total_frames": len(state.emotion_history),
        "duration": round(duration, 1),
        "fps": round(len(state.emotion_history) / duration, 1) if duration > 0 else 0,
        "emotions": emotions_percent,
        "dominant_emotion": dominant,
        "average_confidence": round(total_confidence / len(state.emotion_history), 1),
        "is_running": state.is_running
    })

@app.route('/api/report')
def get_report():
    """Get detailed report"""
    if not state.emotion_history:
        return jsonify({"error": "No data collected"}), 400
    
    # Generate report
    emotions_count = {}
    emotion_details = {e: [] for e in state.detector.ALL_EMOTIONS}
    
    for entry in state.emotion_history:
        emotion = entry['emotion']
        emotions_count[emotion] = emotions_count.get(emotion, 0) + 1
        emotion_details[emotion].append(entry['confidence'])
    
    # Calculate averages for each emotion
    avg_by_emotion = {}
    for emotion in state.detector.ALL_EMOTIONS:
        if emotion_details[emotion]:
            avg_by_emotion[emotion] = round(sum(emotion_details[emotion]) / len(emotion_details[emotion]), 2)
        else:
            avg_by_emotion[emotion] = 0
    
    duration = (datetime.now() - state.session_start).total_seconds()
    
    return jsonify({
        "session_start": state.session_start.isoformat(),
        "session_duration": round(duration, 1),
        "total_frames": len(state.emotion_history),
        "fps": round(len(state.emotion_history) / duration, 1) if duration > 0 else 0,
        "emotions_count": emotions_count,
        "average_confidence_by_emotion": avg_by_emotion,
        "all_emotions": state.detector.ALL_EMOTIONS,
        "emotion_colors": state.detector.EMOTION_COLORS,
        "history": state.emotion_history[-100:] if len(state.emotion_history) > 100 else state.emotion_history
    })

@app.route('/api/download_report')
def download_report():
    """Download JSON report"""
    if not state.emotion_history:
        return jsonify({"error": "No data collected"}), 400
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "session_start": state.session_start.isoformat(),
        "total_frames": len(state.emotion_history),
        "duration": round((datetime.now() - state.session_start).total_seconds(), 1),
        "emotion_history": state.emotion_history,
        "developer": "DARSHAN GOWDA G D",
        "github": "https://github.com/Darshangowda04",
        "linkedin": "https://www.linkedin.com/in/darshan-gowda-g-d-b7473132b/"
    }
    
    from flask import send_file
    import io
    
    file_bytes = io.BytesIO(json.dumps(report, indent=2).encode())
    filename = f"emotion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    return send_file(
        file_bytes,
        mimetype='application/json',
        as_attachment=True,
        download_name=filename
    )

@app.errorhandler(404)
def not_found(error):
    """Handle 404"""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
