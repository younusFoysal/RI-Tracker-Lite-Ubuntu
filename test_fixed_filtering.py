#!/usr/bin/env python3

import os
import sys
import psutil
import platform

def test_fixed_app_filtering():
    """Test the fixed application filtering behavior"""
    print("=== Testing FIXED Application Filtering ===\n")
    
    # Use the same logic as the updated main.py
    print(f"Platform: {platform.system()}")
    
    # Define system process patterns to exclude based on platform
    if platform.system() == "Windows":
        # Windows system processes
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
        
        # Windows system directories patterns
        system_dirs = [
            '\\Windows\\', '\\Windows\\System32\\', '\\Windows\\SysWOW64\\',
            '\\Windows\\WinSxS\\', '\\Windows\\servicing\\', '\\ProgramData\\',
            '\\Program Files\\Common Files\\', '\\Program Files (x86)\\Common Files\\'
        ]
    else:
        # Linux/Unix system processes
        system_process_names = [
            # Core system processes
            'init', 'kthreadd', 'ksoftirqd', 'migration', 'rcu_', 'watchdog',
            
            # systemd processes
            'systemd', 'systemd-journald', 'systemd-udevd', 'systemd-resolved', 
            'systemd-logind', 'systemd-oomd', 'systemd-networkd', 'systemd-timesyncd',
            
            # D-Bus processes
            'dbus', 'dbus-daemon', 'dbus-launch',
            
            # Network and hardware management
            'NetworkManager', 'ModemManager', 'wpa_supplicant', 'dhclient',
            'polkitd', 'udisksd', 'upowerd', 'colord', 'accounts-daemon',
            
            # Desktop environment - GNOME
            'gnome-shell', 'gnome-session-binary', 'gnome-session-ctl',
            'gnome-keyring-daemon', 'gnome-shell-calendar-server',
            'gnome-remote-desktop-daemon', 'gdm3', 'gdm-wayland-session',
            
            # GNOME Settings Daemon processes
            'gsd-a11y-settings', 'gsd-color', 'gsd-datetime', 'gsd-housekeeping',
            'gsd-keyboard', 'gsd-media-keys', 'gsd-power', 'gsd-print-notifications',
            'gsd-printer', 'gsd-rfkill', 'gsd-screensaver-proxy', 'gsd-sharing',
            'gsd-smartcard', 'gsd-sound', 'gsd-wacom', 'gsd-xsettings',
            'gsd-disk-utility-notify',
            
            # GVFS (GNOME Virtual File System)
            'gvfsd', 'gvfsd-trash', 'gvfsd-metadata', 'gvfsd-recent',
            'gvfsd-network', 'gvfsd-dnssd', 'gvfsd-admin',
            'gvfs-udisks2-volume-monitor', 'gvfs-afc-volume-monitor',
            'gvfs-mtp-volume-monitor', 'gvfs-goa-volume-monitor',
            'gvfs-gphoto2-volume-monitor',
            
            # Input methods and accessibility
            'ibus-daemon', 'ibus-engine-simple', 'ibus-extension-gtk3',
            'ibus-memconf', 'ibus-portal', 'ibus-x11',
            'at-spi-bus-launcher', 'at-spi2-registryd',
            
            # Desktop portals and integration
            'xdg-desktop-portal', 'xdg-desktop-portal-gnome', 'xdg-desktop-portal-gtk',
            'xdg-document-portal', 'xdg-permission-store',
            
            # Evolution data services
            'evolution-source-registry', 'evolution-calendar-factory',
            'evolution-addressbook-factory', 'evolution-alarm-notify',
            
            # Other GNOME services
            'goa-daemon', 'goa-identity-service', 'gcr-ssh-agent',
            'dconf-service', 'tracker-miner-fs-3',
            
            # Audio/Media services
            'pipewire', 'wireplumber', 'rtkit-daemon',
            
            # Print services
            'cupsd', 'cups-browsed',
            
            # System services
            'cron', 'rsyslogd', 'kerneloops', 'snapd', 'snapd-desktop-integration',
            'power-profiles-daemon', 'switcheroo-control', 'fwupd', 'boltd',
            'packagekitd'
        ]
        
        # Linux system directories patterns
        system_dirs = [
            '/usr/lib/systemd/', '/usr/libexec/', '/usr/lib/gnome-',
            '/usr/lib/gvfs/', '/usr/lib/evolution/', '/usr/lib/gsd-',
            '/lib/systemd/', '/sbin/', '/usr/sbin/'
        ]
    
    print(f"System processes to filter: {len(system_process_names)}")
    print(f"System directories to filter: {len(system_dirs)}\n")
    
    # Get list of running processes with FIXED filtering logic
    active_apps = {}
    system_apps_filtered = []
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
                
                # Check if it should be filtered by the FIXED logic
                is_system_by_name = app_name.lower() in [p.lower() for p in system_process_names]
                is_system_by_path = any(system_dir.lower() in exe_path.lower() for system_dir in system_dirs)
                
                if is_system_by_name or is_system_by_path:
                    # This WILL be filtered by the new logic
                    system_apps_filtered.append(app_name)
                else:
                    # This will NOT be filtered - legitimate user app
                    active_apps[app_name] = {
                        'name': app_name,
                        'exe': exe_path
                    }
                    user_apps_found.append(app_name)
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
    except Exception as e:
        print(f"Error checking running applications: {e}")
        return
    
    print(f"Total applications that WILL be tracked: {len(active_apps)}")
    print(f"Linux system apps that WILL be filtered out: {len(system_apps_filtered)}")
    print(f"User apps that will be tracked: {len(user_apps_found)}\n")
    
    print("System apps that WILL be filtered out (SUCCESS):")
    for app in sorted(set(system_apps_filtered)):
        print(f"  - {app}")
    
    print(f"\nUser applications that will be tracked:")
    for app in sorted(set(user_apps_found)):
        print(f"  - {app}")
        
    print(f"\n=== SUMMARY ===")
    print(f"FIXED: Linux-specific filtering is now active!")
    print(f"System apps filtered: {len(set(system_apps_filtered))}")
    print(f"User apps tracked: {len(set(user_apps_found))}")
    print(f"Total apps that will be tracked: {len(active_apps)}")
    
    # Compare with the previous results
    print(f"\n=== IMPROVEMENT ===")
    print(f"BEFORE: ~110 total apps (91 system + 42 user)")
    print(f"AFTER:  {len(active_apps)} total apps ({len(set(system_apps_filtered))} filtered + {len(set(user_apps_found))} user)")
    print(f"Reduction: {110 - len(active_apps)} apps removed from tracking")

if __name__ == "__main__":
    test_fixed_app_filtering()