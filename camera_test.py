"""
Camera Access Test
Checks if your camera is accessible and working
"""

import cv2
import sys

def test_camera_access(camera_id=0):
    """Test if camera is accessible"""
    print("=" * 60)
    print("CAMERA ACCESS TEST")
    print("=" * 60)
    print()
    
    print(f"Testing camera device: {camera_id}")
    print("-" * 60)
    
    # Try to open camera
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print("❌ FAILED: Camera could not be opened")
        print()
        print("Possible solutions:")
        print("  1. Camera is in use by another application (close it)")
        print("  2. Camera permissions denied (check Windows settings)")
        print("  3. Try different camera ID: python camera_test.py 1")
        print("  4. Camera driver issue (update camera drivers)")
        print()
        return False
    
    print("✓ Camera device opened successfully")
    print()
    
    # Get camera properties
    try:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        backend = int(cap.get(cv2.CAP_PROP_BACKEND))
        
        print("Camera Properties:")
        print(f"  Resolution: {frame_width}x{frame_height}")
        print(f"  FPS: {fps}")
        print(f"  Backend: {backend}")
        print()
    except Exception as e:
        print(f"⚠️  Could not read all properties: {e}")
        print()
    
    # Try to read frames
    print("Reading frames from camera...")
    frame_count = 0
    
    try:
        for i in range(10):
            ret, frame = cap.read()
            
            if not ret:
                print(f"❌ Failed to read frame {i+1}")
                cap.release()
                return False
            
            frame_count += 1
            print(f"  ✓ Frame {i+1} read successfully ({frame.shape[1]}x{frame.shape[0]})")
    
    except Exception as e:
        print(f"❌ Error reading frames: {e}")
        cap.release()
        return False
    
    print()
    print("=" * 60)
    print("✓ CAMERA TEST PASSED")
    print("=" * 60)
    print()
    print("Your camera is working correctly!")
    print("You can now run: python app.py")
    print()
    
    cap.release()
    return True


def test_multiple_cameras():
    """Test multiple camera devices"""
    print("=" * 60)
    print("TESTING MULTIPLE CAMERAS")
    print("=" * 60)
    print()
    
    available_cameras = []
    
    # Test cameras 0-5
    for camera_id in range(6):
        cap = cv2.VideoCapture(camera_id)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                available_cameras.append(camera_id)
                print(f"✓ Camera {camera_id} - Available (resolution: {frame.shape[1]}x{frame.shape[0]})")
            cap.release()
        else:
            print(f"✗ Camera {camera_id} - Not available")
    
    print()
    
    if available_cameras:
        print(f"Found {len(available_cameras)} available camera(s): {available_cameras}")
        print()
        if 0 not in available_cameras and available_cameras:
            print(f"⚠️  Default camera (0) not available")
            print(f"Use: python app.py --camera {available_cameras[0]}")
        return True
    else:
        print("❌ No cameras found")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        test_multiple_cameras()
    else:
        camera_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0
        test_camera_access(camera_id)
