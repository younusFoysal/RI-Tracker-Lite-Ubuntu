#!/usr/bin/env python3
"""
Test script to reproduce the exact issue from the description:
1. First screenshot works and uploads successfully
2. Subsequent screenshots fail with permission denied
3. Shows the blocking message about GNOME Shell permissions

This script will take multiple screenshots with delays to simulate
the app behavior and identify when/why permissions get blocked.
"""

import os
import sys
import time

# Ensure the backend package is importable when running from repo root
BASE_DIR = os.path.dirname(__file__)
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from backend.main import Api

def test_repeated_screenshots():
    """Test taking multiple screenshots to reproduce the permission issue"""
    print("TESTING REPEATED SCREENSHOTS")
    print("=" * 50)
    
    api = Api()
    
    # Test multiple screenshot attempts with delays
    for i in range(5):
        print(f"\n--- Screenshot Attempt #{i+1} ---")
        print(f"Time: {time.strftime('%H:%M:%S')}")
        
        # Check backoff status before attempt
        now = time.time()
        if api._screenshot_backoff_until and now < api._screenshot_backoff_until:
            remaining = int(api._screenshot_backoff_until - now)
            print(f"Backoff active: {remaining} seconds remaining")
            print(f"Reason: {api._screenshot_block_reason}")
        else:
            print("No backoff active")
        
        # Take screenshot
        path = api.take_screenshot()
        
        if path and os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✓ Screenshot successful: {size} bytes")
            print(f"  Path: {path}")
            print(f"  Timestamp: {api.screenshot_timestamp}")
            
            # Try to upload it
            result = api.upload_screenshot(path)
            if result:
                print(f"✓ Upload successful: {result['url']}")
            else:
                print("✗ Upload failed")
                
        else:
            print("✗ Screenshot failed")
            if api._screenshot_block_reason:
                print(f"  Block reason: {api._screenshot_block_reason}")
            if api._screenshot_backoff_until:
                remaining = int(api._screenshot_backoff_until - time.time())
                print(f"  Backoff set for: {remaining} seconds")
        
        # Check if we should continue based on backoff
        if api._screenshot_backoff_until and time.time() < api._screenshot_backoff_until:
            remaining = int(api._screenshot_backoff_until - time.time())
            print(f"\nBackoff active, waiting {min(remaining, 30)} seconds before next attempt...")
            time.sleep(min(remaining, 30))
        else:
            # Wait a bit between attempts to simulate real usage
            print("Waiting 10 seconds before next attempt...")
            time.sleep(10)

def test_permission_state():
    """Check the current permission state and environment"""
    print("CHECKING PERMISSION STATE")
    print("=" * 30)
    
    # Check environment
    session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
    display = os.environ.get('DISPLAY')
    wayland_display = os.environ.get('WAYLAND_DISPLAY')
    is_wayland = (session_type == 'wayland') or (wayland_display and not display)
    desktop_env = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
    
    print(f"Session Type: {session_type}")
    print(f"Display: {display}")
    print(f"Wayland Display: {wayland_display}")
    print(f"Is Wayland: {is_wayland}")
    print(f"Desktop Environment: {desktop_env}")
    
    # Check if gnome-screenshot is available
    import subprocess
    try:
        result = subprocess.run(['which', 'gnome-screenshot'], capture_output=True)
        if result.returncode == 0:
            gnome_path = result.stdout.decode().strip()
            print(f"gnome-screenshot: {gnome_path}")
        else:
            print("gnome-screenshot: not found")
    except Exception as e:
        print(f"Error checking gnome-screenshot: {e}")
    
    print()

if __name__ == "__main__":
    test_permission_state()
    test_repeated_screenshots()