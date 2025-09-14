#!/usr/bin/env python3

from PIL import Image
import os

def convert_ico_to_png():
    """Convert icon.ico to ri-tracker.png"""
    try:
        # Open the .ico file
        with Image.open('icon.ico') as img:
            # Get the largest size available
            img.load()
            # Save as PNG
            img.save('ri-tracker.png', 'PNG')
            print(f"Successfully converted icon.ico to ri-tracker.png")
            print(f"Icon size: {img.size}")
    except Exception as e:
        print(f"Error converting icon: {e}")

if __name__ == "__main__":
    convert_ico_to_png()