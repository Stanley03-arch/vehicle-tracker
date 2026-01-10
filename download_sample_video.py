"""
Download a sample traffic video for testing the vehicle tracking system
Uses multiple methods with retry logic for better reliability
"""
import os
import sys
import time

def download_with_requests(url, output_file):
    """Download using requests library with retry logic"""
    try:
        import requests
        
        print("Downloading using requests library...")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Show progress
                    if total_size > 0:
                        percent = int(downloaded * 100 / total_size)
                        downloaded_mb = downloaded / (1024 * 1024)
                        total_mb = total_size / (1024 * 1024)
                        
                        bar_length = 40
                        filled_length = int(bar_length * percent / 100)
                        bar = '█' * filled_length + '░' * (bar_length - filled_length)
                        
                        sys.stdout.write(f'\r[{bar}] {percent}% ({downloaded_mb:.1f}/{total_mb:.1f} MB)')
                        sys.stdout.flush()
        
        print()
        return True
        
    except ImportError:
        print("requests library not available, trying urllib...")
        return False
    except Exception as e:
        print(f"\nError with requests: {e}")
        return False

def download_with_urllib(url, output_file):
    """Download using urllib with better error handling"""
    try:
        import urllib.request
        import ssl
        
        print("Downloading using urllib...")
        
        # Create SSL context that doesn't verify certificates (for compatibility)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        def progress_hook(count, block_size, total_size):
            """Show download progress"""
            if total_size > 0:
                percent = int(count * block_size * 100 / total_size)
                downloaded_mb = (count * block_size) / (1024 * 1024)
                total_mb = total_size / (1024 * 1024)
                
                bar_length = 40
                filled_length = int(bar_length * percent / 100)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                
                sys.stdout.write(f'\r[{bar}] {percent}% ({downloaded_mb:.1f}/{total_mb:.1f} MB)')
                sys.stdout.flush()
        
        # Add headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            
            with open(output_file, 'wb') as f:
                downloaded = 0
                block_size = 8192
                
                while True:
                    chunk = response.read(block_size)
                    if not chunk:
                        break
                    
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Show progress
                    if total_size > 0:
                        percent = int(downloaded * 100 / total_size)
                        downloaded_mb = downloaded / (1024 * 1024)
                        total_mb = total_size / (1024 * 1024)
                        
                        bar_length = 40
                        filled_length = int(bar_length * percent / 100)
                        bar = '█' * filled_length + '░' * (bar_length - filled_length)
                        
                        sys.stdout.write(f'\r[{bar}] {percent}% ({downloaded_mb:.1f}/{total_mb:.1f} MB)')
                        sys.stdout.flush()
        
        print()
        return True
        
    except Exception as e:
        print(f"\nError with urllib: {e}")
        return False

def download_sample_video():
    """Download a sample traffic video with multiple fallback methods"""
    
    print("="*60)
    print("Sample Video Downloader")
    print("="*60)
    print()
    
    # Sample video URLs - using smaller, more reliable sources
    sample_videos = {
        "1": {
            "name": "Highway Traffic (Small - 720p)",
            "url": "https://videos.pexels.com/video-files/2103099/2103099-hd_1280_720_30fps.mp4",
            "filename": "input_video.mp4",
            "size": "~15 MB"
        },
        "2": {
            "name": "City Traffic (Medium - 1080p)",
            "url": "https://videos.pexels.com/video-files/3044127/3044127-hd_1920_1080_25fps.mp4",
            "filename": "input_video.mp4",
            "size": "~25 MB"
        }
    }
    
    print("Available sample videos:")
    print()
    for key, video in sample_videos.items():
        print(f"{key}. {video['name']} ({video['size']})")
    print()
    print("0. Cancel")
    print()
    
    choice = input("Select a video to download (1-2): ").strip()
    
    if choice == "0":
        print("Cancelled.")
        return
    
    if choice not in sample_videos:
        print("Invalid choice!")
        return
    
    video = sample_videos[choice]
    output_file = video["filename"]
    
    # Check if file already exists
    if os.path.exists(output_file):
        overwrite = input(f"\n'{output_file}' already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Cancelled.")
            return
    
    print(f"\nDownloading: {video['name']}")
    print(f"Saving to: {output_file}")
    print()
    
    # Try multiple download methods
    success = False
    
    # Method 1: Try requests library
    if not success:
        success = download_with_requests(video['url'], output_file)
    
    # Method 2: Try urllib
    if not success:
        success = download_with_urllib(video['url'], output_file)
    
    if success:
        print("\n✓ Download complete!")
        print(f"✓ Video saved to: {output_file}")
        
        # Verify file size
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024 * 1024)
            print(f"✓ File size: {file_size:.2f} MB")
        
        print()
        print("You can now run the vehicle tracker:")
        print("  python vehicle_tracker.py --video input_video.mp4")
        print()
    else:
        print("\n✗ All download methods failed.")
        print()
        print("Alternative options:")
        print()
        print("1. Install requests library and try again:")
        print("   pip install requests")
        print("   python download_sample_video.py")
        print()
        print("2. Download manually from:")
        print("   - Pexels: https://www.pexels.com/search/videos/traffic/")
        print("   - Pixabay: https://pixabay.com/videos/search/traffic/")
        print("   Save as 'input_video.mp4' in this directory")
        print()
        print("3. Use your webcam instead:")
        print("   python webcam_tracker.py")
        print()

if __name__ == "__main__":
    download_sample_video()
