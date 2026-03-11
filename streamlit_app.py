"""
AI Face Emotion Detection - Streamlit Web Application
Lightweight version for Streamlit Cloud (no heavy dependencies)
"""

import streamlit as st
from datetime import datetime
import json
import matplotlib.pyplot as plt
import io

# Page configuration
st.set_page_config(
    page_title="AI Face Emotion Detection",
    page_icon="😊",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .main { background-color: #1a1a2e; color: #ffffff; }
    h1 { color: #00d4ff; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5); }
    h2 { color: #00d4ff; }
    .emotion-box {
        background-color: #16213e;
        border: 2px solid #00d4ff;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Emotion mappings
EMOTIONS = {
    "Happy": ("😊", "#00FF00"),
    "Calm": ("😌", "#64C8FF"),
    "Neutral": ("😐", "#C8C8C8"),
    "Intense": ("😲", "#FF0000"),
    "Focus": ("🧐", "#C86400"),
    "Sad": ("😭", "#00FFFF"),
    "Depression": ("😔", "#8B00FF")
}

# Initialize session state
if 'emotion_history' not in st.session_state:
    st.session_state.emotion_history = []
if 'session_start' not in st.session_state:
    st.session_state.session_start = datetime.now()

# Title
st.markdown("<h1>😊 AI FACE EMOTION DETECTION 😊</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00d4ff;'>Real-time Emotion Recognition</p>", unsafe_allow_html=True)

# Sidebar
page = st.sidebar.radio("📋 Select Mode", ["📊 Demo", "📈 Reports", "ℹ️ About"])

if page == "📊 Demo":
    st.markdown("### 📊 Emotion Detection Demo")
    st.info("Click any emotion to add it to your session history")
    
    cols = st.columns(3)
    for idx, (emotion, (emoji, color)) in enumerate(EMOTIONS.items()):
        with cols[idx % 3]:
            if st.button(f"{emoji} {emotion}", key=f"btn_{emotion}", use_container_width=True):
                st.session_state.emotion_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "emotion": emotion,
                    "emoji": emoji
                })
                st.success(f"✅ Added {emotion}!")
                st.rerun()
    
    # Show history
    if st.session_state.emotion_history:
        st.divider()
        st.markdown(f"### 📊 History ({len(st.session_state.emotion_history)} detections)")
        
        # Count emotions
        counts = {}
        for entry in st.session_state.emotion_history:
            emotion = entry['emotion']
            counts[emotion] = counts.get(emotion, 0) + 1
        
        # Create chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        fig.patch.set_facecolor('#1a1a2e')
        
        emotions_list = list(counts.keys())
        colors_list = [EMOTIONS[e][1] for e in emotions_list]
        
        ax1.pie(counts.values(), labels=emotions_list, colors=colors_list, autopct='%1.1f%%',
               textprops={'color': 'white', 'weight': 'bold'})
        ax1.set_facecolor('#16213e')
        ax1.set_title("Distribution", color='white', fontsize=12, weight='bold')
        
        ax2.barh(emotions_list, list(counts.values()), color=colors_list, edgecolor='white')
        ax2.set_facecolor('#16213e')
        ax2.set_xlabel("Count", color='white', fontweight='bold')
        ax2.tick_params(colors='white')
        for spine in ax2.spines.values():
            spine.set_color('white')
        ax2.set_title("Frequency", color='white', fontsize=12, weight='bold')
        
        st.pyplot(fig)
        plt.close()
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", len(st.session_state.emotion_history))
        with col2:
            dominant = max(counts, key=counts.get)
            st.metric("Top", f"{EMOTIONS[dominant][0]} {dominant}")
        with col3:
            duration = (datetime.now() - st.session_state.session_start).total_seconds()
            st.metric("Session", f"{duration:.0f}s")
        
        # Export
        if st.button("💾 Export as JSON"):
            data = json.dumps(st.session_state.emotion_history, indent=2)
            st.download_button(
                "📥 Download JSON",
                data,
                f"emotions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json"
            )

elif page == "📈 Reports":
    st.markdown("### 📈 Session Reports")
    
    if not st.session_state.emotion_history:
        st.warning("No data yet. Use Demo mode to collect emotions!")
    else:
        counts = {}
        for entry in st.session_state.emotion_history:
            emotion = entry['emotion']
            counts[emotion] = counts.get(emotion, 0) + 1
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total", len(st.session_state.emotion_history))
        with col2:
            dominant = max(counts, key=counts.get)
            st.metric("Dominant", dominant)
        with col3:
            duration = (datetime.now() - st.session_state.session_start).total_seconds()
            st.metric("Duration", f"{duration:.0f}s")
        with col4:
            fps = len(st.session_state.emotion_history) / max(duration, 1)
            st.metric("Rate", f"{fps:.2f}/s")
        
        st.divider()
        
        # Detailed breakdown
        st.markdown("**Emotion Breakdown:**")
        for emotion in sorted(counts.keys(), key=lambda x: counts[x], reverse=True):
            emoji, color = EMOTIONS[emotion]
            pct = (counts[emotion] / len(st.session_state.emotion_history)) * 100
            st.markdown(f"{emoji} **{emotion}**: {counts[emotion]} ({pct:.1f}%)")

elif page == "ℹ️ About":
    st.markdown("""
    ### 🚀 AI Face Emotion Detection
    
    **7 Emotion Categories:**
    - 😊 Happy
    - 😌 Calm
    - 😐 Neutral
    - 😲 Intense
    - 🧐 Focus
    - 😭 Sad
    - 😔 Depression
    
    **Features:**
    - Real-time emotion detection
    - Beautiful visual reports
    - Session statistics
    - Export as JSON
    
    **Technologies:**
    - Streamlit (Web Framework)
    - OpenCV (Detection Engine)
    - Matplotlib (Visualizations)
    
    ---
    **Developer:** DARSHAN GOWDA G D
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #00d4ff;'>
    <p>🚀 AI Face Emotion Detection | Powered by Streamlit</p>
</div>
""", unsafe_allow_html=True)
