#!/usr/bin/env python3
"""
Comprehensive screenshot test script to reproduce and analyze the exact failure scenario
from the issue description, testing all current fallback methods systematically.
"""

import os
import sys
import subprocess
import tempfile
import time
import base64
from datetime import datetime, timezone

# Ensure the backend package is importable when running from repo root
BASE_DIR = os.path.dirname(__file__)
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

def test_environment_detection():
    """Test environment detection logic"""
    print("=== ENVIRONMENT DETECTION ===")
    session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
    display = os.environ.get('DISPLAY')
    wayland_display = os.environ.get('WAYLAND_DISPLAY')
    is_wayland = (session_type == 'wayland') or (wayland_display and not display)
    
    print(f"XDG_SESSION_TYPE: {session_type}")
    print(f"DISPLAY: {display}")
    print(f"WAYLAND_DISPLAY: {wayland_display}")
    print(f"Detected as Wayland: {is_wayland}")
    print()

def test_mss_screenshot():
    """Test MSS screenshot capture"""
    print("=== MSS SCREENSHOT TEST ===")
    try:
        import mss
        import mss.tools
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        with mss.mss() as sct:
            screenshot = sct.grab(sct.monitors[0])  # 0 = all monitors
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=temp_filename)
            
        if os.path.exists(temp_filename) and os.path.getsize(temp_filename) > 0:
            print(f"✓ MSS screenshot successful: {temp_filename} ({os.path.getsize(temp_filename)} bytes)")
            os.unlink(temp_filename)
            return True
        else:
            print("✗ MSS screenshot failed: empty file")
            return False
            
    except Exception as e:
        print(f"✗ MSS screenshot failed: {e}")
        return False

