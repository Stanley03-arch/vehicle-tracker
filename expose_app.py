"""
Expose your Vehicle Tracking App to the World!
This script uses ngrok to create a secure public URL for your local app.
"""
import os
import sys
import time
import subprocess
import requests
from pyngrok import ngrok, conf

# Configuration
PORT = 5000
NGROK_AUTH_TOKEN = "385K50ePiypjGMgv99PLceXtFng_695AzpGYQbQufk5nbf1AC"

def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def main():
    print("="*60)
    print("🌍 DEPLOYING VEHICLE TRACKER TO THE WEB")
    print("="*60)
    print()

    # 1. Start the Web App if not running
    if not is_port_in_use(PORT):
        print(f"Starting local web server on port {PORT}...")
        # Start web_app.py in a separate process
        subprocess.Popen([sys.executable, 'web_app.py'], 
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        # Wait for it to start
        print("Waiting for server to initialize...")
        for _ in range(10):
            if is_port_in_use(PORT):
                break
            time.sleep(1)
    else:
        print(f"✅ Local server is already running on port {PORT}")

    # 2. Connect ngrok
    print("\nCreating public tunnel...")
    try:
        # Set auth token
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)
        
        # Open a HTTP tunnel on the default port 5000
        public_url = ngrok.connect(PORT).public_url
        
        print("\n" + "="*60)
        print("🎉 YOUR APP IS LIVE!")
        print("="*60)
        print(f"\nPublic URL: {public_url}")
        print("\nShare this link with anyone! They can upload videos")
        print("and your computer will process them.")
        print("\nPress Ctrl+C to stop sharing.")
        print("="*60)

        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down tunnel...")
            ngrok.kill()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNote: You may need to sign up for a free ngrok account.")
        print("If asked for an authtoken, run:")
        print("ngrok config add-authtoken YOUR_TOKEN")
        print("Get it here: https://dashboard.ngrok.com/get-started/your-authtoken")

if __name__ == "__main__":
    main()
