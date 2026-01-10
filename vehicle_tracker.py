"""
Real-Time Vehicle Tracking & Counting System using YOLO11
Detects, tracks, and counts vehicles crossing a virtual line in video
"""
import cv2
import argparse
from pathlib import Path
from ultralytics import YOLO
import time
from collections import defaultdict

# Import configuration and utilities
import config
from utils import (
    get_center_point,
    check_line_crossing,
    draw_counting_line,
    draw_statistics,
    draw_bounding_box,
    get_counting_line_coords,
    format_time
)


class VehicleTracker:
    """Main class for vehicle tracking and counting"""
    
    def __init__(self, model_path: str = None, video_path: str = None):
        """
        Initialize the vehicle tracker
        
        Args:
            model_path: Path to YOLO model (default from config)
            video_path: Path to input video (default from config)
        """
        self.model_path = model_path or config.MODEL_NAME
        self.video_path = video_path or config.VIDEO_INPUT
        
        # Initialize YOLO model
        print(f"Loading YOLO model: {self.model_path}")
        self.model = YOLO(self.model_path)
        
        # Set device
        if config.USE_GPU:
            print("GPU enabled (if available)")
        
        # Tracking data
        self.vehicle_counts = defaultdict(int)
        self.tracked_objects = {}  # Store previous positions
        self.counted_ids = set()  # IDs that have been counted
        
        # Video properties
        self.cap = None
        self.out = None
        self.frame_width = 0
        self.frame_height = 0
        self.fps = 0
        self.total_frames = 0
        
        # Counting line coordinates
        self.line_coords = None
        
    def initialize_video(self, output_path: str = None):
        """
        Initialize video capture and writer
        
        Args:
            output_path: Path to save output video (default from config)
        """
        self.cap = cv2.VideoCapture(self.video_path)
        
        if not self.cap.isOpened():
            raise ValueError(f"Error opening video file: {self.video_path}")
        
        # Get video properties
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"\nVideo Properties:")
        print(f"  Resolution: {self.frame_width}x{self.frame_height}")
        print(f"  FPS: {self.fps}")
        print(f"  Total Frames: {self.total_frames}")
        
        # Apply resize if configured
        if config.RESIZE_WIDTH and config.RESIZE_HEIGHT:
            self.frame_width = config.RESIZE_WIDTH
            self.frame_height = config.RESIZE_HEIGHT
            print(f"  Resizing to: {self.frame_width}x{self.frame_height}")
        
        # Set counting line coordinates
        self.line_coords = get_counting_line_coords(
            self.frame_width,
            self.frame_height,
            config.COUNTING_LINE_POSITION,
            config.COUNTING_LINE_COORDS,
            config.COUNTING_LINE_ORIENTATION
        )
        print(f"  Counting Line: {self.line_coords} ({config.COUNTING_LINE_ORIENTATION})\n")
        
        # Initialize video writer
        output_path = output_path or config.VIDEO_OUTPUT
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(
            output_path,
            fourcc,
            self.fps,
            (self.frame_width, self.frame_height)
        )
        
        print(f"Output will be saved to: {output_path}\n")
    
    def process_frame(self, frame):
        """
        Process a single frame: detect, track, and count vehicles
        
        Args:
            frame: Input video frame
        
        Returns:
            Processed frame with annotations
        """
        # Resize frame if configured
        if config.RESIZE_WIDTH and config.RESIZE_HEIGHT:
            frame = cv2.resize(frame, (self.frame_width, self.frame_height))
        
        # Run YOLO tracking
        results = self.model.track(
            frame,
            persist=True,
            conf=config.CONFIDENCE_THRESHOLD,
            iou=config.IOU_THRESHOLD,
            classes=list(config.VEHICLE_CLASSES.keys()),
            verbose=False
        )
        
        # Draw counting line
        frame = draw_counting_line(
            frame,
            self.line_coords,
            config.LINE_COLOR,
            config.LINE_THICKNESS
        )
        
        # Process detections
        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            classes = results[0].boxes.cls.cpu().numpy().astype(int)
            confidences = results[0].boxes.conf.cpu().numpy()
            
            for box, track_id, cls, conf in zip(boxes, track_ids, classes, confidences):
                # Get class name
                class_name = config.VEHICLE_CLASSES.get(cls, "unknown")
                
                # Get center point
                center_x, center_y = get_center_point(box)
                
                # Determine coordinate to check based on orientation
                curr_pos = center_x if config.COUNTING_LINE_ORIENTATION == "vertical" else center_y
                line_pos = self.line_coords[0] if config.COUNTING_LINE_ORIENTATION == "vertical" else self.line_coords[1]
                
                # Check for line crossing
                if track_id in self.tracked_objects:
                    prev_pos = self.tracked_objects[track_id]['pos']
                    
                    # Check if crossed and not already counted
                    if (track_id not in self.counted_ids and 
                        check_line_crossing(curr_pos, prev_pos, line_pos)):
                        
                        self.vehicle_counts[class_name] += 1
                        self.counted_ids.add(track_id)
                        print(f"✓ Counted: {class_name.upper()} (ID: {track_id}) - Total: {sum(self.vehicle_counts.values())}")
                
                # Update tracked object position
                self.tracked_objects[track_id] = {
                    'pos': curr_pos,
                    'class': class_name
                }
                
                # Draw bounding box and label
                color = config.COLORS.get(class_name, (255, 255, 255))
                frame = draw_bounding_box(
                    frame,
                    box,
                    track_id,
                    class_name,
                    conf,
                    color,
                    config.BOX_THICKNESS,
                    config.SHOW_TRACK_ID,
                    config.SHOW_CONFIDENCE
                )
        
        # Draw statistics
        frame = draw_statistics(
            frame,
            dict(self.vehicle_counts),
            config.STATS_POSITION,
            config.FONT_SCALE,
            config.STATS_COLOR,
            config.STATS_BG_COLOR
        )
        
        return frame
    
    def run(self, output_path: str = None):
        """
        Run the vehicle tracking and counting system
        
        Args:
            output_path: Path to save output video
        """
        try:
            # Initialize video
            self.initialize_video(output_path)
            
            print("Starting vehicle tracking and counting...")
            print("Press 'q' to quit early\n")
            
            frame_count = 0
            start_time = time.time()
            
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    break
                
                frame_count += 1
                
                # Skip frames if configured
                if config.SKIP_FRAMES > 0 and frame_count % (config.SKIP_FRAMES + 1) != 0:
                    continue
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                # Write to output video
                self.out.write(processed_frame)
                
                # Display frame
                if config.DISPLAY_WINDOW:
                    cv2.imshow('Vehicle Tracking & Counting', processed_frame)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("\nStopped by user")
                        break
                
                # Print progress
                if frame_count % 30 == 0:
                    elapsed = time.time() - start_time
                    fps = frame_count / elapsed
                    progress = (frame_count / self.total_frames) * 100
                    print(f"Progress: {progress:.1f}% | Frame: {frame_count}/{self.total_frames} | FPS: {fps:.1f}")
            
            # Final statistics
            elapsed_time = time.time() - start_time
            avg_fps = frame_count / elapsed_time
            
            print("\n" + "="*50)
            print("PROCESSING COMPLETE")
            print("="*50)
            print(f"Frames Processed: {frame_count}")
            print(f"Time Elapsed: {format_time(elapsed_time)}")
            print(f"Average FPS: {avg_fps:.2f}")
            print("\nVehicle Counts:")
            print("-"*30)
            
            total = 0
            for vehicle_class in sorted(self.vehicle_counts.keys()):
                count = self.vehicle_counts[vehicle_class]
                total += count
                print(f"  {vehicle_class.upper()}: {count}")
            
            print("-"*30)
            print(f"  TOTAL: {total}")
            print("="*50)
            
        finally:
            # Cleanup
            if self.cap:
                self.cap.release()
            if self.out:
                self.out.release()
            if config.DISPLAY_WINDOW:
                cv2.destroyAllWindows()


