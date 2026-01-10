"""
Flask Web Application for Vehicle Tracking
Allows drag-and-drop video upload and processing through a web interface
"""
from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import os
import subprocess
import threading
import time
from pathlib import Path

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'}

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB max file size

# Global variable to track processing status
processing_status = {
    'status': 'idle',
    'progress': 0,
    'message': '',
    'output_file': None
}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_video_background(input_path, output_path):
    """Process video in background thread"""
    global processing_status
    
    try:
        processing_status['status'] = 'processing'
        processing_status['progress'] = 0
        processing_status['message'] = 'Starting video processing...'
        
        # Run the vehicle tracker with unbuffered output (-u)
        cmd = [
            'python', '-u', 'vehicle_tracker.py',
            '--video', input_path,
            '--output', output_path,
            '--no-display'
        ]
        
        # Use Popen to capture output in real-time
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Read output line by line
        for line in process.stdout:
            if "Progress:" in line:
                try:
                    # Parse "Progress: 45.2% | ..."
                    parts = line.split('|')[0]
                    percent_str = parts.split(':')[1].strip().replace('%', '')
                    percent = float(percent_str)
                    processing_status['progress'] = percent
                    processing_status['message'] = f'Processing: {percent:.1f}%'
                except:
                    pass
        
        # Wait for process to complete
        process.wait()
        
        if process.returncode == 0:
            processing_status['status'] = 'complete'
            processing_status['progress'] = 100
            processing_status['message'] = 'Processing complete!'
            processing_status['output_file'] = os.path.basename(output_path)
        else:
            stderr_output = process.stderr.read()
            processing_status['status'] = 'error'
            processing_status['message'] = f'Error: {stderr_output[:200]}'
            
    except Exception as e:
        processing_status['status'] = 'error'
        processing_status['message'] = f'Error: {str(e)}'

@app.route('/')
def index():
    """Serve the main page"""
    return send_file('web_app.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    global processing_status
    
    # Reset status
    processing_status = {
        'status': 'idle',
        'progress': 0,
        'message': '',
        'output_file': None
    }
    
    if 'video' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a video file.'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = int(time.time())
        input_filename = f"{timestamp}_{filename}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        file.save(input_path)
        
        # Generate output filename
        output_filename = f"tracked_{input_filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Start processing in background thread
        thread = threading.Thread(
            target=process_video_background,
            args=(input_path, output_path)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully. Processing started.',
            'filename': input_filename
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def get_status():
    """Get current processing status"""
    return jsonify(processing_status)

@app.route('/download/<filename>')
def download_file(filename):
    """Download processed video"""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    print("="*60)
    print("🚗 Vehicle Tracking Web Application")
    print("="*60)
    print()
    print("Starting server...")
    print("Open your browser and go to: http://localhost:5000")
    print()
    print("Press Ctrl+C to stop the server")
    print("="*60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