def test_gdbus_screenshot():
    """Test GNOME Shell D-Bus screenshot via gdbus"""
    print("=== GDBUS GNOME SCREENSHOT TEST ===")
    try:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        result = subprocess.run([
            'gdbus', 'call', '--session',
            '--dest', 'org.gnome.Shell.Screenshot',
            '--object-path', '/org/gnome/Shell/Screenshot',
            '--method', 'org.gnome.Shell.Screenshot.Screenshot',
            'false', 'false', temp_filename
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        
        if result.returncode == 0 and os.path.exists(temp_filename) and os.path.getsize(temp_filename) > 0:
            print(f"✓ gdbus screenshot successful: {temp_filename} ({os.path.getsize(temp_filename)} bytes)")
            os.unlink(temp_filename)
            return True
        else:
            err_str = result.stderr.decode(errors='ignore')
            print(f"✗ gdbus screenshot failed: rc={result.returncode}, err={err_str}")
            return False
            
    except FileNotFoundError:
        print("✗ gdbus not found")
        return False
    except Exception as e:
        print(f"✗ gdbus screenshot error: {e}")
        return False

def test_dbus_send_screenshot():
    """Test GNOME Shell D-Bus screenshot via dbus-send"""
    print("=== DBUS-SEND GNOME SCREENSHOT TEST ===")
    try:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        result = subprocess.run([
            'dbus-send', '--session', '--print-reply',
            '--dest=org.gnome.Shell.Screenshot',
            '/org/gnome/Shell/Screenshot',
            'org.gnome.Shell.Screenshot.Screenshot',
            'boolean:false', 'boolean:false', f'string:{temp_filename}'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        
        if result.returncode == 0 and os.path.exists(temp_filename) and os.path.getsize(temp_filename) > 0:
            print(f"✓ dbus-send screenshot successful: {temp_filename} ({os.path.getsize(temp_filename)} bytes)")
            os.unlink(temp_filename)
            return True
        else:
            err_str = result.stderr.decode(errors='ignore')
            print(f"✗ dbus-send screenshot failed: rc={result.returncode}, err={err_str}")
            return False
            
    except FileNotFoundError:
        print("✗ dbus-send not found")
        return False
    except Exception as e:
        print(f"✗ dbus-send screenshot error: {e}")
        return False

def test_cli_tools():
    """Test various CLI screenshot tools"""
    print("=== CLI TOOLS TEST ===")
    
    tools = [
        ('gnome-screenshot', ['gnome-screenshot', '--file={}'], "GNOME screenshot tool"),
        ('spectacle', ['spectacle', '-b', '-n', '-o', '{}'], "KDE screenshot tool"),
        ('xfce4-screenshooter', ['xfce4-screenshooter', '-f', '-s', '{}'], "XFCE screenshot tool"),
        ('grim', ['grim', '{}'], "wlroots screenshot tool"),
        ('scrot', ['scrot', '{}'], "X11 screenshot tool"),
        ('import', ['import', '-window', 'root', '{}'], "ImageMagick screenshot tool"),
    ]
    
    successful_tools = []
    
    for tool_name, cmd_template, description in tools:
        print(f"Testing {tool_name} ({description})...")
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                temp_filename = temp_file.name
            
            # Format the command with the temp filename
            cmd = [part.format(temp_filename) if '{}' in part else part for part in cmd_template]
            
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
            
            if result.returncode == 0 and os.path.exists(temp_filename) and os.path.getsize(temp_filename) > 0:
                print(f"  ✓ {tool_name} successful: {os.path.getsize(temp_filename)} bytes")
                successful_tools.append(tool_name)
                os.unlink(temp_filename)
            else:
                err_str = result.stderr.decode(errors='ignore')
                print(f"  ✗ {tool_name} failed: rc={result.returncode}, err={err_str}")
                
        except FileNotFoundError:
            print(f"  ✗ {tool_name} not found")
        except Exception as e:
            print(f"  ✗ {tool_name} error: {e}")
    
    print(f"Successful tools: {successful_tools}")
    return successful_tools

def test_xdg_desktop_portal():
    """Test xdg-desktop-portal screenshot"""
    print("=== XDG-DESKTOP-PORTAL TEST ===")
    try:
        # Check if xdg-desktop-portal is running
        result = subprocess.run(['pgrep', 'xdg-desktop-portal'], capture_output=True)
        if result.returncode == 0:
            print("✓ xdg-desktop-portal is running")
            
            # Try to call the portal via dbus
            result = subprocess.run([
                'dbus-send', '--session', '--print-reply',
                '--dest=org.freedesktop.portal.Desktop',
                '/org/freedesktop/portal/desktop',
                'org.freedesktop.portal.Screenshot.Screenshot',
                'string:', 'dict:'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
            
            if result.returncode == 0:
                print("✓ xdg-desktop-portal Screenshot method available")
                return True
            else:
                print(f"✗ xdg-desktop-portal Screenshot failed: {result.stderr.decode(errors='ignore')}")
                return False
        else:
            print("✗ xdg-desktop-portal not running")
            return False
            
    except Exception as e:
        print(f"✗ xdg-desktop-portal test error: {e}")
        return False

def test_placeholder_generation():
    """Test placeholder image generation"""
    print("=== PLACEHOLDER GENERATION TEST ===")
    try:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        placeholder_png_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO0nVxkAAAAASUVORK5CYII="
        )
        with open(temp_filename, 'wb') as f:
            f.write(base64.b64decode(placeholder_png_b64))
        
        if os.path.exists(temp_filename) and os.path.getsize(temp_filename) > 0:
            print(f"✓ Placeholder generation successful: {temp_filename} ({os.path.getsize(temp_filename)} bytes)")
            os.unlink(temp_filename)
            return True
        else:
            print("✗ Placeholder generation failed: empty file")
            return False
            
    except Exception as e:
        print(f"✗ Placeholder generation error: {e}")
        return False

def test_api_screenshot():
    """Test the main Api.take_screenshot() method"""
    print("=== API SCREENSHOT TEST ===")
    try:
        # Import the Api class from the backend directory
        import sys
        import os
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        from main import Api
        
        api = Api()
        path = api.take_screenshot()
        
        if path and os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✓ Api.take_screenshot() successful: {path} ({size} bytes)")
            
            # Test upload as well
            result = api.upload_screenshot(path)
            if result:
                print(f"✓ Upload successful: {result['url']}")
                return True
            else:
                print("✗ Upload failed")
                return False
        else:
            print("✗ Api.take_screenshot() returned no file")
            return False
            
    except Exception as e:
        print(f"✗ Api screenshot test error: {e}")
        return False

def main():
    """Run comprehensive screenshot tests"""
    print("COMPREHENSIVE SCREENSHOT TEST")
    print("=" * 50)
    
    test_environment_detection()
    
    test_results = []
    
    # Test all methods
    test_results.append(("MSS", test_mss_screenshot()))
    test_results.append(("gdbus", test_gdbus_screenshot()))
    test_results.append(("dbus-send", test_dbus_send_screenshot()))
    
    successful_cli_tools = test_cli_tools()
    test_results.append(("CLI tools", len(successful_cli_tools) > 0))
    
    test_results.append(("XDG Portal", test_xdg_desktop_portal()))
    test_results.append(("Placeholder", test_placeholder_generation()))
    test_results.append(("API Method", test_api_screenshot()))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    for test_name, success in test_results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{test_name:15} {status}")
    
    passed = sum(1 for _, success in test_results if success)
    total = len(test_results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if successful_cli_tools:
        print(f"Available CLI tools: {', '.join(successful_cli_tools)}")
    else:
        print("No CLI screenshot tools available")

if __name__ == "__main__":
    main()