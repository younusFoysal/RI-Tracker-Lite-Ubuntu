#!/usr/bin/env python3
"""
Standalone screenshot test for Ubuntu/Wayland/X11.

Usage:
  python3 backend/test_screenshot.py

This script:
- Prints session/display environment info
- Probes availability of common screenshot tools
- Invokes Api.take_screenshot() from backend/main.py and reports the result

It does not launch the webview UI.
"""
import os
import shutil
import sys
from datetime import datetime

# Ensure backend is importable when running from repo root
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(THIS_DIR)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from backend.main import Api  # noqa: E402

def which(name):
    return shutil.which(name) or "(not found)"

def print_env_info():
    print("=== Environment Info ===")
    print(f"XDG_SESSION_TYPE = {os.environ.get('XDG_SESSION_TYPE')}")
    print(f"DISPLAY           = {os.environ.get('DISPLAY')}")
    print(f"WAYLAND_DISPLAY   = {os.environ.get('WAYLAND_DISPLAY')}")
    print()

    print("=== Screenshot tools availability ===")
    for tool in [
        'gnome-screenshot', 'grim', 'spectacle', 'xfce4-screenshooter', 'gdbus'
    ]:
        print(f"{tool:20s}: {which(tool)}")
    print()


def main():
    print_env_info()
    api = Api()

    print("Taking screenshot via Api.take_screenshot()...")
    path = api.take_screenshot()
    if path and os.path.exists(path):
        size = os.path.getsize(path)
        print(f"SUCCESS: Screenshot captured at {path} ({size} bytes)")
        print(f"Timestamp recorded: {api.screenshot_timestamp}")
    else:
        print("FAILURE: Screenshot could not be captured.")
        print("Tips:")
        print("- On GNOME/Wayland: sudo apt install -y gnome-screenshot libglib2.0-bin")
        print("- On KDE: sudo apt install -y kde-spectacle")
        print("- On XFCE: sudo apt install -y xfce4-screenshooter")
        print("- On wlroots/Sway/Hyprland: sudo apt install -y grim")

if __name__ == '__main__':
    main()
