"""
Example Integrations
Demonstrates how to use the emotion detection system with other applications
"""

import cv2
import json
from client_library import (
    EmotionDetectionClient,
    EmotionProcessor,
    EmotionCallback
)


# ===== EXAMPLE 1: Simple Integration with Local Mode =====

def example_simple_local():
    """Simple local emotion detection"""
    print("=" * 60)
    print("EXAMPLE 1: Simple Local Emotion Detection")
    print("=" * 60)
    
    client = EmotionDetectionClient(mode='local')
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect emotion
        result = client.detect_emotion(frame)
        
        # Get emotion data
        emotion = result.get('dominant_emotion', 'unknown')
        confidence = result.get('dominant_confidence', 0)
        
        print(f"Emotion: {emotion}, Confidence: {confidence}%")
        
        # Visualize
        frame = client.visualize_frame(frame)
        cv2.imshow("Emotion Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


# ===== EXAMPLE 2: Remote API Integration =====

def example_remote_api():
    """Use remote emotion detection API"""
    print("=" * 60)
    print("EXAMPLE 2: Remote API Integration")
    print("=" * 60)
    
    client = EmotionDetectionClient(mode='remote', api_url='http://localhost:5000')
    
    # Start streaming on server
    if client.start_stream():
        print("Streaming started on server")
        
        try:
            for i in range(10):
                # Get emotion from remote API
                emotion_data = client.get_current_emotion()
                
                print(f"Frame {i+1}:")
                print(f"  Emotion: {emotion_data.get('dominant_emotion')}")
                print(f"  Confidence: {emotion_data.get('confidence')}%")
                print()
        
        finally:
            # Stop streaming
            client.stop_stream()
            print("Streaming stopped")
    else:
        print("Failed to start streaming")


# ===== EXAMPLE 3: Custom Callbacks =====

def example_callbacks():
    """Use custom callbacks for emotion detection"""
    print("=" * 60)
    print("EXAMPLE 3: Custom Callbacks")
    print("=" * 60)
    
    class EmotionLogger(EmotionCallback):
        """Log all emotion changes"""
        
        def __init__(self):
            self.emotion_history = []
        
        def on_emotion_detected(self, emotion, confidence, all_emotions):
            # Log every emotion detection
            self.emotion_history.append({
                "emotion": emotion,
                "confidence": confidence,
                "timestamp": len(self.emotion_history)
            })
        
        def on_emotion_change(self, emotion, confidence):
            # Alert when emotion changes
            print(f"🎭 EMOTION CHANGED: {emotion} ({confidence}%)")
        
        def on_no_face_detected(self):
            print("⚠️  No face detected")
        
        def save_history(self, filename="emotion_history.json"):
            with open(filename, 'w') as f:
                json.dump(self.emotion_history, f, indent=2)
            print(f"History saved to {filename}")
    
    # Create processor with callback
    processor = EmotionProcessor(camera_id=0)
    logger = EmotionLogger()
    processor.add_callback(logger)
    
    print("Starting emotion detection with logging...")
    print("Press 'q' to quit\n")
    
    processor.run(show_display=True)
    
    # Save history
    logger.save_history()


# ===== EXAMPLE 4: Game Integration =====

def example_game_integration():
    """Emotion-based game control example"""
    print("=" * 60)
    print("EXAMPLE 4: Emotion-Based Game Control")
    print("=" * 60)
    
    class GameControlCallback(EmotionCallback):
        """Map emotions to game actions"""
        
        def __init__(self):
            self.game_state = {
                "power_level": 0,
                "defense_mode": False,
                "special_attack_ready": False
            }
        
        def on_emotion_detected(self, emotion, confidence, all_emotions):
            # Map emotions to game mechanics
            if emotion == "angry" and confidence > 70:
                self.game_state["power_level"] = min(100, confidence)
                print(f"⚡ Power Level: {self.game_state['power_level']}%")
            
            elif emotion == "fear" and confidence > 60:
                self.game_state["defense_mode"] = True
                print("🛡️  Defense Mode ACTIVE")
            
            elif emotion == "happy" and confidence > 75:
                self.game_state["special_attack_ready"] = True
                print("✨ Special Attack READY!")
            
            elif emotion == "neutral":
                self.game_state["defense_mode"] = False
                self.game_state["special_attack_ready"] = False
                print("⚖️  Neutral State")
    
    processor = EmotionProcessor(camera_id=0)
    game_controller = GameControlCallback()
    processor.add_callback(game_controller)
    
    print("Starting emotion-based game control...")
    print("Different emotions trigger different game actions!")
    print("Press 'q' to quit\n")
    
    processor.run(show_display=True)


# ===== EXAMPLE 5: Streaming to Web App =====

def example_web_integration():
    """Example HTML/JavaScript for web integration"""
    html_code = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Emotion Detection Dashboard</title>
        <style>
            body { font-family: Arial; margin: 20px; background: #1a1a1a; color: #fff; }
            .container { max-width: 1200px; margin: 0 auto; }
            .emotion-display { font-size: 48px; font-weight: bold; padding: 20px; }
            .emotion-bars { display: flex; flex-direction: column; gap: 10px; }
            .bar { display: flex; align-items: center; }
            .bar-label { width: 100px; }
            .bar-container { flex: 1; background: #333; height: 30px; border-radius: 5px; }
            .bar-fill { height: 100%; border-radius: 5px; transition: width 0.2s; }
            .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 20px; }
            .stat-box { background: #222; padding: 15px; border-radius: 5px; }
            #video { width: 100%; max-width: 640px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 Emotion Detection Dashboard</h1>
            
            <img id="video" src="http://localhost:5000/api/video" alt="Live Stream">
            
            <div class="emotion-display" id="emotionDisplay">Detecting...</div>
            
            <div class="stats">
                <div class="stat-box">
                    <h3>Current Emotion</h3>
                    <p id="currentEmotion">-</p>
                </div>
                <div class="stat-box">
                    <h3>Confidence</h3>
                    <p id="confidence">-</p>
                </div>
                <div class="stat-box">
                    <h3>Faces Detected</h3>
                    <p id="facesDetected">-</p>
                </div>
                <div class="stat-box">
                    <h3>FPS</h3>
                    <p id="fps">-</p>
                </div>
            </div>
            
            <h2>Emotion Analysis</h2>
            <div class="emotion-bars" id="emotionBars"></div>
        </div>
        
        <script>
            const API_URL = 'http://localhost:5000';
            
            async function updateDashboard() {
                try {
                    const response = await fetch(API_URL + '/api/emotion');
                    const data = await response.json();
                    
                    // Update emotion display
                    document.getElementById('emotionDisplay').textContent = 
                        data.dominant_emotion.toUpperCase();
                    document.getElementById('currentEmotion').textContent = 
                        data.dominant_emotion;
                    document.getElementById('confidence').textContent = 
                        data.confidence + '%';
                    document.getElementById('facesDetected').textContent = 
                        data.faces_detected;
                    document.getElementById('fps').textContent = 
                        data.fps;
                    
                    // Update emotion bars
                    const barsContainer = document.getElementById('emotionBars');
                    barsContainer.innerHTML = '';
                    
                    Object.entries(data.all_emotions).forEach(([emotion, score]) => {
                        const bar = document.createElement('div');
                        bar.className = 'bar';
                        bar.innerHTML = `
                            <div class="bar-label">${emotion}:</div>
                            <div class="bar-container">
                                <div class="bar-fill" 
                                     style="width: ${score}%; 
                                             background: ${getEmotionColor(emotion)};">
                                </div>
                            </div>
                            <div>${Math.round(score)}%</div>
                        `;
                        barsContainer.appendChild(bar);
                    });
                } catch(e) {
                    console.error('Error:', e);
                }
            }
            
            function getEmotionColor(emotion) {
                const colors = {
                    'angry': '#FF0000',
                    'disgust': '#FF6600',
                    'fear': '#8000FF',
                    'happy': '#00FF00',
                    'neutral': '#C0C0C0',
                    'sad': '#0000FF',
                    'surprise': '#FFFF00'
                };
                return colors[emotion] || '#FFFFFF';
            }
            
            // Start streaming
            async function startStreaming() {
                await fetch(API_URL + '/api/stream/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ camera_id: 0 })
                });
            }
            
            // Initialize
            startStreaming();
            setInterval(updateDashboard, 500);
        </script>
    </body>
    </html>
    '''
    
    print("=" * 60)
    print("EXAMPLE 5: Web Integration")
    print("=" * 60)
    print("\nSave this HTML code to a file (e.g., dashboard.html)")
    print("and open it in a browser while the API server is running.\n")
    print(html_code)


# ===== EXAMPLE 6: Real-Time Alerts =====

def example_alerts():
    """Emotion-based alert system"""
    print("=" * 60)
    print("EXAMPLE 6: Real-Time Alerts")
    print("=" * 60)
    
    class AlertCallback(EmotionCallback):
        
        def __init__(self):
            self.last_emotion = None
        
        def on_emotion_change(self, emotion, confidence):
            alerts = {
                "angry": "⚠️  ALERT: Angry emotion detected! Activating calming protocol...",
                "sad": "💙 NOTE: Sadness detected. Consider playing uplifting content.",
                "fear": "😨 WARNING: Fear detected! Checking safety systems...",
                "happy": "😊 Happiness detected! Positive energy level high!",
                "surprise": "😮 SURPRISE detected! Event recorded.",
            }
            
            if emotion in alerts:
                print(alerts[emotion])
    
    processor = EmotionProcessor(camera_id=0)
    alert_system = AlertCallback()
    processor.add_callback(alert_system)
    
    print("Starting emotion alert system...")
    processor.run(show_display=True)


# ===== MAIN MENU =====

def main():
    """Run example menu"""
    examples = {
        '1': ('Simple Local Detection', example_simple_local),
        '2': ('Remote API Integration', example_remote_api),
        '3': ('Custom Callbacks', example_callbacks),
        '4': ('Game Integration', example_game_integration),
        '5': ('Web Integration (HTML)', example_web_integration),
        '6': ('Real-Time Alerts', example_alerts),
    }
    
    print("\n" + "=" * 60)
    print("EMOTION DETECTION - EXAMPLES")
    print("=" * 60)
    print("\nAvailable Examples:\n")
    
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    
    print(f"\n  0. Exit\n")
    
    while True:
        choice = input("Select an example (0-6): ").strip()
        
        if choice == '0':
            print("Goodbye!")
            break
        
        if choice in examples:
            try:
                name, func = examples[choice]
                print(f"\nRunning: {name}\n")
                func()
            except KeyboardInterrupt:
                print("\n\nExample interrupted. Returning to menu...\n")
            except Exception as e:
                print(f"Error: {e}\n")
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
