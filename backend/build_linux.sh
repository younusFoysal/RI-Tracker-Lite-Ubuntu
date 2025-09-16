#!/bin/bash

echo "Building RI Tracker for Linux..."
echo ""
echo "Note: For maximum Ubuntu compatibility (22.04 and newer),"
echo "consider using './build_docker.sh' instead of this script."
echo "See Linux_deb_build.md for more details."
echo ""

# Ensure we're in the backend directory
cd "$(dirname "$0")"

# Clean previous build
echo "Cleaning previous build..."
#rm -rf build/ dist/
rm -rf build/

# Build with PyInstaller using the spec file
echo "Building executable with PyInstaller..."
pyinstaller ri-tracker.spec

# Check if build was successful
if [ ! -f "dist/ri-tracker" ]; then
    echo "Error: Build failed - executable not found!"
    exit 1
fi

echo "Build successful!"

# Copy the PNG icon to the dist directory for the desktop file
echo "Copying icon to dist directory..."
cp ritracker.png dist/

# Create desktop file
echo "Creating desktop file..."
python3 create_desktop_file.py

echo ""
echo "Build complete! Files created:"
echo "- Executable: $(pwd)/dist/ri-tracker"
echo "- Desktop file: $(pwd)/ri-tracker.desktop"
echo "- Icon: $(pwd)/dist/ritracker.png"
echo ""
echo "To run the application:"
echo "  ./dist/ri-tracker"
echo ""
echo "The desktop file has been installed to ~/.local/share/applications/"
echo "The application should now appear in your desktop environment's application menu with an icon."

# Create .deb package
echo ""
echo "Creating .deb package..."

# Create debian package structure
DEB_DIR="ri-tracker-deb"
rm -rf "$DEB_DIR"
mkdir -p "$DEB_DIR/DEBIAN"
mkdir -p "$DEB_DIR/usr/bin"
mkdir -p "$DEB_DIR/usr/share/applications"
mkdir -p "$DEB_DIR/usr/share/pixmaps"

# Copy files to debian package structure
cp "dist/ri-tracker" "$DEB_DIR/usr/bin/"
cp "ri-tracker.desktop" "$DEB_DIR/usr/share/applications/"
cp "ritracker.png" "$DEB_DIR/usr/share/pixmaps/"

# Update desktop file for system-wide installation
sed -i "s|Exec=.*|Exec=/usr/bin/ri-tracker|g" "$DEB_DIR/usr/share/applications/ri-tracker.desktop"
sed -i "s|Icon=.*|Icon=/usr/share/pixmaps/ritracker.png|g" "$DEB_DIR/usr/share/applications/ri-tracker.desktop"

# Get application version (you can modify this as needed)
APP_VERSION="1.0.0"

# Create control file
cat > "$DEB_DIR/DEBIAN/control" << EOF
Package: ri-tracker
Version: $APP_VERSION
Section: utils
Priority: optional
Architecture: amd64
Depends: 
Maintainer: Remote Integrity Team <contact@remoteintegrity.com>
Description: Remote Integrity Tracker Application
 A comprehensive activity tracking and monitoring application
 for remote work environments. Tracks application usage,
 browser history, and system activity.
EOF

# Set proper permissions
chmod 755 "$DEB_DIR/usr/bin/ri-tracker"
chmod 644 "$DEB_DIR/usr/share/applications/ri-tracker.desktop"
chmod 644 "$DEB_DIR/usr/share/pixmaps/ritracker.png"

# Build the .deb package
DEB_FILE="ri-tracker_${APP_VERSION}_amd64.deb"
dpkg-deb --build "$DEB_DIR" "$DEB_FILE"

if [ -f "$DEB_FILE" ]; then
    echo "✓ .deb package created successfully: $DEB_FILE"
    echo ""
    echo "========================================="
    echo "       INSTALLATION INSTRUCTIONS        "
    echo "========================================="
    echo ""
    echo "🚀 Quick Installation (Any Ubuntu OS):"
    echo "   sudo dpkg -i $DEB_FILE"
    echo ""
    echo "🔧 Fix dependencies (if needed):"
    echo "   sudo apt-get install -f"
    echo ""
    echo "✅ Verify installation:"
    echo "   ri-tracker"
    echo ""
    echo "🗑️  Uninstall when needed:"
    echo "   sudo apt remove ri-tracker"
    echo ""
    echo "📋 Package details:"
    dpkg-deb --info "$DEB_FILE"
    echo ""
    echo "✅ Build completed successfully!"
    echo "   The .deb package is ready for distribution and can be"
    echo "   easily installed on any Ubuntu OS with a single command."
else
    echo "✗ Failed to create .deb package"
    echo "   Check the error messages above for troubleshooting."
fi