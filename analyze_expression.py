"""
Quick Expression Analysis Script
Runs emotion detection for a short period and generates a detailed report
"""

import cv2
import time
import json
from datetime import datetime
from emotion_detector_simple import SimplifiedEmotionDetector
from visualizer import EmotionVisualizer
from beautiful_report import BeautifulReportGenerator
from terminal_report import print_terminal_report


def analyze_expression(duration: int = 15, camera_id: int = 0):
    """
    Analyze user's expression for specified duration and generate report
    
    Args:
        duration: How many seconds to analyze (default: 15)
        camera_id: Camera device ID
    """
    
    print("\n" + "=" * 70)
    print(" " * 15 + "EXPRESSION ANALYSIS STARTED")
    print("=" * 70)
    print(f"\nAnalyzing your expression for {duration} seconds...")
    print("Please look at the camera naturally for accurate analysis.\n")
    
    # Initialize
    detector = SimplifiedEmotionDetector(analysis_interval=0.3)
    visualizer = EmotionVisualizer(detector.EMOTION_COLORS)
    
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("❌ Cannot access camera")
        return None
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # Data collection
    emotion_data = []
    start_time = time.time()
    frame_count = 0
    
    print(f"Starting capture at {datetime.now().strftime('%H:%M:%S')}\n")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            elapsed = time.time() - start_time
            
            # Analyze
            result = detector.analyze_frame(frame)
            detector.update_fps()
            frame_count += 1
            
            # Record data (with or without analysis)
            emotion_data.append({
                "timestamp": elapsed,
                "emotion": detector.dominant_emotion,
                "confidence": detector.dominant_confidence,
                "all_emotions": detector.current_emotions.copy(),
                "faces_detected": detector.faces_detected
            })
            
            # Render
            frame = visualizer.render_complete_hud(
                frame,
                emotion=detector.dominant_emotion,
                confidence=detector.dominant_confidence,
                all_emotions=detector.current_emotions,
                emotion_colors=detector.EMOTION_COLORS,
                faces_detected=detector.faces_detected,
                fps=detector.fps
            )
            
            # Add timer overlay
            timer_text = f"Time: {int(elapsed)}s / {duration}s"
            cv2.putText(frame, timer_text, (20, frame.shape[0] - 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            cv2.imshow("Expression Analysis - Press Q to skip", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Analysis skipped by user")
                break
            
            if elapsed >= duration:
                print(f"\n✅ Analysis complete!")
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    return generate_report(emotion_data, detector)


def generate_report(emotion_data, detector):
    """Generate detailed analysis report"""
    
    if not emotion_data:
        print("❌ No emotion data collected")
        return None
    
    # Display beautiful terminal report
    print_terminal_report(emotion_data, detector)
    
    # Also save to file
    save_report_to_file(emotion_data, {}, detector)
    
    return {
        "emotion_data": emotion_data,
        "statistics": {
            "total_frames": len(emotion_data),
            "dominant_emotion": detector.dominant_emotion,
        }
    }


def save_report_to_file(emotion_data, avg_scores, detector):
    """Save detailed report to JSON file"""
    
    report = {
        "analysis_timestamp": datetime.now().isoformat(),
        "duration": emotion_data[-1]["timestamp"],
        "total_frames": len(emotion_data),
        "emotion_data": emotion_data,
        "emotions_available": detector.ALL_EMOTIONS,
        "emotion_colors": detector.EMOTION_COLORS
    }
    
    filename = f"expression_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📁 Detailed report saved to: {filename}")
    
    # Generate beautiful visual report
    try:
        print("\n📊 Generating beautiful visual reports...")
        report_gen = BeautifulReportGenerator(emotion_data, detector)
        
        # Generate PNG report
        png_file = report_gen.generate_full_report()
        print(f"✅ Visual report created: {png_file}")
        
        # Generate HTML report
        html_file = report_gen.generate_html_report()
        print(f"✅ Web report created: {html_file}")
        print(f"\n💡 Open {html_file} in your browser for interactive report!")
        
    except Exception as e:
        print(f"⚠️  Could not generate visual reports: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze your facial expression")
    parser.add_argument(
        "--duration",
        type=int,
        default=15,
        help="Analysis duration in seconds (default: 15)"
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Camera ID (default: 0)"
    )
    
    args = parser.parse_args()
    
    try:
        result = analyze_expression(duration=args.duration, camera_id=args.camera)
        if result:
            print("✅ Analysis complete and saved!")
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
