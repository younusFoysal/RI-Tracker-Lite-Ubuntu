#!/usr/bin/env python3
"""
Test script to verify that all required dependencies can be imported successfully.
This helps ensure the requirements.txt file contains all necessary packages.
"""

import sys
import importlib

# List of core modules that should be importable
required_modules = [
    'webview',
    'requests', 
    'mss',
    'psutil',
    'pynput',
    'tzlocal',
    'screeninfo',
    'bottle'
]

# Optional modules (may not be available on all systems)
optional_modules = [
    'gi',  # PyGObject for GTK backend
    'PyQt5',  # Qt backend
    'pyinstaller'  # For building executables
]

def test_imports():
    """Test importing all required and optional modules."""
    print("Testing required module imports...")
    failed_required = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module} - OK")
        except ImportError as e:
            print(f"✗ {module} - FAILED: {e}")
            failed_required.append(module)
    
    print("\nTesting optional module imports...")
    failed_optional = []
    
    for module in optional_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module} - OK")
        except ImportError as e:
            print(f"~ {module} - Not available: {e}")
            failed_optional.append(module)
    
    print("\n" + "="*50)
    print("IMPORT TEST RESULTS")
    print("="*50)
    
    if not failed_required:
        print("✓ All required modules imported successfully!")
    else:
        print(f"✗ Failed to import {len(failed_required)} required modules:")
        for module in failed_required:
            print(f"  - {module}")
    
    if failed_optional:
        print(f"~ {len(failed_optional)} optional modules not available:")
        for module in failed_optional:
            print(f"  - {module}")
    else:
        print("✓ All optional modules are available!")
    
    # Return success status
    return len(failed_required) == 0

if __name__ == "__main__":
    print("RI-Tracker Dependencies Test")
    print("="*50)
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print("="*50)
    
    success = test_imports()
    
    if success:
        print("\n🎉 Setup test PASSED! All required dependencies are available.")
        sys.exit(0)
    else:
        print("\n❌ Setup test FAILED! Some required dependencies are missing.")
        print("Please install missing packages using: pip install -r backend/requirements.txt")
        sys.exit(1)