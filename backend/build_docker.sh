#!/bin/bash

echo "Building RI Tracker for Linux with Ubuntu 22.04 compatibility using Docker..."

# Ensure we're in the backend directory
cd "$(dirname "$0")"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not available in PATH"
    echo "Please install Docker to use this build method"
    echo "Alternative: Use a Ubuntu 22.04 system and run ./build_linux.sh directly"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p docker_output

# Build the Docker image
echo "Building Docker image with Ubuntu 22.04 base..."
docker build -t ri-tracker-builder .

if [ $? -ne 0 ]; then
    echo "Error: Docker image build failed"
    exit 1
fi

echo "Docker image built successfully!"

# Run the container to build the application
echo "Building application in Docker container..."
docker run --rm -v "$(pwd)/docker_output:/app/output" ri-tracker-builder

if [ $? -ne 0 ]; then
    echo "Error: Application build failed in Docker container"
    exit 1
fi

# Check if the executable was created
if [ ! -f "docker_output/ri-tracker" ]; then
    echo "Error: Build failed - executable not found in docker_output directory!"
    exit 1
fi

echo ""
echo "✓ Build successful with Ubuntu 22.04 compatibility!"
echo ""
echo "Built files:"
echo "- Executable: $(pwd)/docker_output/ri-tracker"
if [ -f "docker_output/*.deb" ]; then
    echo "- .deb package: $(pwd)/docker_output/*.deb"
fi
echo ""
echo "This executable should work on Ubuntu 22.04 and newer versions."
echo ""
echo "To run the application:"
echo "  ./docker_output/ri-tracker"
echo ""
echo "To copy to system location (optional):"
echo "  sudo cp docker_output/ri-tracker /usr/local/bin/"
echo "  ri-tracker"
echo ""
echo "To install .deb package (if available):"
echo "  sudo dpkg -i docker_output/*.deb"
echo "  sudo apt-get install -f  # if there are dependency issues"

# Clean up Docker image (optional, comment out if you want to keep it for future builds)
echo ""
echo "Cleaning up Docker image..."
docker rmi ri-tracker-builder

echo "Build process completed!"