def main():
    """Main entry point with command-line argument parsing"""
    parser = argparse.ArgumentParser(
        description='Real-Time Vehicle Tracking & Counting System using YOLO11'
    )
    
    parser.add_argument(
        '--video',
        type=str,
        default=config.VIDEO_INPUT,
        help='Path to input video file'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=config.VIDEO_OUTPUT,
        help='Path to save output video'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default=config.MODEL_NAME,
        help='YOLO model to use (e.g., yolo11n.pt, yolo11m.pt)'
    )
    
    parser.add_argument(
        '--line-y',
        type=int,
        default=None,
        help='Y coordinate for counting line (overrides config)'
    )
    
    parser.add_argument(
        '--no-display',
        action='store_true',
        help='Run without displaying video window (headless mode)'
    )
    
    parser.add_argument(
        '--conf',
        type=float,
        default=config.CONFIDENCE_THRESHOLD,
        help='Confidence threshold for detection'
    )
    
    args = parser.parse_args()
    
    # Override config with command-line arguments
    if args.line_y:
        config.COUNTING_LINE_COORDS = (0, args.line_y, 10000, args.line_y)
    
    if args.no_display:
        config.DISPLAY_WINDOW = False
    
    if args.conf:
        config.CONFIDENCE_THRESHOLD = args.conf
    
    # Create tracker and run
    tracker = VehicleTracker(
        model_path=args.model,
        video_path=args.video
    )
    
    tracker.run(output_path=args.output)


if __name__ == "__main__":
    main()
