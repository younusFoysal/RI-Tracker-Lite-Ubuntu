# Linux .deb Package Build Guide

## Overview
This guide explains how to build a .deb package for RI-Tracker that can be easily installed on any Ubuntu OS with a single command.

## One-Command Build Process

### Quick Start
```bash
cd backend
chmod +x build_linux.sh
./build_linux.sh
```

This single command will:
- Build the executable with PyInstaller
- Create a desktop file with proper icon association
- Generate a complete .deb package
- Provide installation instructions

## Ubuntu Compatibility Solutions

### For Maximum Compatibility (Recommended)
If you're building on Ubuntu 24.04 but need compatibility with Ubuntu 22.04 and other versions:

```bash
cd backend
chmod +x build_docker.sh
./build_docker.sh
```

This uses Docker with Ubuntu 22.04 base image to ensure GLIBC compatibility across Ubuntu versions.

### Standard Build (Same Ubuntu Version)
If building for the same Ubuntu version you're using:

```bash
cd backend
./build_linux.sh
```

## Build Output

After running the build script, you'll get:

### Files Created
- `ri-tracker_1.0.0_amd64.deb` - Main installation package
- `dist/ri-tracker` - Standalone executable
- `ri-tracker.desktop` - Desktop integration file
- `ritracker.png` - Application icon

### Package Details
- **Package Name**: ri-tracker
- **Version**: 1.0.0
- **Architecture**: amd64
- **Section**: utils
- **Dependencies**: None (self-contained)

## Installation on Any Ubuntu OS

### Simple Installation
```bash
# Download/copy the .deb file to target system
sudo dpkg -i ri-tracker_1.0.0_amd64.deb
```

### Handle Dependencies (if needed)
```bash
# If there are any dependency issues
sudo apt-get install -f
```

### Verify Installation
```bash
# Check if installed
dpkg -l | grep ri-tracker

# Run the application
ri-tracker
```

## Uninstallation

```bash
sudo apt remove ri-tracker
```

## Distribution

The .deb package can be:
- Shared with other Ubuntu users
- Installed without requiring development dependencies
- Managed through Ubuntu's package system
- Easily removed when no longer needed

## Troubleshooting

### Build Issues
1. **Missing dependencies**: Install required packages
   ```bash
   sudo apt update && sudo apt install -y python3-gi gir1.2-webkit2-4.1
   ```

2. **PyInstaller not found**: Install in virtual environment
   ```bash
   pip install -r requirements.txt
   ```

### Installation Issues
1. **Architecture mismatch**: Ensure you're using amd64 Ubuntu
2. **Permission denied**: Use `sudo` with `dpkg -i`
3. **Dependency problems**: Run `sudo apt-get install -f`

### Compatibility Issues
- For older Ubuntu versions, use the Docker build method
- The Docker-built package works on Ubuntu 22.04 and newer
- Standard build works best on the same Ubuntu version

## Advanced Options

### Custom Version
Edit `build_linux.sh` and change:
```bash
APP_VERSION="1.0.0"  # Change this line
```

### Custom Package Details
Modify the control file section in `build_linux.sh`:
```bash
cat > "$DEB_DIR/DEBIAN/control" << EOF
Package: ri-tracker
Version: $APP_VERSION
# Modify other fields as needed
EOF
```

## Benefits of .deb Package

1. **Easy Installation**: Single command installation
2. **System Integration**: Appears in application menu
3. **Dependency Management**: Ubuntu handles dependencies
4. **Easy Removal**: Clean uninstallation
5. **Version Tracking**: Package manager tracks versions
6. **Security**: Package integrity verification

## File Locations After Installation

- **Executable**: `/usr/bin/ri-tracker`
- **Desktop File**: `/usr/share/applications/ri-tracker.desktop`
- **Icon**: `/usr/share/pixmaps/ritracker.png`

## Testing the Package

1. **Build the package**:
   ```bash
   ./build_linux.sh
   ```

2. **Test installation**:
   ```bash
   sudo dpkg -i ri-tracker_1.0.0_amd64.deb
   ```

3. **Verify it works**:
   ```bash
   ri-tracker
   ```

4. **Test removal**:
   ```bash
   sudo apt remove ri-tracker
   ```

This ensures your .deb package works correctly before distribution.