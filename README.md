# 🚗 Real-Time Vehicle Tracking & Counting System

A powerful real-time vehicle tracking and counting system built with **YOLO11**, **OpenCV**, and **Python**. This system can detect, track, and count vehicles crossing a virtual line in traffic videos.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![YOLO11](https://img.shields.io/badge/YOLO-11-green)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

✅ **Multi-Vehicle Detection**: Detects Cars, Trucks, Motorcycles, and Buses  
✅ **Real-Time Tracking**: Assigns unique IDs to each vehicle using BoT-SORT tracker  
✅ **Automated Counting**: Counts vehicles when they cross a virtual counting line  
✅ **Rich Visualizations**: Draws bounding boxes, track IDs, class names, and confidence scores  
✅ **Customizable**: Easy configuration for line position, colors, and detection parameters  
✅ **Video Output**: Saves fully annotated output video  
✅ **GPU Support**: Automatically uses GPU if CUDA is available  
✅ **Statistics Display**: Real-time counting statistics overlaid on video  

## 🎯 Demo

The system processes traffic videos and provides:
- Bounding boxes around detected vehicles
- Unique tracking IDs for each vehicle
- Class labels (Car, Truck, Bus, Motorcycle)
- Confidence scores
- Counting line visualization
- Real-time statistics (total count and per-class counts)

## 📋 Requirements

- Python 3.8 or higher
- CUDA-capable GPU (optional, but recommended for real-time performance)
- Webcam or video file for input

## 🚀 Installation

### 1. Clone or Download this Repository

```bash
cd "COMPUTER VISION CAR COUNTING MODEL"
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `ultralytics` - YOLO11 implementation
- `opencv-python` - Video processing and visualization
- `numpy` - Numerical operations
- `torch` - Deep learning backend
- `torchvision` - Vision utilities

### 4. Download YOLO11 Model

The YOLO11 model will be downloaded automatically on first run. Alternatively, you can download it manually:

```bash
# The model will be downloaded to your home directory
# Default: yolo11n.pt (nano - fastest)
# Other options: yolo11s.pt, yolo11m.pt, yolo11l.pt, yolo11x.pt
```

## 💻 Usage

### Basic Usage

```bash
python vehicle_tracker.py --video path/to/your/video.mp4
```

### Advanced Usage

```bash
# Specify output path
python vehicle_tracker.py --video input.mp4 --output results/output.mp4

# Use different YOLO model (more accurate but slower)
python vehicle_tracker.py --video input.mp4 --model yolo11m.pt

# Custom counting line position (Y coordinate in pixels)
python vehicle_tracker.py --video input.mp4 --line-y 400

# Adjust confidence threshold
python vehicle_tracker.py --video input.mp4 --conf 0.5

# Run in headless mode (no display window)
python vehicle_tracker.py --video input.mp4 --no-display
```

### Using the Example Script

```bash
# Edit config.py to set your video path, then run:
python run_example.py
```

## ⚙️ Configuration

Edit `config.py` to customize the system:

### Model Settings
```python
MODEL_NAME = "yolo11n.pt"  # Model variant
CONFIDENCE_THRESHOLD = 0.3  # Detection confidence
IOU_THRESHOLD = 0.5        # NMS threshold
```

### Counting Line Position
```python
# Option 1: Percentage of frame height (0.0 to 1.0)
COUNTING_LINE_POSITION = 0.5  # Middle of frame

# Option 2: Absolute pixel coordinates
COUNTING_LINE_COORDS = (0, 400, 1920, 400)  # (x1, y1, x2, y2)
```

### Visualization
```python
COLORS = {
    "car": (0, 255, 0),        # Green
    "truck": (255, 0, 0),      # Blue
    "bus": (0, 165, 255),      # Orange
    "motorcycle": (255, 0, 255) # Magenta
}

LINE_COLOR = (0, 255, 255)  # Yellow
LINE_THICKNESS = 3
BOX_THICKNESS = 2
```

### Video Settings
```python
VIDEO_INPUT = "input_video.mp4"
VIDEO_OUTPUT = "output_video.mp4"
RESIZE_WIDTH = None   # Set to resize (e.g., 1280)
RESIZE_HEIGHT = None  # Set to resize (e.g., 720)
```

## 📊 YOLO11 Model Variants

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| `yolo11n.pt` | 2.6 MB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Real-time, embedded systems |
| `yolo11s.pt` | 9.4 MB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Balanced performance |
| `yolo11m.pt` | 20 MB | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | High accuracy |
| `yolo11l.pt` | 25 MB | ⚡⚡ | ⭐⭐⭐⭐⭐ | Very high accuracy |
| `yolo11x.pt` | 56 MB | ⚡ | ⭐⭐⭐⭐⭐ | Maximum accuracy |

## 🎥 Sample Videos

You can test the system with free traffic videos from:

1. **Pexels**: https://www.pexels.com/search/videos/traffic/
2. **Pixabay**: https://pixabay.com/videos/search/traffic/
3. **YouTube** (use youtube-dl or similar):
   ```bash
   pip install yt-dlp
   yt-dlp -f "best[height<=720]" "VIDEO_URL" -o input_video.mp4
   ```

## 🔧 Troubleshooting

### Issue: "No module named 'ultralytics'"
**Solution**: Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Slow performance / Low FPS
**Solutions**:
- Use a smaller YOLO model (`yolo11n.pt`)
- Reduce video resolution in `config.py`
- Enable GPU support (install CUDA)
- Set `SKIP_FRAMES = 1` to process every other frame

### Issue: CUDA out of memory
**Solutions**:
- Use a smaller model
- Reduce video resolution
- Close other GPU-intensive applications

### Issue: "Error opening video file"
**Solution**: 
- Check the video path is correct
- Ensure the video format is supported (MP4, AVI, MOV)
- Try converting the video to MP4 format

## 🖥️ GPU Setup (Optional but Recommended)

### For NVIDIA GPUs:

1. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
2. Install cuDNN: https://developer.nvidia.com/cudnn
3. Install PyTorch with CUDA:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

### Verify GPU is available:
```python
import torch
print(torch.cuda.is_available())  # Should print True
```

## 📁 Project Structure

```
COMPUTER VISION CAR COUNTING MODEL/
├── vehicle_tracker.py    # Main tracking script
├── config.py            # Configuration settings
├── utils.py             # Utility functions
├── run_example.py       # Example usage script
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore patterns
├── input_video.mp4     # Your input video (not included)
└── output_video.mp4    # Generated output (after running)
```

## 🎓 How It Works

1. **Video Input**: Reads video frame by frame using OpenCV
2. **Detection**: YOLO11 detects vehicles in each frame
3. **Tracking**: BoT-SORT tracker assigns unique IDs to vehicles
4. **Filtering**: Filters detections to only vehicle classes
5. **Line Crossing**: Monitors vehicle center points crossing the counting line
6. **Counting**: Increments counter when a vehicle crosses (avoids double-counting)
7. **Visualization**: Draws bounding boxes, labels, and statistics
8. **Output**: Saves annotated video and displays real-time results

## 🚦 Vehicle Classes Detected

The system detects the following vehicle types from the COCO dataset:

- 🚗 **Car** (Class ID: 2)
- 🏍️ **Motorcycle** (Class ID: 3)
- 🚌 **Bus** (Class ID: 5)
- 🚚 **Truck** (Class ID: 7)

> **Note**: Ambulances are typically detected as cars or trucks. For specific ambulance detection, you would need to fine-tune YOLO11 on a custom dataset.

## 📈 Performance Tips

1. **Use GPU**: 10-20x faster than CPU
2. **Optimize Resolution**: Lower resolution = faster processing
3. **Choose Right Model**: Balance between speed and accuracy
4. **Skip Frames**: Process every Nth frame for faster results
5. **Batch Processing**: Process multiple videos sequentially

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open-source and available under the MIT License.

## 🙏 Acknowledgments

- **Ultralytics** for YOLO11 implementation
- **OpenCV** for computer vision tools
- **PyTorch** for deep learning framework

## 📞 Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section
2. Review the configuration in `config.py`
3. Ensure all dependencies are installed correctly

## 🎉 Example Output

After running the system, you'll see:

```
Loading YOLO model: yolo11n.pt
Video Properties:
  Resolution: 1920x1080
  FPS: 30
  Total Frames: 900
  Counting Line: (0, 540, 1920, 540)

Starting vehicle tracking and counting...
✓ Counted: CAR (ID: 5) - Total: 1
✓ Counted: TRUCK (ID: 12) - Total: 2
✓ Counted: MOTORCYCLE (ID: 8) - Total: 3
...

==================================================
PROCESSING COMPLETE
==================================================
Frames Processed: 900
Time Elapsed: 00:01:23
Average FPS: 10.84

Vehicle Counts:
------------------------------
  BUS: 3
  CAR: 45
  MOTORCYCLE: 12
  TRUCK: 8
------------------------------
  TOTAL: 68
==================================================
```

---

**Built with ❤️ using YOLO11, OpenCV, and Python**

🌟 If you find this project useful, please star the repository!
