"""
Real-Time Vehicle Tracking using Webcam
Test the system with your webcam instead of a video file
"""
import cv2
import argparse
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
    format_time
)


class WebcamVehicleTracker:
    """Vehicle tracker for webcam input"""
    
    def __init__(self, model_path: str = None, camera_id: int = 0):
        """
        Initialize the webcam vehicle tracker
        
        Args:
            model_path: Path to YOLO model (default from config)
            camera_id: Camera device ID (0 for default webcam)
        """
        self.model_path = model_path or config.MODEL_NAME
        self.camera_id = camera_id
        
        # Initialize YOLO model
        print(f"Loading YOLO model: {self.model_path}")
        self.model = YOLO(self.model_path)
        
        # Tracking data
        self.vehicle_counts = defaultdict(int)
        self.tracked_objects = {}
        self.counted_ids = set()
        
        # Video properties
        self.cap = None
        self.frame_width = 0
        self.frame_height = 0
        
    def initialize_camera(self):
        """Initialize webcam capture"""
        print(f"\nOpening camera {self.camera_id}...")
        self.cap = cv2.VideoCapture(self.camera_id)
        
        if not self.cap.isOpened():
            raise ValueError(f"Error opening camera {self.camera_id}")
        
        # Get camera properties
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Camera resolution: {self.frame_width}x{self.frame_height}")
        
        # Set counting line at middle of frame
        self.line_coords = (0, self.frame_height // 2, self.frame_width, self.frame_height // 2)
        print(f"Counting line: {self.line_coords}\n")
    
    def process_frame(self, frame):
        """
        Process a single frame: detect, track, and count vehicles
        
        Args:
            frame: Input video frame
        
        Returns:
            Processed frame with annotations
        """
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
                
                # Check for line crossing
                if track_id in self.tracked_objects:
                    prev_center_y = self.tracked_objects[track_id]['center_y']
                    
                    # Check if crossed and not already counted
                    if (track_id not in self.counted_ids and 
                        check_line_crossing(center_y, prev_center_y, self.line_coords[1])):
                        
                        self.vehicle_counts[class_name] += 1
                        self.counted_ids.add(track_id)
                        print(f"✓ Counted: {class_name.upper()} (ID: {track_id}) - Total: {sum(self.vehicle_counts.values())}")
                
                # Update tracked object position
                self.tracked_objects[track_id] = {
                    'center_y': center_y,
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
    
    def run(self):
        """Run the webcam vehicle tracking"""
        try:
            # Initialize camera
            self.initialize_camera()
            
            print("Starting webcam vehicle tracking...")
            print("Press 'q' to quit")
            print("Press 'r' to reset counts\n")
            
            frame_count = 0
            start_time = time.time()
            
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Error reading from camera")
                    break
                
                frame_count += 1
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                # Add FPS counter
                elapsed = time.time() - start_time
                fps = frame_count / elapsed if elapsed > 0 else 0
                cv2.putText(
                    processed_frame,
                    f"FPS: {fps:.1f}",
                    (self.frame_width - 150, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )
                
                # Display frame
                cv2.imshow('Webcam Vehicle Tracking', processed_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\nStopped by user")
                    break
                elif key == ord('r'):
                    # Reset counts
                    self.vehicle_counts.clear()
                    self.counted_ids.clear()
                    print("\n✓ Counts reset")
            
            # Final statistics
            elapsed_time = time.time() - start_time
            avg_fps = frame_count / elapsed_time
            
            print("\n" + "="*50)
            print("SESSION COMPLETE")
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
            cv2.destroyAllWindows()


def main():
    """Main entry point with command-line argument parsing"""
    parser = argparse.ArgumentParser(
        description='Real-Time Vehicle Tracking using Webcam'
    )
    
    parser.add_argument(
        '--camera',
        type=int,
        default=0,
        help='Camera device ID (default: 0)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default=config.MODEL_NAME,
        help='YOLO model to use (e.g., yolo11n.pt, yolo11m.pt)'
    )
    
    parser.add_argument(
        '--conf',
        type=float,
        default=config.CONFIDENCE_THRESHOLD,
        help='Confidence threshold for detection'
    )
    
    args = parser.parse_args()
    
    # Override config with command-line arguments
    if args.conf:
        config.CONFIDENCE_THRESHOLD = args.conf
    
    # Create tracker and run
    tracker = WebcamVehicleTracker(
        model_path=args.model,
        camera_id=args.camera
    )
    
    tracker.run()


if __name__ == "__main__":
    main()
