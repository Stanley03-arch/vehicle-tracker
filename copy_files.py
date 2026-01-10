import shutil
import os

files = [
    'vehicle_tracker.py',
    'utils.py',
    'config.py',
    'web_app.html',
    'yolo11n.pt',
    'yolo11x.pt'
]

dest = 'CLOUD_DEPLOY'
os.makedirs(dest, exist_ok=True)

for f in files:
    if os.path.exists(f):
        print(f"Copying {f}...")
        shutil.copy2(f, dest)
    else:
        print(f"Warning: {f} not found")

print("Copy complete!")
