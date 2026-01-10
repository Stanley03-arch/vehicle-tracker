"""
Configuration file for Vehicle Tracking and Counting System
Customize these settings based on your requirements
"""

# YOLO Model Configuration
MODEL_NAME = "yolo11x.pt"  # Using Extra Large model for maximum accuracy
CONFIDENCE_THRESHOLD = 0.25  # Lower threshold to catch more vehicles
IOU_THRESHOLD = 0.5  # IoU threshold for NMS

# Vehicle Classes (COCO dataset class IDs)
VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle", 
    5: "bus",
    7: "truck"
}

# Counting Line Configuration
# Orientation: "horizontal" (for up/down traffic) or "vertical" (for left/right traffic)
COUNTING_LINE_ORIENTATION = "vertical"

# Line position as percentage of frame size (0.0 to 1.0)
# For horizontal: percentage of height (0.5 = middle height)
# For vertical: percentage of width (0.5 = middle width)
COUNTING_LINE_POSITION = 0.5  

# Or use absolute pixel coordinates (will override percentage if not None)
# Format: (x1, y1, x2, y2)
COUNTING_LINE_COORDS = None

# Visualization Settings
COLORS = {
    "car": (0, 255, 0),        # Green
    "truck": (255, 0, 0),      # Blue
    "bus": (0, 165, 255),      # Orange
    "motorcycle": (255, 0, 255) # Magenta
}

LINE_COLOR = (0, 255, 255)     # Yellow for counting line
LINE_THICKNESS = 3
BOX_THICKNESS = 2
FONT_SCALE = 0.6
FONT_THICKNESS = 2

# Display Settings
SHOW_CONFIDENCE = True
SHOW_TRACK_ID = True
SHOW_CLASS_NAME = True
DISPLAY_WINDOW = True  # Set to False for headless mode

# Video Settings
VIDEO_INPUT = "input_video.mp4"  # Path to input video
VIDEO_OUTPUT = "output_video.mp4"  # Path to save output video
RESIZE_WIDTH = None  # Set to resize video width (None = original size)
RESIZE_HEIGHT = None  # Set to resize video height (None = original size)

# Performance Settings
SKIP_FRAMES = 0  # Process every Nth frame (0 = process all frames)
USE_GPU = True  # Use GPU if available

# Statistics Display
STATS_POSITION = (10, 30)  # Position for statistics text
STATS_COLOR = (255, 255, 255)  # White
STATS_BG_COLOR = (0, 0, 0)  # Black background
