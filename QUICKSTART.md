# 🚀 Quick Start Guide

## Get the System Running in 3 Steps!

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get a Video File

**Option A: Download a Sample Video (Easiest)**
```bash
python download_sample_video.py
```
This will download a free traffic video from Pexels.

**Option B: Use Your Webcam (No video needed!)**
```bash
python webcam_tracker.py
```

**Option C: Use Your Own Video**
- Download a traffic video from [Pexels](https://www.pexels.com/search/videos/traffic/) or [Pixabay](https://pixabay.com/videos/search/traffic/)
- Save it as `input_video.mp4` in this directory

### Step 3: Run the Tracker

**For Video Files:**
```bash
python vehicle_tracker.py --video input_video.mp4
```

**For Webcam:**
```bash
python webcam_tracker.py
```

---

## 🔍 Verify Your Setup

Run the setup checker to ensure everything is installed correctly:
```bash
python check_setup.py
```

This will check:
- ✓ Python version
- ✓ All dependencies
- ✓ GPU availability
- ✓ Video file
- ✓ YOLO model

---

## 📝 What You'll See

When running the tracker, you'll see:
- **Real-time video** with bounding boxes around vehicles
- **Unique IDs** for each tracked vehicle
- **Vehicle counts** displayed on screen
- **Counting line** showing where vehicles are counted
- **Statistics** showing total counts by vehicle type

Example output:
```
✓ Counted: CAR (ID: 5) - Total: 1
✓ Counted: TRUCK (ID: 12) - Total: 2
✓ Counted: MOTORCYCLE (ID: 8) - Total: 3

Progress: 45.2% | Frame: 406/900 | FPS: 12.3
```

---

## ⚙️ Common Commands

### Basic Usage
```bash
# Use default settings
python vehicle_tracker.py --video input_video.mp4

# Specify output file
python vehicle_tracker.py --video input.mp4 --output results.mp4

# Use different model (more accurate but slower)
python vehicle_tracker.py --video input.mp4 --model yolo11m.pt

# Adjust confidence threshold
python vehicle_tracker.py --video input.mp4 --conf 0.5

# Run without display window (headless)
python vehicle_tracker.py --video input.mp4 --no-display
```

### Webcam Usage
```bash
# Use default webcam
python webcam_tracker.py

# Use specific camera (if you have multiple)
python webcam_tracker.py --camera 1

# Use different model
python webcam_tracker.py --model yolo11s.pt
```

---

## 🎮 Keyboard Controls

When running the tracker:
- **`q`** - Quit the application
- **`r`** - Reset counts (webcam mode only)

---

## 🐛 Troubleshooting

### "No module named 'ultralytics'"
**Solution:**
```bash
pip install -r requirements.txt
```

### "Video file NOT found"
**Solution:**
```bash
# Download a sample video
python download_sample_video.py

# OR use webcam instead
python webcam_tracker.py
```

### Slow Performance / Low FPS
**Solutions:**
- Use a smaller model: `--model yolo11n.pt`
- Reduce video resolution in `config.py`
- Process fewer frames: Set `SKIP_FRAMES = 1` in `config.py`

### "Error opening camera"
**Solution:**
- Check if your webcam is connected
- Try a different camera ID: `--camera 1`
- Make sure no other app is using the webcam

---

## 📊 Model Comparison

| Model | Speed | Accuracy | Best For |
|-------|-------|----------|----------|
| `yolo11n.pt` | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Real-time, webcam |
| `yolo11s.pt` | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Balanced |
| `yolo11m.pt` | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | High accuracy |

---

## 🎯 Next Steps

1. **Test with sample video**: `python download_sample_video.py`
2. **Try webcam mode**: `python webcam_tracker.py`
3. **Customize settings**: Edit `config.py` to adjust colors, line position, etc.
4. **Use your own videos**: Process your own traffic footage

---

## 💡 Tips

- **GPU**: If you have an NVIDIA GPU, the system will automatically use it for faster processing
- **Line Position**: Adjust `COUNTING_LINE_POSITION` in `config.py` to change where vehicles are counted
- **Colors**: Customize vehicle colors in `config.py` under `COLORS`
- **Confidence**: Lower `CONFIDENCE_THRESHOLD` to detect more vehicles (may include false positives)

---

## 📚 Full Documentation

For complete documentation, see [README.md](README.md)

---

**Built with ❤️ using YOLO11, OpenCV, and Python**

Need help? Run `python check_setup.py` to diagnose issues!
