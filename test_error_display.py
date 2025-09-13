import webview
import sys
import os
import time

# Add the backend directory to the path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(backend_path)

# Import the Api class from main.py
from backend.main import Api

class TestApi(Api):
    def create_session(self):
        """Override create_session to simulate a long error message"""
        # Simulate a delay
        time.sleep(1)
        
        # Return a long error message
        window.evaluate_js('window.toastFromPython("Failed to create session with a very long error message!", "error")')
        return {
            "success": False, 
            "message": "Employee already has an active session. Please stop the current session before starting a new one. Active session ID: jhbasuydgfbyus6854657234jbhj"
        }

# Create an instance of the TestApi class
api = TestApi()

# Create a window
window = webview.create_window('Test Error Display', 'frontend/dist/index.html', js_api=api)

# Start the webview
webview.start(debug=True)