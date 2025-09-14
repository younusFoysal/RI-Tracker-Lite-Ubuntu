#!/usr/bin/env python3

import os
import shutil
from pathlib import Path

def create_desktop_file():
    """Create a .desktop file for Linux to display the application icon properly"""
    
    # Get the current directory (where the executable will be)
    current_dir = Path.cwd().absolute()
    executable_path = current_dir / "dist" / "ri-tracker"
    icon_path = current_dir / "ritracker.png"
    
    # Desktop file content
    desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=RI Tracker
Comment=Remote Integrity Tracker Application
Exec={executable_path}
Icon={icon_path}
Terminal=false
Categories=Office;Utility;
"""
    
    # Write the desktop file
    desktop_file = current_dir / "ri-tracker.desktop"
    with open(desktop_file, 'w') as f:
        f.write(desktop_content)
    
    # Make it executable
    os.chmod(desktop_file, 0o755)
    
    print(f"Created desktop file: {desktop_file}")
    print(f"Executable path: {executable_path}")
    print(f"Icon path: {icon_path}")
    
    # Also try to install to user's applications directory
    try:
        user_apps_dir = Path.home() / ".local" / "share" / "applications"
        user_apps_dir.mkdir(parents=True, exist_ok=True)
        
        user_desktop_file = user_apps_dir / "ri-tracker.desktop"
        shutil.copy2(desktop_file, user_desktop_file)
        os.chmod(user_desktop_file, 0o755)
        
        print(f"Installed desktop file to: {user_desktop_file}")
    except Exception as e:
        print(f"Could not install to user applications directory: {e}")

if __name__ == "__main__":
    create_desktop_file()