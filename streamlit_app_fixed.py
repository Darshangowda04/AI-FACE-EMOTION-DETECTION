"""
Fixed Streamlit App with Proper Camera Access
Deploy to Streamlit Cloud for live emotion detection
"""

import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
import threading
import cv2
import numpy as np
from emotion_detector_simple import SimplifiedEmotionDetector
from visualizer import EmotionVisualizer
from datetime import datetime
import json
from io import BytesIO

# Page config
st.set_page_config(
    page_title="AI Face Emotion Detection",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    .main { background-color: #1a1a2e; color: #ffffff; }
    h1, h2, h3 { color: #00d4ff; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5); }
    .stat-box {
        background-color: #16213e;
        border: 2px solid #00d4ff;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .emotion-box {
        background-color: #16213e;
        border-left: 4px solid #00d4ff;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .success-box {
        background-color: rgba(46, 204, 113, 0.1);
        border: 2px solid #2ecc71;
        padding: 15px;
        border-radius: 8px;
        color: #2ecc71;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'detector' not in st.session_state:
    st.session_state.detector = SimplifiedEmotionDetector(analysis_interval=0.3)
    st.session_state.visualizer = EmotionVisualizer(st.session_state.detector.EMOTION_COLORS)

if 'emotion_history' not in st.session_state:
    st.session_state.emotion_history = []

if 'session_active' not in st.session_state:
    st.session_state.session_active = False

if 'session_start' not in st.session_state:
    st.session_state.session_start = None

# Title
st.markdown("<h1 style='text-align: center;'>😊 AI FACE EMOTION DETECTION 😊</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00d4ff;'>Real-time Emotion Recognition with Beautiful Analysis</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 📋 Options")
    mode = st.radio("Select Mode", ["🎥 Live Detection", "📊 Statistics", "ℹ️ About"])
    st.divider()

# Main content based on mode
if mode == "🎥 Live Detection":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📹 Camera Feed")
        
        # RTC configuration
        rtc_configuration = RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        )
        
        class VideoProcessor:
            def __init__(self):
                self.detector = st.session_state.detector
                self.visualizer = st.session_state.visualizer
            
            def recv(self, frame):
                img = frame.to_ndarray(format="bgr24")
                img = cv2.flip(img, 1)
                
                # Detect emotion
                self.detector.analyze_frame(img)
                self.detector.update_fps()
                
                # Record emotion
                st.session_state.emotion_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "emotion": self.detector.dominant_emotion,
                    "confidence": self.detector.dominant_confidence,
                    "all_emotions": self.detector.current_emotions.copy()
                })
                
                # Render HUD
                img = self.visualizer.render_complete_hud(
                    img,
                    emotion=self.detector.dominant_emotion,
                    confidence=self.detector.dominant_confidence,
                    all_emotions=self.detector.current_emotions,
                    emotion_colors=self.detector.EMOTION_COLORS,
                    faces_detected=self.detector.faces_detected,
                    fps=self.detector.fps
                )
                
                return av.VideoFrame.from_ndarray(img, format="bgr24")
        
        # Start detection
        webrtc_ctx = webrtc_streamer(
            key="emotion-detection",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=rtc_configuration,
            video_processor_factory=VideoProcessor,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
            disabled=False,
        )
        
        if webrtc_ctx.state.playing:
            st.session_state.session_active = True
            if st.session_state.session_start is None:
                st.session_state.session_start = datetime.now()
    
    with col2:
        st.markdown("### 📊 Stats")
        
        if st.session_state.emotion_history:
            # Calculate current stats
            emotions_count = {}
            confidences = []
            
            for entry in st.session_state.emotion_history:
                emotion = entry['emotion']
                emotions_count[emotion] = emotions_count.get(emotion, 0) + 1
                confidences.append(entry['confidence'])
            
            # Display stats
            st.markdown(f"<div class='stat-box'><strong>Total Frames:</strong> {len(st.session_state.emotion_history)}</div>", unsafe_allow_html=True)
            
            duration = (datetime.now() - st.session_state.session_start).total_seconds() if st.session_state.session_start else 0
            st.markdown(f"<div class='stat-box'><strong>Duration:</strong> {duration:.1f}s</div>", unsafe_allow_html=True)
            
            fps = len(st.session_state.emotion_history) / duration if duration > 0 else 0
            st.markdown(f"<div class='stat-box'><strong>FPS:</strong> {fps:.1f}</div>", unsafe_allow_html=True)
            
            dominant = max(emotions_count, key=emotions_count.get)
            st.markdown(f"<div class='stat-box'><strong>Dominant Emotion:</strong> {dominant.upper()}</div>", unsafe_allow_html=True)
            
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            st.markdown(f"<div class='stat-box'><strong>Confidence:</strong> {avg_confidence:.1f}%</div>", unsafe_allow_html=True)
            
            # Emotion bars
            st.markdown("### 😊 Emotions")
            sorted_emotions = sorted(emotions_count.items(), key=lambda x: x[1], reverse=True)
            
            for emotion, count in sorted_emotions:
                percentage = (count / len(st.session_state.emotion_history)) * 100
                st.progress(percentage / 100, text=f"{emotion.title()}: {percentage:.1f}%")
        else:
            st.info("👈 Start camera to see statistics")

elif mode == "📊 Statistics":
    st.markdown("### 📊 Session Statistics")
    
    if st.session_state.emotion_history:
        col1, col2, col3 = st.columns(3)
        
        emotions_count = {}
        confidences = []
        all_emotions_data = {e: [] for e in st.session_state.detector.ALL_EMOTIONS}
        
        for entry in st.session_state.emotion_history:
            emotion = entry['emotion']
            emotions_count[emotion] = emotions_count.get(emotion, 0) + 1
            confidences.append(entry['confidence'])
            
            for e, score in entry['all_emotions'].items():
                all_emotions_data[e].append(score)
        
        # Metrics
        with col1:
            st.metric("Total Frames", len(st.session_state.emotion_history))
        
        with col2:
            duration = (datetime.now() - st.session_state.session_start).total_seconds() if st.session_state.session_start else 0
            st.metric("Duration", f"{duration:.1f}s")
        
        with col3:
            fps = len(st.session_state.emotion_history) / duration if duration > 0 else 0
            st.metric("FPS", f"{fps:.1f}")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Emotion Distribution")
            st.bar_chart(emotions_count)
        
        with col2:
            st.markdown("#### Average Confidence")
            avg_conf_by_emotion = {}
            for e, scores in all_emotions_data.items():
                if scores:
                    avg_conf_by_emotion[e] = sum(scores) / len(scores)
            
            st.bar_chart(avg_conf_by_emotion)
        
        # Download report
        st.markdown("#### 📥 Download Report")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "session_duration": (datetime.now() - st.session_state.session_start).total_seconds() if st.session_state.session_start else 0,
            "total_frames": len(st.session_state.emotion_history),
            "emotions": emotions_count,
            "average_confidence": sum(confidences) / len(confidences) if confidences else 0,
            "emotion_details": all_emotions_data,
            "developer": "DARSHAN GOWDA G D",
            "github": "https://github.com/Darshangowda04",
            "linkedin": "https://www.linkedin.com/in/darshan-gowda-g-d-b7473132b/"
        }
        
        json_str = json.dumps(report, indent=2)
        st.download_button(
            label="📥 Download JSON Report",
            data=json_str,
            file_name=f"emotion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        # Clear data
        if st.button("🗑️ Clear Session Data"):
            st.session_state.emotion_history = []
            st.session_state.session_start = None
            st.rerun()
    else:
        st.info("No data collected yet. Start detection in 'Live Detection' mode!")

elif mode == "ℹ️ About":
    st.markdown("### 👨‍💻 About This Project")
    
    st.markdown("""
    **AI Face Emotion Detection** is a real-time emotion recognition system that uses:
    
    - **OpenCV**: For face detection and feature extraction
    - **TensorFlow**: For deep learning models
    - **Streamlit**: For interactive web interface
    - **Python**: Core programming language
    
    ### Features:
    ✅ Real-time emotion detection (5 emotions: Happy, Calm, Neutral, Focus, Intense)
    ✅ Live video streaming with emotion overlays
    ✅ Detailed statistics and analysis
    ✅ Beautiful visualizations and charts
    ✅ JSON report generation
    
    ### Developer Information:
    **DARSHAN GOWDA G D**
    
    - 🔗 [GitHub](https://github.com/Darshangowda04)
    - 💼 [LinkedIn](https://www.linkedin.com/in/darshan-gowda-g-d-b7473132b/)
    
    ### How to Use:
    1. Go to **Live Detection** mode
    2. Click "Start" to enable your camera
    3. Look at the camera naturally for emotion detection
    4. View real-time statistics on the right panel
    5. Go to **Statistics** to download your report
    
    © 2026 - All Rights Reserved
    """)
    
    st.divider()
    st.markdown("""
    <div class='success-box'>
    ✅ This application is live and ready to use!
    </div>
    """, unsafe_allow_html=True)
