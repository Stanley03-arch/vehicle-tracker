"""
One-Click Setup and Test Script
This script will set up everything and test the vehicle tracking system
"""
import os
import sys
import subprocess

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(text)
    print("="*60)

def run_command(cmd, description):
    """Run a command and show the result"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} - Success")
            return True
        else:
            print(f"✗ {description} - Failed")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"✗ {description} - Error: {e}")
        return False

def check_dependencies():
    """Check if all dependencies are installed"""
    print_header("Step 1: Checking Dependencies")
    
    required = ['ultralytics', 'cv2', 'numpy', 'torch']
    missing = []
    
    for package in required:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'ultralytics':
                import ultralytics
            elif package == 'numpy':
                import numpy
            elif package == 'torch':
                import torch
            print(f"✓ {package} - Installed")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print("\n⚠ Missing dependencies detected!")
        install = input("\nInstall missing dependencies now? (y/n): ").strip().lower()
        if install == 'y':
            print("\nInstalling dependencies...")
            run_command("pip install -r requirements.txt", "Installing packages")
        else:
            print("Cannot proceed without dependencies.")
            return False
    
    return True

def test_webcam():
    """Test if webcam is available"""
    print_header("Step 2: Testing Webcam")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✓ Webcam is available and working")
                return True
            else:
                print("⚠ Webcam detected but cannot read frames")
                return False
        else:
            print("⚠ No webcam detected")
            return False
    except Exception as e:
        print(f"⚠ Error testing webcam: {e}")
        return False

def check_video_file():
    """Check if video file exists"""
    print_header("Step 3: Checking for Video File")
    
    if os.path.exists("input_video.mp4"):
        file_size = os.path.getsize("input_video.mp4") / (1024 * 1024)
        print(f"✓ Video file found: input_video.mp4 ({file_size:.2f} MB)")
        return True
    else:
        print("✗ No video file found")
        return False

def download_video():
    """Attempt to download a sample video"""
    print_header("Step 4: Downloading Sample Video")
    
    print("\nAttempting to download a sample traffic video...")
    print("This may take a few minutes depending on your connection.\n")
    
    # Try to install requests first
    try:
        import requests
    except ImportError:
        print("Installing requests library for better downloads...")
        run_command("pip install requests", "Installing requests")
    
    # Run the download script
    try:
        # Use a simple approach - download directly
        import urllib.request
        import ssl
        
        url = "https://videos.pexels.com/video-files/2103099/2103099-hd_1280_720_30fps.mp4"
        output = "input_video.mp4"
        
        print("Downloading from Pexels...")
        print("URL: Highway Traffic Video (720p)")
        
        # Create SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Add headers
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        # Download with progress
        with urllib.request.urlopen(req, context=ssl_context, timeout=60) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            
            with open(output, 'wb') as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        percent = int(downloaded * 100 / total_size)
                        sys.stdout.write(f'\rProgress: {percent}% ({downloaded/(1024*1024):.1f}/{total_size/(1024*1024):.1f} MB)')
                        sys.stdout.flush()
        
        print("\n✓ Download complete!")
        return True
        
    except Exception as e:
        print(f"\n✗ Download failed: {e}")
        return False

def run_tracker(use_webcam=False):
    """Run the vehicle tracker"""
    print_header("Step 5: Running Vehicle Tracker")
    
    if use_webcam:
        print("\nStarting webcam tracker...")
        print("Press 'q' to quit\n")
        os.system("python webcam_tracker.py")
    else:
        print("\nStarting video tracker...")
        print("Press 'q' to quit\n")
        os.system("python vehicle_tracker.py --video input_video.mp4")

def main():
    """Main setup and test flow"""
    print_header("🚗 Vehicle Tracking System - One-Click Setup")
    
    print("\nThis script will:")
    print("1. Check and install dependencies")
    print("2. Test your webcam")
    print("3. Download a sample video (if needed)")
    print("4. Run the vehicle tracker")
    
    input("\nPress Enter to continue...")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Setup failed - dependencies not installed")
        return
    
    # Step 2: Test webcam
    has_webcam = test_webcam()
    
    # Step 3: Check for video file
    has_video = check_video_file()
    
    # Step 4: If no video, try to download
    if not has_video:
        print("\n⚠ No video file found.")
        
        if has_webcam:
            choice = input("\nOptions:\n1. Download sample video\n2. Use webcam\n3. Exit\n\nChoice (1-3): ").strip()
            
            if choice == "1":
                has_video = download_video()
            elif choice == "2":
                run_tracker(use_webcam=True)
                return
            else:
                print("\nExiting. To run later:")
                print("  - With video: python vehicle_tracker.py --video input_video.mp4")
                print("  - With webcam: python webcam_tracker.py")
                return
        else:
            download = input("\nDownload sample video? (y/n): ").strip().lower()
            if download == 'y':
                has_video = download_video()
            else:
                print("\nCannot proceed without video or webcam.")
                print("\nManual options:")
                print("1. Download a video from: https://www.pexels.com/search/videos/traffic/")
                print("2. Save it as 'input_video.mp4' in this directory")
                print("3. Run: python vehicle_tracker.py --video input_video.mp4")
                return
    
    # Step 5: Run the tracker
    if has_video:
        print("\n✓ All checks passed! Ready to run.")
        
        run_choice = input("\nRun tracker now? (y/n): ").strip().lower()
        if run_choice == 'y':
            run_tracker(use_webcam=False)
        else:
            print("\nSetup complete! To run later:")
            print("  python vehicle_tracker.py --video input_video.mp4")
    elif has_webcam:
        run_tracker(use_webcam=True)
    else:
        print("\n⚠ Setup incomplete. Please get a video file or webcam.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Setup cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
