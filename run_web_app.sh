#!/bin/bash

echo ""
echo "================================================================================"
echo "             🎭 AI FACE EMOTION DETECTION - Flask Web App 🎭"
echo "================================================================================"
echo ""

# Activate virtual environment
source .venv/bin/activate

echo "Starting Flask Web Server..."
echo ""
echo "📍 Access the app at: http://localhost:5000"
echo ""
echo "Instructions:"
echo "1. Open http://localhost:5000 in your browser"
echo "2. Click 'START' button to begin emotion detection"
echo "3. Grant camera permission when prompted"
echo "4. View real-time emotion analysis with statistics"
echo "5. Download JSON report when finished"
echo ""
echo "Press CTRL+C to stop the server"
echo ""
echo "================================================================================"
echo ""

python app_web.py
