import os, sys

# Ensure the backend package is importable when running from repo root
BASE_DIR = os.path.dirname(__file__)
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from main import Api

if __name__ == "__main__":
    api = Api()
    print("Running Api.take_screenshot() test...")
    path = api.take_screenshot()
    if path and os.path.exists(path):
        print(f"Screenshot path: {path}")
        info = os.stat(path)
        print(f"Size: {info.st_size} bytes")
        print("Attempting upload via Api.upload_screenshot()...")
        result = api.upload_screenshot(path)
        if result:
            print("Upload success:")
            print(result)
        else:
            print("Upload failed or server unreachable.")
    else:
        print("Api.take_screenshot() returned no file.")
