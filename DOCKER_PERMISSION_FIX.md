# Docker Permission Fix Guide

## 🚨 Issue Identified
You have Docker installed (version 27.5.1) but are getting permission denied errors because your user is not in the docker group.

## 🔧 Quick Fix (Required)

### Step 1: Add Your User to Docker Group
Run this command and enter your password when prompted:
```bash
sudo usermod -aG docker $USER
```

### Step 2: Apply Group Changes
You have two options:

**Option A: Logout and Login Again (Recommended)**
- Logout of your current session
- Login again
- The docker group will be active

**Option B: Use newgrp Command**
```bash
newgrp docker
```

### Step 3: Verify Fix is Working
Test Docker without sudo:
```bash
docker --version
docker run hello-world
```

You should see:
- Docker version information
- "Hello from Docker!" message (downloads and runs test container)

## 🚀 Build Your .deb Package

Once Docker permissions are fixed, run your build:
```bash
cd /home/foysal/Projects/RemoteIntegrity/RI-Tracker-Lite-Ubuntu/backend
./build_docker.sh
```

## ✅ Expected Success Output
```
Building RI Tracker for Linux with Ubuntu 22.04 compatibility using Docker...
Building Docker image with Ubuntu 22.04 base...
✓ Build successful with Ubuntu 22.04 compatibility!

Built files:
- Executable: /path/to/docker_output/ri-tracker
- .deb package: /path/to/docker_output/*.deb
```

## 🔍 Troubleshooting

### If Still Getting Permission Errors
1. **Verify you're in docker group:**
   ```bash
   groups
   ```
   Should show: `foysal sudo vboxsf docker`

2. **Restart Docker service:**
   ```bash
   sudo systemctl restart docker
   ```

3. **Check Docker daemon status:**
   ```bash
   sudo systemctl status docker
   ```

### If Build Fails
1. **Check Docker is running:**
   ```bash
   docker info
   ```

2. **Clear Docker cache if needed:**
   ```bash
   docker system prune -f
   ```

## 📋 Summary
1. Run: `sudo usermod -aG docker $USER`
2. Logout and login (or use `newgrp docker`)
3. Test: `docker run hello-world`
4. Build: `./build_docker.sh`

Your .deb package will be ready for installation on any Ubuntu system!