"""
Utility functions for vehicle tracking and counting system
"""
import cv2
import numpy as np
from typing import Tuple, Dict


def get_center_point(bbox: Tuple[int, int, int, int]) -> Tuple[int, int]:
    """
    Calculate the center point of a bounding box
    
    Args:
        bbox: Bounding box coordinates (x1, y1, x2, y2)
    
    Returns:
        Tuple of (center_x, center_y)
    """
    x1, y1, x2, y2 = bbox
    center_x = int((x1 + x2) / 2)
    center_y = int((y1 + y2) / 2)
    return center_x, center_y


def check_line_crossing(
    curr_pos: int,
    prev_pos: int,
    line_pos: int,
    margin: int = 5
) -> bool:
    """
    Check if an object has crossed the counting line
    
    Args:
        curr_pos: Current coordinate (X or Y)
        prev_pos: Previous coordinate (X or Y)
        line_pos: Coordinate of counting line
        margin: Margin of error for line crossing
    
    Returns:
        True if object crossed the line (in either direction)
    """
    # Check crossing in positive direction (e.g., left to right or top to bottom)
    if prev_pos < line_pos - margin and curr_pos >= line_pos + margin:
        return True
    
    # Check crossing in negative direction (e.g., right to left or bottom to top)
    if prev_pos > line_pos + margin and curr_pos <= line_pos - margin:
        return True
    
    return False


def draw_counting_line(
    frame: np.ndarray,
    line_coords: Tuple[int, int, int, int],
    color: Tuple[int, int, int],
    thickness: int
) -> np.ndarray:
    """
    Draw the counting line on the frame
    
    Args:
        frame: Video frame
        line_coords: Line coordinates (x1, y1, x2, y2)
        color: Line color (B, G, R)
        thickness: Line thickness
    
    Returns:
        Frame with line drawn
    """
    x1, y1, x2, y2 = line_coords
    cv2.line(frame, (x1, y1), (x2, y2), color, thickness)
    
    # Add text label for the line
    cv2.putText(
        frame,
        "COUNTING LINE",
        (x1 + 10, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )
    
    return frame


def draw_statistics(
    frame: np.ndarray,
    counts: Dict[str, int],
    position: Tuple[int, int],
    font_scale: float = 0.8,
    color: Tuple[int, int, int] = (255, 255, 255),
    bg_color: Tuple[int, int, int] = (0, 0, 0)
) -> np.ndarray:
    """
    Draw counting statistics on the frame
    
    Args:
        frame: Video frame
        counts: Dictionary of vehicle counts by class
        position: Position to draw statistics (x, y)
        font_scale: Font scale
        color: Text color
        bg_color: Background color
    
    Returns:
        Frame with statistics drawn
    """
    x, y = position
    line_height = 30
    
    # Draw background rectangle
    total_lines = len(counts) + 1
    cv2.rectangle(
        frame,
        (x - 5, y - 25),
        (x + 250, y + line_height * total_lines + 5),
        bg_color,
        -1
    )
    
    # Draw total count
    total = sum(counts.values())
    cv2.putText(
        frame,
        f"TOTAL: {total}",
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (0, 255, 255),  # Yellow for total
        2
    )
    
    # Draw individual class counts
    y_offset = y + line_height
    for vehicle_class, count in counts.items():
        cv2.putText(
            frame,
            f"{vehicle_class.upper()}: {count}",
            (x, y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            color,
            2
        )
        y_offset += line_height
    
    return frame


def draw_bounding_box(
    frame: np.ndarray,
    bbox: Tuple[int, int, int, int],
    track_id: int,
    class_name: str,
    confidence: float,
    color: Tuple[int, int, int],
    thickness: int = 2,
    show_id: bool = True,
    show_confidence: bool = True
) -> np.ndarray:
    """
    Draw bounding box with label on the frame
    
    Args:
        frame: Video frame
        bbox: Bounding box coordinates (x1, y1, x2, y2)
        track_id: Tracking ID
        class_name: Class name
        confidence: Detection confidence
        color: Box color
        thickness: Box thickness
        show_id: Whether to show track ID
        show_confidence: Whether to show confidence score
    
    Returns:
        Frame with bounding box drawn
    """
    x1, y1, x2, y2 = bbox
    
    # Draw bounding box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
    
    # Prepare label text
    label_parts = [class_name]
    if show_id:
        label_parts.append(f"ID:{track_id}")
    if show_confidence:
        label_parts.append(f"{confidence:.2f}")
    
    label = " | ".join(label_parts)
    
    # Calculate label size
    (label_width, label_height), baseline = cv2.getTextSize(
        label,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        2
    )
    
    # Draw label background
    cv2.rectangle(
        frame,
        (x1, y1 - label_height - baseline - 5),
        (x1 + label_width + 5, y1),
        color,
        -1
    )
    
    # Draw label text
    cv2.putText(
        frame,
        label,
        (x1 + 2, y1 - baseline - 2),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 0, 0),  # Black text
        2
    )
    
    # Draw center point
    center_x, center_y = get_center_point(bbox)
    cv2.circle(frame, (center_x, center_y), 4, color, -1)
    
    return frame


def format_time(seconds: float) -> str:
    """
    Format elapsed time in seconds to HH:MM:SS format
    
    Args:
        seconds: Time in seconds
    
    Returns:
        Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def get_counting_line_coords(
    frame_width: int,
    frame_height: int,
    line_position: float = 0.5,
    custom_coords: Tuple[int, int, int, int] = None,
    orientation: str = "horizontal"
) -> Tuple[int, int, int, int]:
    """
    Get counting line coordinates based on frame dimensions
    
    Args:
        frame_width: Width of video frame
        frame_height: Height of video frame
        line_position: Position as percentage (0.0 to 1.0)
        custom_coords: Custom line coordinates (overrides line_position)
        orientation: "horizontal" or "vertical"
    
    Returns:
        Line coordinates (x1, y1, x2, y2)
    """
    if custom_coords is not None:
        return custom_coords
    
    if orientation == "vertical":
        line_x = int(frame_width * line_position)
        return (line_x, 0, line_x, frame_height)
    else:
        line_y = int(frame_height * line_position)
        return (0, line_y, frame_width, line_y)
