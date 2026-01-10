"""
Simple example script to run the vehicle tracking system
Demonstrates basic usage with default settings
"""
from vehicle_tracker import VehicleTracker
import config

def main():
    """Run vehicle tracking with default configuration"""
    
    print("="*60)
    print("Vehicle Tracking & Counting System - Example")
    print("="*60)
    print()
    
    # Check if video file exists
    import os
    if not os.path.exists(config.VIDEO_INPUT):
        print(f"⚠️  Video file not found: {config.VIDEO_INPUT}")
        print()
        print("Please update config.py with your video file path, or")
        print("use the command-line interface:")
        print()
        print("  python vehicle_tracker.py --video path/to/your/video.mp4")
        print()
        return
    
    # Create tracker instance
    tracker = VehicleTracker()
    
    # Run tracking
    tracker.run()
    
    print()
    print("✓ Processing complete!")
    print(f"✓ Output saved to: {config.VIDEO_OUTPUT}")


if __name__ == "__main__":
    main()
