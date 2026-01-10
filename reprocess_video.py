"""
Reprocess your video with improved counting
This version counts vehicles moving in BOTH directions
"""
import sys
import os

print("="*60)
print("🚗 REPROCESS VIDEO - Improved Counting")
print("="*60)
print()

# Find the uploaded video
uploads_dir = "uploads"
if os.path.exists(uploads_dir):
    videos = [f for f in os.listdir(uploads_dir) if f.endswith('.mp4')]
    if videos:
        latest_video = max([os.path.join(uploads_dir, f) for f in videos], key=os.path.getmtime)
        print(f"Found video: {os.path.basename(latest_video)}")
        print()
        
        # Ask for counting line position
        print("Where should the counting line be?")
        print("1. Top (25% from top)")
        print("2. Upper-Middle (40% from top)")
        print("3. Middle (50% - default)")
        print("4. Lower-Middle (60% from top)")
        print("5. Bottom (75% from top)")
        print()
        
        choice = input("Choice (1-5, or press Enter for middle): ").strip()
        
        line_positions = {
            "1": 0.25,
            "2": 0.40,
            "3": 0.50,
            "4": 0.60,
            "5": 0.75
        }
        
        line_pos = line_positions.get(choice, 0.50)
        
        # Update config
        import config
        config.COUNTING_LINE_POSITION = line_pos
        
        # Generate output filename
        output_file = f"outputs/reprocessed_{os.path.basename(latest_video)}"
        
        print()
        print(f"Processing with counting line at {int(line_pos*100)}% from top...")
        print()
        
        # Run the tracker
        import subprocess
        cmd = [
            'python', 'vehicle_tracker.py',
            '--video', latest_video,
            '--output', output_file
        ]
        
        subprocess.run(cmd)
        
        print()
        print("="*60)
        print("DONE!")
        print("="*60)
        print(f"Output saved to: {output_file}")
        print()
        print("Check the 'outputs' folder for your tracked video!")
        print()
    else:
        print("No videos found in uploads folder.")
        print()
        print("Please upload a video through the web interface first,")
        print("or specify the video path:")
        print()
        video_path = input("Video path: ").strip().strip('"').strip("'")
        
        if os.path.exists(video_path):
            output_file = "outputs/tracked_output.mp4"
            
            import subprocess
            cmd = [
                'python', 'vehicle_tracker.py',
                '--video', video_path,
                '--output', output_file
            ]
            
            subprocess.run(cmd)
            
            print()
            print(f"Output saved to: {output_file}")
        else:
            print(f"Video not found: {video_path}")
else:
    print("Uploads folder not found.")
    print()
    print("Please provide the path to your video:")
    video_path = input("Video path: ").strip().strip('"').strip("'")
    
    if os.path.exists(video_path):
        output_file = "outputs/tracked_output.mp4"
        
        import subprocess
        cmd = [
            'python', 'vehicle_tracker.py',
            '--video', video_path,
            '--output', output_file
        ]
        
        subprocess.run(cmd)
        
        print()
        print(f"Output saved to: {output_file}")
    else:
        print(f"Video not found: {video_path}")

input("\nPress Enter to exit...")
