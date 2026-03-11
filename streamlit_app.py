"""
AI Face Emotion Detection - Streamlit Web Application
Deploy on Streamlit Cloud and run directly from GitHub
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import json
import matplotlib.pyplot as plt
from emotion_detector_simple import SimplifiedEmotionDetector
import io

# Page configuration
st.set_page_config(
    page_title="AI Face Emotion Detection",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main {
        background-color: #1a1a2e;
        color: #ffffff;
    }
    h1 {
        color: #00d4ff;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    h2 {
        color: #00d4ff;
    }
    .emotion-box {
        background-color: #16213e;
        border: 2px solid #00d4ff;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'detector' not in st.session_state:
    st.session_state.detector = SimplifiedEmotionDetector(analysis_interval=0.1)

if 'emotion_history' not in st.session_state:
    st.session_state.emotion_history = []

if 'session_start' not in st.session_state:
    st.session_state.session_start = datetime.now()

# Title
st.markdown("""
<h1>😊 AI FACE EMOTION DETECTION 😊</h1>
<p style="text-align: center; color: #00d4ff; font-size: 0.9em;">
    Real-time Emotion Recognition with Beautiful Visual Reports
</p>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("### ⚙️ Configuration")
upload_option = st.sidebar.radio(
    "Choose Input Method",
    ["📷 Upload Image", "📊 Demo Mode", "📈 View Reports"]
)

# Emotion color mapping
EMOTION_COLORS = st.session_state.detector.EMOTION_COLORS
EMOTION_EMOJIS = st.session_state.detector.EMOTION_EMOJIS

def analyze_image(image):
    """Analyze image and detect emotions"""
    # Convert to BGR for OpenCV
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Analyze
    result = st.session_state.detector.analyze_frame(cv_image)
    
    return result, cv_image

def create_emotion_report(emotion_history):
    """Create a report from emotion history"""
    if not emotion_history:
        return None
    
    # Calculate statistics
    emotion_counts = {}
    emotion_totals = {e: 0.0 for e in st.session_state.detector.ALL_EMOTIONS}
    
    for entry in emotion_history:
        emotion = entry.get("dominant_emotion", "neutral")
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        for em, score in entry.get("all_emotions", {}).items():
            emotion_totals[em] += score
    
    # Calculate averages
    num_readings = len(emotion_history)
    emotion_averages = {e: emotion_totals[e] / num_readings for e in emotion_totals}
    
    return {
        "counts": emotion_counts,
        "averages": emotion_averages,
        "total_readings": num_readings,
        "dominant": max(emotion_averages, key=emotion_averages.get) if emotion_averages else "neutral"
    }

