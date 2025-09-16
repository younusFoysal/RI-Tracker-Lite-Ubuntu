#!/usr/bin/env python3

import os
import sys
import psutil

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from main import Api

def test_current_app_filtering():
    """Test the current application filtering behavior"""
    print("=== Testing Current Application Filtering ===\n")
    
    # Create an API instance
    api = Api()
    
    # Manually call the check_running_applications logic to see what gets collected
    print("Current system process filtering logic (Windows-focused):")
    
    # Define system process patterns to exclude (current logic from main.py)
    system_process_names = [
        'System', 'Registry', 'smss.exe', 'csrss.exe', 'wininit.exe', 
        'services.exe', 'lsass.exe', 'svchost.exe', 'winlogon.exe', 
        'dwm.exe', 'conhost.exe', 'dllhost.exe', 'taskhostw.exe',
        'explorer.exe', 'RuntimeBroker.exe', 'ShellExperienceHost.exe',
        'SearchUI.exe', 'sihost.exe', 'ctfmon.exe', 'WmiPrvSE.exe',
        'spoolsv.exe', 'SearchIndexer.exe', 'fontdrvhost.exe',
        'WUDFHost.exe', 'LsaIso.exe', 'SgrmBroker.exe', 'audiodg.exe',
        'dasHost.exe', 'SearchProtocolHost.exe', 'SearchFilterHost.exe'
    ]
    
    # System directories patterns (current logic from main.py)
    system_dirs = [
        '\\Windows\\', '\\Windows\\System32\\', '\\Windows\\SysWOW64\\',
        '\\Windows\\WinSxS\\', '\\Windows\\servicing\\', '\\ProgramData\\',
        '\\Program Files\\Common Files\\', '\\Program Files (x86)\\Common Files\\'
    ]
    
    print(f"Windows system processes to exclude: {system_process_names}")
    print(f"Windows system directories to exclude: {system_dirs}\n")
    
    # Get list of running processes with current filtering logic
    active_apps = {}
    system_apps_found = []
    user_apps_found = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'username']):
            try:
                # Get process info
                proc_info = proc.info
                
                # Skip processes without a name or executable
                if not proc_info['name'] or not proc_info['exe']:
                    continue
                
                # Use the executable name as the app name
                app_name = os.path.basename(proc_info['exe'])
                exe_path = proc_info['exe']
                
                # Check if it would be filtered by current logic
                is_system_by_name = app_name.lower() in [p.lower() for p in system_process_names]
                is_system_by_path = any(system_dir.lower() in exe_path.lower() for system_dir in system_dirs)
                
                # Categorize as system or user app based on common Linux system process patterns
                is_linux_system_app = any([
                    app_name.startswith('systemd'),
                    app_name.startswith('dbus'),
                    app_name.startswith('gnome-') and app_name != 'gnome-terminal-server',
                    app_name.startswith('gsd-'),
                    app_name.startswith('xdg-'),
                    app_name.startswith('gvfs'),
                    app_name.startswith('ibus-'),
                    app_name.startswith('at-spi'),
                    app_name.startswith('evolution-') and 'user' not in app_name.lower(),
                    app_name in ['init', 'polkitd', 'NetworkManager', 'ModemManager', 'cupsd', 
                                'gdm3', 'upowerd', 'colord', 'rtkit-daemon', 'accounts-daemon',
                                'cron', 'udisksd', 'rsyslogd', 'wpa_supplicant', 'snapd',
                                'power-profiles-daemon', 'switcheroo-control', 'cups-browsed',
                                'kerneloops', 'pipewire', 'wireplumber', 'packagekitd', 'boltd',
                                'fwupd', 'tracker-miner-fs-3']
                ])
                
                if not (is_system_by_name or is_system_by_path):
                    # This would NOT be filtered by current logic
                    active_apps[app_name] = {
                        'name': app_name,
                        'exe': exe_path,
                        'is_linux_system': is_linux_system_app
                    }
                    
                    if is_linux_system_app:
                        system_apps_found.append(app_name)
                    else:
                        user_apps_found.append(app_name)
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
    except Exception as e:
        print(f"Error checking running applications: {e}")
        return
    
    print(f"Total applications that would be tracked: {len(active_apps)}")
    print(f"Linux system apps that would NOT be filtered (PROBLEM): {len(system_apps_found)}")
    print(f"User apps that would be tracked (CORRECT): {len(user_apps_found)}\n")
    
    print("Linux system apps that are NOT being filtered out:")
    for app in sorted(system_apps_found):
        print(f"  - {app}")
    
    print(f"\nUser applications that would be correctly tracked:")
    for app in sorted(user_apps_found):
        print(f"  - {app}")
        
    print(f"\n=== SUMMARY ===")
    print(f"The current Windows-based filtering is ineffective on Linux.")
    print(f"System apps being tracked: {len(system_apps_found)}")
    print(f"User apps being tracked: {len(user_apps_found)}")
    print(f"Total apps: {len(active_apps)}")

if __name__ == "__main__":
    test_current_app_filtering()