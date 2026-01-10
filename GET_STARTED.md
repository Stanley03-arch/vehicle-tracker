# 🚀 GET STARTED NOW!

## The Fastest Way to Run This System

### Option 1: One-Click Setup (Recommended)
```bash
python setup_and_run.py
```
This script will:
- ✓ Check all dependencies
- ✓ Test your webcam
- ✓ Download a sample video (if needed)
- ✓ Run the tracker automatically

---

### Option 2: Use Your Webcam (No Video Needed!)
```bash
python webcam_tracker.py
```
**Controls:**
- Press `q` to quit
- Press `r` to reset counts

---

### Option 3: Download Sample Video
```bash
python download_sample_video.py
```
Then run:
```bash
python vehicle_tracker.py --video input_video.mp4
```

---

## 🔧 If You Get Errors

### "No module named 'ultralytics'" or similar
```bash
pip install -r requirements.txt
```

### "Video file NOT found"
**Solution 1:** Use webcam instead
```bash
python webcam_tracker.py
```

**Solution 2:** Download a video manually
1. Go to https://www.pexels.com/search/videos/traffic/
2. Download any traffic video
3. Save it as `input_video.mp4` in this folder
4. Run: `python vehicle_tracker.py --video input_video.mp4`

---

## 📊 What You'll See

The system will show:
- 🎥 Real-time video with bounding boxes
- 🔢 Unique IDs for each vehicle
- 📈 Live counting statistics
- 📏 Counting line visualization
- 🚗 Vehicle types (Car, Truck, Bus, Motorcycle)

---

## 🎯 Quick Commands

| Command | What It Does |
|---------|-------------|
| `python setup_and_run.py` | One-click setup and run |
| `python webcam_tracker.py` | Use webcam (no video needed) |
| `python check_setup.py` | Verify installation |
| `python download_sample_video.py` | Download sample video |
| `python vehicle_tracker.py --video FILE.mp4` | Process a video file |

---

## 💡 Pro Tips

1. **Fastest Start**: Run `python webcam_tracker.py` - no video download needed!
2. **Better Accuracy**: Use `--model yolo11m.pt` for more accurate detection
3. **Faster Speed**: Use `--model yolo11n.pt` for faster processing
4. **Custom Video**: `python vehicle_tracker.py --video YOUR_VIDEO.mp4`

---

## 📖 Full Documentation

For complete documentation, see:
- [QUICKSTART.md](QUICKSTART.md) - Detailed quick start guide
- [README.md](README.md) - Complete documentation

---

**Need Help?** Run `python check_setup.py` to diagnose any issues!

🌟 **Ready to go?** Just run: `python setup_and_run.py`