def draw_emotion_chart(report):
    """Draw emotion distribution chart"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor('#1a1a2e')
    
    # Pie chart
    emotions = list(report['counts'].keys())
    counts = list(report['counts'].values())
    colors_list = [EMOTION_COLORS.get(e, '#95A5A6') for e in emotions]
    
    axes[0].pie(counts, labels=emotions, colors=colors_list, autopct='%1.1f%%',
               textprops={'color': 'white', 'weight': 'bold'})
    axes[0].set_title("Emotion Distribution", color='white', fontsize=14, weight='bold')
    axes[0].set_facecolor('#16213e')
    
    # Bar chart
    emotions_sorted = sorted(report['averages'].keys(), 
                            key=lambda x: report['averages'][x], reverse=True)
    averages_sorted = [report['averages'][e] for e in emotions_sorted]
    colors_sorted = [EMOTION_COLORS.get(e, '#95A5A6') for e in emotions_sorted]
    
    axes[1].barh(emotions_sorted, averages_sorted, color=colors_sorted, edgecolor='white', linewidth=1.5)
    axes[1].set_xlabel("Average Score (%)", color='white', fontweight='bold')
    axes[1].set_xlim(0, 100)
    axes[1].set_facecolor('#16213e')
    axes[1].tick_params(colors='white')
    for spine in axes[1].spines.values():
        spine.set_color('white')
    axes[1].set_title("Average Emotion Scores", color='white', fontsize=14, weight='bold')
    
    for ax in axes:
        ax.tick_params(colors='white')
    
    return fig

# Main Content
if upload_option == "📷 Upload Image":
    st.markdown("### 📷 Upload an Image for Emotion Detection")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Load and display image
            image = Image.open(uploaded_file)
            st.image(image, caption="📸 Uploaded Image", use_column_width=True)
            
            # Analyze
            if st.button("🔍 Analyze Emotion", key="analyze_btn"):
                with st.spinner("🤖 Analyzing emotions..."):
                    result, cv_image = analyze_image(image)
                    
                    # Display results
                    col_res1, col_res2 = st.columns(2)
                    
                    with col_res1:
                        dominant = result.get('dominant_emotion', 'neutral')
                        confidence = result.get('dominant_confidence', 0)
                        emoji = EMOTION_EMOJIS.get(dominant, '😐')
                        
                        st.markdown(f"""
                        <div class="emotion-box">
                            <h2>{emoji} {dominant.upper()}</h2>
                            <p style="font-size: 1.5em; color: #00d4ff;">
                                Confidence: <b>{confidence}%</b>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_res2:
                        st.markdown("### 📊 All Emotions Detected")
                        emotions_dict = result.get('all_emotions', {})
                        
                        for emotion in sorted(emotions_dict.keys(), 
                                            key=lambda x: emotions_dict[x], reverse=True):
                            score = emotions_dict[emotion]
                            emoji = EMOTION_EMOJIS.get(emotion, '😐')
                            bar_length = int(score / 5)
                            bar = "█" * bar_length + "░" * (20 - bar_length)
                            st.markdown(f"{emoji} **{emotion.upper()}** | {bar} | **{score:.1f}%**")
                    
                    # Store in history for report
                    st.session_state.emotion_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "dominant_emotion": dominant,
                        "confidence": confidence,
                        "all_emotions": emotions_dict,
                        "faces_detected": result.get('faces_detected', 1)
                    })

elif upload_option == "📊 Demo Mode":
    st.markdown("### 📊 Demo: Multiple Emotion Samples")
    
    st.info("🎬 This demo analyzes sample images to show emotion detection capabilities")
    
    # Create sample emotions for demo
    demo_emotions = {
        "😊 Happy": {"happy": 85, "calm": 10, "neutral": 5},
        "😌 Calm": {"calm": 80, "neutral": 15, "happy": 5},
        "😐 Neutral": {"neutral": 75, "calm": 15, "happy": 10},
        "😲 Intense": {"intense": 80, "focus": 15, "happy": 5},
        "🧐 Focus": {"focus": 85, "intense": 10, "neutral": 5},
        "😭 Sad": {"sad": 85, "depression": 10, "calm": 5},
        "😔 Depression": {"depression": 85, "sad": 10, "neutral": 5},
    }
    
    cols = st.columns(3)
    col_idx = 0
    
    for emotion_name, scores in demo_emotions.items():
        with cols[col_idx % 3]:
            if st.button(f"Analyze {emotion_name}", key=f"demo_{emotion_name}"):
                # Create demo entry
                emotions_dict = {e: 0 for e in st.session_state.detector.ALL_EMOTIONS}
                emotions_dict.update(scores)
                
                # Normalize
                total = sum(emotions_dict.values())
                emotions_dict = {k: (v/total)*100 for k, v in emotions_dict.items()}
                
                st.session_state.emotion_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "dominant_emotion": max(emotions_dict, key=emotions_dict.get),
                    "confidence": int(max(emotions_dict.values())),
                    "all_emotions": emotions_dict,
                    "faces_detected": 1
                })
                
                st.success(f"✅ Added {emotion_name} to history!")
        
        col_idx += 1
    
    # Display history
    if st.session_state.emotion_history:
        st.markdown("### 📈 Detection History")
        report = create_emotion_report(st.session_state.emotion_history)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Detections", report['total_readings'])
        with col2:
            st.metric("Dominant Emotion", 
                     f"{EMOTION_EMOJIS.get(report['dominant'], '😐')} {report['dominant'].upper()}")
        
        # Draw charts
        fig = draw_emotion_chart(report)
        st.pyplot(fig)
        plt.close(fig)
        
        # Detailed breakdown
        st.markdown("### 📊 Detailed Breakdown")
        for emotion in sorted(report['averages'].keys(), 
                             key=lambda x: report['averages'][x], reverse=True):
            emoji = EMOTION_EMOJIS.get(emotion, '😐')
            avg = report['averages'][emotion]
            count = report['counts'].get(emotion, 0)
            percentage = (count / report['total_readings']) * 100 if report['total_readings'] > 0 else 0
            
            st.markdown(f"""
            {emoji} **{emotion.upper()}**
            - Average Score: {avg:.1f}%
            - Detected: {count} times ({percentage:.1f}%)
            """)

