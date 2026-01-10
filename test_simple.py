"""
Simple test to identify and fix issues
"""
import sys
import os

print("="*60)
print("SIMPLE DIAGNOSTIC TEST")
print("="*60)

# Test 1: Python version
print("\n1. Python Version:")
print(f"   {sys.version}")

# Test 2: Import dependencies
print("\n2. Testing Imports:")
try:
    import cv2
    print("   ✓ OpenCV imported")
    print(f"     Version: {cv2.__version__}")
except Exception as e:
    print(f"   ✗ OpenCV error: {e}")

try:
    import numpy as np
    print("   ✓ NumPy imported")
    print(f"     Version: {np.__version__}")
except Exception as e:
    print(f"   ✗ NumPy error: {e}")

try:
    import torch
    print("   ✓ PyTorch imported")
    print(f"     Version: {torch.__version__}")
    print(f"     CUDA available: {torch.cuda.is_available()}")
except Exception as e:
    print(f"   ✗ PyTorch error: {e}")

try:
    from ultralytics import YOLO
    print("   ✓ Ultralytics imported")
except Exception as e:
    print(f"   ✗ Ultralytics error: {e}")

# Test 3: Check config
print("\n3. Testing Config:")
try:
    import config
    print("   ✓ Config imported")
    print(f"     Model: {config.MODEL_NAME}")
    print(f"     Video input: {config.VIDEO_INPUT}")
except Exception as e:
    print(f"   ✗ Config error: {e}")

# Test 4: Check utils
print("\n4. Testing Utils:")
try:
    from utils import get_center_point, draw_counting_line
    print("   ✓ Utils imported")
except Exception as e:
    print(f"   ✗ Utils error: {e}")

# Test 5: Test webcam
print("\n5. Testing Webcam:")
try:
    import cv2
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        cap.release()
        if ret:
            print("   ✓ Webcam working")
            print(f"     Frame shape: {frame.shape}")
        else:
            print("   ⚠ Webcam opened but can't read frames")
    else:
        print("   ⚠ No webcam detected")
except Exception as e:
    print(f"   ✗ Webcam error: {e}")

# Test 6: Test YOLO model loading
print("\n6. Testing YOLO Model:")
try:
    from ultralytics import YOLO
    import config
    print(f"   Loading {config.MODEL_NAME}...")
    model = YOLO(config.MODEL_NAME)
    print("   ✓ YOLO model loaded successfully")
except Exception as e:
    print(f"   ✗ YOLO model error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("DIAGNOSTIC COMPLETE")
print("="*60)

# Provide recommendations
print("\nRECOMMENDATIONS:")
print("- If all tests passed: Run 'python webcam_tracker.py'")
print("- If webcam failed: Download a video and use video mode")
print("- If imports failed: Run 'pip install -r requirements.txt'")
print()
