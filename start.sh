#!/bin/bash

# Unix/Linux/Mac Startup Script for Emotion Detection

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║   AI Face Emotion Detection - Setup & Start           ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.7+ from https://www.python.org"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Check if requirements installed
python3 -c "import deepface" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "Installing dependencies (this may take a few minutes)..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    echo "✓ Dependencies installed"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "          Ready to start emotion detection!"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Choose an option:"
echo "  1 - Run real-time emotion detection app"
echo "  2 - Start REST API server"
echo "  3 - Run examples"
echo "  4 - View quick start guide"
echo "  5 - Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        clear
        echo "Starting real-time emotion detection..."
        echo ""
        python app.py
        ;;
    2)
        clear
        echo "Starting REST API server..."
        echo "Open browser at http://localhost:5000"
        echo ""
        python api.py
        ;;
    3)
        clear
        echo "Running examples..."
        echo ""
        python examples.py
        ;;
    4)
        clear
        python QUICKSTART.py
        ;;
    5)
        echo "Goodbye!"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
