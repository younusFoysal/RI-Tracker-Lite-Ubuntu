#!/usr/bin/env python3

import os
import sys
import time
import threading

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set environment to test Qt backend specifically
os.environ['WEBVIEW_GUI'] = 'qt'

def test_backend():
    try:
        import webview
        from main import Api, init_db
        
        print("Testing webview with Qt backend...")
        
        # Initialize database and API
        init_db()
        api = Api()
        
        # Create a simple test window
        window = webview.create_window(
            "Backend Test",
            "data:text/html,<html><body><h1>Backend Test</h1><p>If you see this, the Qt backend is working!</p></body></html>",
            js_api=api,
            width=400,
            height=300
        )
        
        # Set a timer to close the window after 5 seconds
        def close_window():
            time.sleep(5)
            try:
                window.destroy()
            except:
                pass
        
        timer_thread = threading.Thread(target=close_window, daemon=True)
        timer_thread.start()
        
        print("Starting webview with Qt backend...")
        webview.start(gui='qt', debug=False)
        print("Webview closed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing backend: {e}")
        return False

if __name__ == "__main__":
    success = test_backend()
    if success:
        print("✓ Qt backend test completed successfully")
        sys.exit(0)
    else:
        print("✗ Qt backend test failed")
        sys.exit(1)