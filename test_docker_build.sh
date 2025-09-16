#!/bin/bash

echo "Testing Docker build scenario..."
echo ""

# Navigate to backend directory
cd /home/foysal/Projects/RemoteIntegrity/RI-Tracker-Lite-Ubuntu/backend

# Test the build_docker.sh script
echo "Running ./build_docker.sh..."
echo "Expected: Error about Docker not being installed"
echo ""

./build_docker.sh

echo ""
echo "Test completed. The script should show Docker error message and suggest alternatives."