elif upload_option == "📈 View Reports":
    st.markdown("### 📈 Session Reports & History")
    
    if not st.session_state.emotion_history:
        st.warning("No emotion data collected yet. Upload images or use Demo Mode!")
    else:
        report = create_emotion_report(st.session_state.emotion_history)
        
        # Summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📹 Total Detections", report['total_readings'])
        with col2:
            st.metric("🎯 Dominant", report['dominant'].upper())
        with col3:
            session_duration = (datetime.now() - st.session_state.session_start).total_seconds()
            st.metric("⏱️ Session Time", f"{session_duration:.0f}s")
        with col4:
            fps = report['total_readings'] / session_duration if session_duration > 0 else 0
            st.metric("⚡ FPS", f"{fps:.1f}")
        
        st.markdown("---")
        
        # Draw charts
        fig = draw_emotion_chart(report)
        st.pyplot(fig)
        plt.close(fig)
        
        st.markdown("---")
        
        # Detailed statistics
        st.markdown("### 📊 Emotion Statistics")
        
        stats_cols = st.columns(2)
        
        with stats_cols[0]:
            st.markdown("#### Emotion Counts")
            for emotion in sorted(report['counts'].keys(), 
                                 key=lambda x: report['counts'][x], reverse=True):
                emoji = EMOTION_EMOJIS.get(emotion, '😐')
                count = report['counts'][emotion]
                percentage = (count / report['total_readings']) * 100
                st.markdown(f"{emoji} **{emotion.upper()}**: {count} times ({percentage:.1f}%)")
        
        with stats_cols[1]:
            st.markdown("#### Average Scores")
            for emotion in sorted(report['averages'].keys(), 
                                 key=lambda x: report['averages'][x], reverse=True):
                emoji = EMOTION_EMOJIS.get(emotion, '😐')
                avg = report['averages'][emotion]
                st.markdown(f"{emoji} **{emotion.upper()}**: {avg:.1f}%")
        
        st.markdown("---")
        
        # Export options
        st.markdown("### 💾 Export Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # JSON export
            json_data = json.dumps({
                "session": {
                    "start": st.session_state.session_start.isoformat(),
                    "end": datetime.now().isoformat(),
                    "duration": (datetime.now() - st.session_state.session_start).total_seconds()
                },
                "statistics": report,
                "history": st.session_state.emotion_history
            }, indent=2, default=str)
            
            st.download_button(
                label="📥 Download JSON Report",
                data=json_data,
                file_name=f"emotion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            # PNG export
            buf = io.BytesIO()
            fig = draw_emotion_chart(report)
            fig.savefig(buf, format='png', facecolor='#1a1a2e', bbox_inches='tight', dpi=150)
            buf.seek(0)
            
            st.download_button(
                label="📥 Download Chart PNG",
                data=buf,
                file_name=f"emotion_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )
            plt.close(fig)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #00d4ff; margin-top: 30px;">
    <h4>🚀 AI Face Emotion Detection</h4>
    <p>Powered by OpenCV & Streamlit</p>
    <p style="font-size: 0.8em; color: #a0a0a0;">
        Developed by DARSHAN GOWDA G D
    </p>
</div>
""", unsafe_allow_html=True)
