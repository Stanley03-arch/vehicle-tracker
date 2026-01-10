"""
Auto-find the best counting line position
Runs the tracker with different line positions to find where vehicles are crossing
"""
import os
import subprocess
import re

def run_test(video_path, position_percent):
    print(f"\nTesting line at {int(position_percent*100)}% height...")
    
    # Create a temporary config override
    cmd = [
        'python', 'vehicle_tracker.py',
        '--video', video_path,
        '--line-y', str(int(1080 * position_percent)), # Assuming 1080p, but tracker handles scaling
        '--no-display',
        '--output', f'outputs/test_{int(position_percent*100)}.mp4'
    ]
    
    # Run and capture output
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Parse output for total count
    match = re.search(r'TOTAL:\s+(\d+)', result.stdout)
    if match:
        count = int(match.group(1))
        print(f"✓ Found {count} vehicles!")
        return count
    return 0

def main():
    print("="*60)
    print("🚗 FIND BEST COUNTING LINE")
    print("="*60)
    
    # Find latest video
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        print("No uploads folder found.")
        return

    videos = [f for f in os.listdir(uploads_dir) if f.endswith('.mp4')]
    if not videos:
        print("No videos found.")
        return
        
    latest_video = max([os.path.join(uploads_dir, f) for f in videos], key=os.path.getmtime)
    print(f"Analyzing video: {os.path.basename(latest_video)}")
    
    # Test positions
    positions = [0.3, 0.5, 0.7, 0.85]
    best_count = 0
    best_pos = 0.5
    
    for pos in positions:
        count = run_test(latest_video, pos)
        if count > best_count:
            best_count = count
            best_pos = pos
            
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    
    if best_count > 0:
        print(f"✅ Best line position: {int(best_pos*100)}% from top")
        print(f"✅ Vehicles counted: {best_count}")
        print(f"✅ Output saved to: outputs/test_{int(best_pos*100)}.mp4")
        
        # Update config suggestion
        print("\nTo use this permanently, update config.py:")
        print(f"COUNTING_LINE_POSITION = {best_pos}")
    else:
        print("❌ No vehicles counted with any line position.")
        print("Try adjusting CONFIDENCE_THRESHOLD in config.py (lower it)")
        print("Or check if vehicles are actually crossing the frame.")

if __name__ == "__main__":
    main()
