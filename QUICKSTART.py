"""
Quick Start Guide
Get the emotion detection system running in 5 minutes
"""

print("""
╔══════════════════════════════════════════════════════════════╗
║     AI FACE EMOTION DETECTION - QUICK START GUIDE            ║
╚══════════════════════════════════════════════════════════════╝

STEP 1: INSTALL DEPENDENCIES
────────────────────────────

1. Open Command Prompt / PowerShell
2. Navigate to project directory:
   cd path\\to\\ai-face-emotion-detection

3. Create virtual environment (recommended):
   python -m venv venv
   venv\\Scripts\\activate

4. Install dependencies:
   pip install -r requirements.txt

⏱️  This takes 3-5 minutes depending on internet speed


STEP 2: RUN THE APPLICATION
────────────────────────────

Option A - Simple Real-Time Detection (Recommended for first time):
   python app.py

Option B - REST API Server (For integration with other apps):
   python api.py

Option C - Run Examples:
   python examples.py


STEP 3: INTERACT WITH THE APPLICATION
──────────────────────────────────────

Real-Time App (app.py):
  • Q key - Quit application
  • S key - Save emotion statistics
  • Watch the HUD display emotions in real-time
  • See color-coded emotion bars

REST API (api.py):
  • Open browser: http://localhost:5000
  • View live camera feed
  • Get emotion data via /api/emotion endpoint
  • Stream video via /api/video endpoint


WHAT TO EXPECT
───────────────

✅ Real-time emotion detection working
✅ 7 emotions tracked: angry, happy, sad, surprise, neutral, fear, disgust
✅ Color-coded visualization (each emotion has unique color)
✅ FPS counter and statistics
✅ Multiple face detection support


COMMON ISSUES & FIXES
─────────────────────

Issue: Camera not opening
Fix:   • Make sure camera is not in use by other app
       • Try: python app.py --camera 1 (different camera)
       • Check Windows camera permissions

Issue: DeepFace download errors
Fix:   • First run downloads ~350MB of models
       • Internet connection required
       • May take 2-5 minutes first time

Issue: Low FPS / Slow performance
Fix:   • Increase analysis interval: python app.py --interval 1.0
       • Close other applications
       • Check camera resolution: default is 1280x720

Issue: Poor emotion detection accuracy
Fix:   • Ensure good lighting
       • Face directly toward camera
       • Try different distance (12-24 inches ideal)


NEXT STEPS
──────────

1. Try examples.py for different integration patterns
2. Read README.md for full documentation
3. Check api.py endpoints for REST API details
4. Customize colors in config.py
5. Integrate with your application using client_library.py


FILE STRUCTURE
───────────────

app.py                 → Main real-time application
api.py                 → REST API server
emotion_detector.py    → Core detection engine
visualizer.py          → UI and visualization
client_library.py      → Reusable library for integration
examples.py            → Example use cases
config.py              → Configuration
requirements.txt       → Dependencies


SYSTEM REQUIREMENTS
────────────────────

✓ Python 3.7 or newer
✓ Webcam/USB camera
✓ 4GB+ RAM
✓ 2+ GB disk space (for models)
✓ Windows/Mac/Linux


API QUICK REFERENCE
────────────────────

Start API: python api.py

Then use these endpoints:

GET /api/emotion
  → Get current emotion and confidence

POST /api/stream/start
  → Start video streaming

GET /api/video
  → View live video stream

POST /api/analyze
  → Analyze uploaded image

GET /api/health
  → Check API status


CUSTOMIZATION
──────────────

Edit config.py to:
  • Change emotion colors
  • Adjust detection speed
  • Enable/disable emotions
  • Configure API settings


TIPS FOR BEST RESULTS
──────────────────────

1. Good lighting (natural light is best)
2. Position 12-24 inches from camera
3. Face directly toward camera
4. Clear background
5. Avoid extreme angles
6. Ensure only your face is visible (or use --enforce-detection)


TROUBLESHOOTING COMMANDS
─────────────────────────

Check Python version:
  python --version

Check installed packages:
  pip list

Reinstall requirements:
  pip install --upgrade -r requirements.txt

Clear cache and reinstall:
  pip cache purge
  pip install --upgrade tensorflow deepface


PERFORMANCE OPTIMIZATION
─────────────────────────

For real-time performance:
  • Use --interval 0.3 for faster (more CPU usage)
  • Use --interval 1.0 for slower (lower CPU usage)
  • Default is 0.5 (good balance)


INTEGRATION EXAMPLES
─────────────────────

Python:
  from emotion_detector import EmotionDetector
  detector = EmotionDetector()
  result = detector.analyze_frame(frame)

REST API:
  import requests
  r = requests.get('http://localhost:5000/api/emotion')
  emotion = r.json()['dominant_emotion']

JavaScript:
  fetch('http://localhost:5000/api/emotion')
    .then(r => r.json())
    .then(data => console.log(data.dominant_emotion))


GETTING HELP
─────────────

1. Check README.md for detailed documentation
2. Review examples.py for use cases
3. Check emotion_detector.py for API details
4. Review error messages carefully


SUCCESS INDICATORS
────────────────────

✅ Window shows "AI FACE EMOTION DETECTION" header
✅ Real-time emotion display with percentage
✅ Color-coded emotion bars update in real-time
✅ FPS counter shows 20-30 FPS
✅ Faces detected count shows correct number


HAVE FUN! 🎉
─────────────

Now that you have the system running:
  • Experiment with different expressions
  • Try the examples
  • Integrate into your applications
  • Customize colors and behavior


═══════════════════════════════════════════════════════════════

Questions? Check:
  1. README.md (full documentation)
  2. examples.py (integration patterns)
  3. Code comments (implementation details)

═══════════════════════════════════════════════════════════════
""")


# Quick command cheat sheet
CHEATSHEET = """
COMMAND CHEATSHEET
──────────────────

Basic start:
  python app.py

Start with logging:
  python app.py --save-logs

Change camera:
  python app.py --camera 1

Faster analysis:
  python app.py --interval 0.3

Start REST API:
  python api.py

Run examples:
  python examples.py

View config:
  python config.py
"""

if __name__ == "__main__":
    print(CHEATSHEET)
