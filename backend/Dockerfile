# Use Ubuntu 22.04 as base to ensure GLIBC compatibility with older systems
FROM ubuntu:22.04

# Set environment variables to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Update and install required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    libgtk-3-dev \
    libwebkit2gtk-4.0-dev \
    libglib2.0-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libatk1.0-dev \
    libgirepository1.0-dev \
    pkg-config \
    dpkg-dev \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app/

# Create output directory for the built executable
RUN mkdir -p /app/output

# Build the application
RUN chmod +x build_linux.sh && ./build_linux.sh

# Create a script to copy files to the mounted output directory
RUN echo '#!/bin/bash' > /app/copy_output.sh && \
    echo 'cp dist/ri-tracker /app/output/ 2>/dev/null || echo "Warning: ri-tracker executable not found"' >> /app/copy_output.sh && \
    echo 'cp *.deb /app/output/ 2>/dev/null || echo "Warning: .deb file not found"' >> /app/copy_output.sh && \
    echo 'ls -la /app/output/' >> /app/copy_output.sh && \
    echo 'echo "Files copied to output directory"' >> /app/copy_output.sh && \
    chmod +x /app/copy_output.sh

CMD ["/app/copy_output.sh"]