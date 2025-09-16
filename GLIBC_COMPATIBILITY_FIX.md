# GLIBC Compatibility Fix for Ubuntu Cross-Version Support

## Problem Description

The RI-Tracker executable built on Ubuntu 24.04 fails to run on Ubuntu 22.04 with the following error:

```
[PYI-40729:ERROR] Failed to load Python shared library '/tmp/_MEI8CheZF/libpython3.12.so.1.0': 
/lib/x86_64-linux-gnu/libm.so.6: version `GLIBC_2.38' not found (required by /tmp/_MEI8CheZF/libpython3.12.so.1.0)
```

## Root Cause

- **Ubuntu 24.04** uses **GLIBC 2.38** and **Python 3.12**
- **Ubuntu 22.04** uses **GLIBC 2.35** and **Python 3.10**
- PyInstaller bundles the system's Python shared library which depends on the host system's GLIBC version
- When the executable is built on Ubuntu 24.04, it requires GLIBC 2.38 which is not available on Ubuntu 22.04

## Solution

Use Docker with Ubuntu 22.04 base image to build the executable, ensuring compatibility with both Ubuntu 22.04 and newer versions.

### Files Created

1. **`backend/Dockerfile`** - Ubuntu 22.04 based container for building
2. **`backend/build_docker.sh`** - Docker build script with compatibility checks

## Usage Instructions

### Prerequisites

- Docker must be installed on the build system
- All existing dependencies and requirements.txt must be present

### Building with Docker (Recommended)

1. Navigate to the backend directory:
   ```bash
   cd backend/
   ```

2. Run the Docker build script:
   ```bash
   ./build_docker.sh
   ```

3. The script will:
   - Check if Docker is available
   - Build a Docker image using Ubuntu 22.04
   - Build the application inside the container
   - Copy the executable to `docker_output/` directory
   - Clean up the Docker image

### Building on Ubuntu 22.04 System (Alternative)

If you have access to an Ubuntu 22.04 system, you can build directly:

```bash
./build_linux.sh
```

## Output

The Docker build process creates:
- **`docker_output/ri-tracker`** - Compatible executable
- **`docker_output/*.deb`** - Debian package (if created)

## Compatibility

The executable built with this method will work on:
- ✅ Ubuntu 22.04 (GLIBC 2.35)
- ✅ Ubuntu 24.04 (GLIBC 2.38)
- ✅ Other Linux distributions with GLIBC 2.35 or newer

## Verification

To verify the executable works on Ubuntu 22.04:

1. Copy the executable to the target system:
   ```bash
   scp docker_output/ri-tracker user@ubuntu22-system:~/
   ```

2. On Ubuntu 22.04 system:
   ```bash
   chmod +x ri-tracker
   ./ri-tracker
   ```

## Technical Details

### Docker Image Specifications
- **Base Image**: ubuntu:22.04
- **Python Version**: 3.10.x (default for Ubuntu 22.04)
- **GLIBC Version**: 2.35
- **Dependencies**: All required system libraries for GUI and PyInstaller

### Build Process
1. Docker creates Ubuntu 22.04 environment
2. Installs Python 3.10 and required system packages
3. Installs Python dependencies from requirements.txt
4. Runs PyInstaller with ri-tracker.spec
5. Creates standalone executable with compatible libraries
6. Copies output to host system

## Troubleshooting

### Docker Not Available
```
Error: Docker is not installed or not available in PATH
```
**Solution**: Install Docker or use Ubuntu 22.04 system with `./build_linux.sh`

### Build Failures
- Ensure all dependencies are listed in `requirements.txt`
- Check Docker has sufficient disk space
- Verify internet connection for package downloads

### Runtime Issues
- The executable should work on any system with GLIBC 2.35+
- For systems with older GLIBC, consider building on even older base images

## Future Improvements

1. **Multi-stage builds**: Optimize Docker image size
2. **Static linking**: Investigate fully static executables
3. **AppImage**: Consider AppImage format for maximum compatibility
4. **CI/CD Integration**: Automate builds for multiple Ubuntu versions

## Files Modified/Created

- ✅ `backend/Dockerfile` - New
- ✅ `backend/build_docker.sh` - New  
- ✅ `GLIBC_COMPATIBILITY_FIX.md` - New (this file)

The original build process (`build_linux.sh`) remains unchanged for local development.