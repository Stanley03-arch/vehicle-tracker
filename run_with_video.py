"""
Quick Video Tracker - Use your downloaded video
Just drag and drop your video file path when prompted
"""
import os
import sys

print("="*60)
print("🚗 QUICK VIDEO TRACKER")
print("="*60)
print()

# Check if video path was provided as argument
if len(sys.argv) > 1:
    video_path = sys.argv[1]
else:
    print("Enter the path to your video file:")
    print("(You can drag and drop the file here)")
    print()
    video_path = input("Video path: ").strip()
    
    # Remove quotes if present
    video_path = video_path.strip('"').strip("'")

# Check if file exists
if not os.path.exists(video_path):
    print(f"\n❌ Error: Video file not found: {video_path}")
    print()
    print("Please check:")
    print("1. The file path is correct")
    print("2. The file exists")
    print("3. You have permission to access it")
    print()
    input("Press Enter to exit...")
    sys.exit(1)

# Get file size
file_size = os.path.getsize(video_path) / (1024 * 1024)
print(f"\n✓ Video file found: {os.path.basename(video_path)}")
print(f"✓ File size: {file_size:.2f} MB")
print()

# Ask for output path
output_path = input("Output file name (press Enter for 'output_video.mp4'): ").strip()
if not output_path:
    output_path = "output_video.mp4"

print()
print("="*60)
print("STARTING VEHICLE TRACKER")
print("="*60)
print()
print("Settings:")
print(f"  Input:  {video_path}")
print(f"  Output: {output_path}")
print()
print("Press 'q' during playback to stop early")
print()

# Run the tracker
import subprocess
cmd = f'python vehicle_tracker.py --video "{video_path}" --output "{output_path}"'
subprocess.run(cmd, shell=True)

print()
print("="*60)
print("DONE!")
print("="*60)
print(f"Check your output video: {output_path}")
print()
