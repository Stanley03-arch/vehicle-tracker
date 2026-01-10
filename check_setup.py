"""
Setup verification script for Vehicle Tracking System
Checks if all dependencies and requirements are met
"""
import sys
import os

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\nChecking dependencies...")
    required_packages = {
        'ultralytics': 'YOLO11 framework',
        'cv2': 'OpenCV (opencv-python)',
        'numpy': 'NumPy',
        'torch': 'PyTorch'
    }
    
    all_installed = True
    for package, description in required_packages.items():
        try:
            if package == 'cv2':
                import cv2
            elif package == 'ultralytics':
                import ultralytics
            elif package == 'numpy':
                import numpy
            elif package == 'torch':
                import torch
            print(f"✓ {description} - Installed")
        except ImportError:
            print(f"✗ {description} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_gpu():
    """Check if GPU is available"""
    print("\nChecking GPU availability...")
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✓ GPU Available: {gpu_name}")
            print(f"  CUDA Version: {torch.version.cuda}")
            return True
        else:
            print("⚠ GPU not available - will use CPU (slower)")
            return False
    except Exception as e:
        print(f"⚠ Could not check GPU: {e}")
        return False

def check_video_file():
    """Check if input video file exists"""
    print("\nChecking for input video...")
    import config
    
    if os.path.exists(config.VIDEO_INPUT):
        file_size = os.path.getsize(config.VIDEO_INPUT) / (1024 * 1024)  # MB
        print(f"✓ Video file found: {config.VIDEO_INPUT} ({file_size:.2f} MB)")
        return True
    else:
        print(f"✗ Video file NOT found: {config.VIDEO_INPUT}")
        print("\n  To get started, you need a traffic video file.")
        print("  You can download free traffic videos from:")
        print("    - Pexels: https://www.pexels.com/search/videos/traffic/")
        print("    - Pixabay: https://pixabay.com/videos/search/traffic/")
        print("\n  After downloading, either:")
        print(f"    1. Rename it to '{config.VIDEO_INPUT}' and place it in this directory")
        print("    2. Update VIDEO_INPUT in config.py with your video path")
        print("    3. Use command line: python vehicle_tracker.py --video your_video.mp4")
        return False

def check_model():
    """Check if YOLO model can be loaded"""
    print("\nChecking YOLO model...")
    try:
        from ultralytics import YOLO
        import config
        print(f"  Loading model: {config.MODEL_NAME}")
        model = YOLO(config.MODEL_NAME)
        print(f"✓ YOLO model loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Error loading YOLO model: {e}")
        return False

def main():
    """Run all checks"""
    print("="*60)
    print("Vehicle Tracking System - Setup Verification")
    print("="*60)
    
    checks = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "GPU": check_gpu(),
        "Video File": check_video_file(),
        "YOLO Model": check_model()
    }
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for check_name, status in checks.items():
        status_symbol = "✓" if status else "✗"
        print(f"{status_symbol} {check_name}")
    
    print("="*60)
    
    # Overall status
    critical_checks = ["Python Version", "Dependencies", "Video File"]
    if all(checks[check] for check in critical_checks):
        print("\n✓ System is ready to run!")
        print("\nTo start tracking, run:")
        print("  python vehicle_tracker.py --video input_video.mp4")
        print("\nOr use the example script:")
        print("  python run_example.py")
    else:
        print("\n✗ Please fix the issues above before running the system.")
        print("\nTo install missing dependencies:")
        print("  pip install -r requirements.txt")
    
    print()

if __name__ == "__main__":
    main()
