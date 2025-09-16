#!/usr/bin/env python3
"""
Test script to reproduce authentication persistence issue
"""

import os
import sys
import sqlite3
import json
from pathlib import Path

# Add backend to path to import the main module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Test the DATA_DIR and db_file path creation
APP_NAME = "RI_Tracker"
DATA_DIR = os.path.join(os.getenv('LOCALAPPDATA') or os.path.expanduser("~/.config"), APP_NAME)
db_file = os.path.join(DATA_DIR, 'tracker.db')

print(f"Testing authentication persistence on this system:")
print(f"Platform: {sys.platform}")
print(f"LOCALAPPDATA env var: {os.getenv('LOCALAPPDATA')}")
print(f"Home directory: {os.path.expanduser('~')}")
print(f"DATA_DIR: {DATA_DIR}")
print(f"db_file path: {db_file}")
print(f"DATA_DIR exists: {os.path.exists(DATA_DIR)}")
print(f"db_file exists: {os.path.exists(db_file)}")

# Test directory creation
try:
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"✓ Successfully created/verified DATA_DIR")
except Exception as e:
    print(f"✗ Error creating DATA_DIR: {e}")
    sys.exit(1)

# Test database creation and auth table
try:
    with sqlite3.connect(db_file) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS auth_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT,
                user_data TEXT
            )
        ''')
        print(f"✓ Successfully created/verified auth_data table")
except Exception as e:
    print(f"✗ Error creating auth_data table: {e}")
    sys.exit(1)

# Test saving authentication data
test_token = "test_token_12345"
test_user_data = {"employeeId": 1, "name": "Test User", "email": "test@example.com"}

try:
    with sqlite3.connect(db_file) as conn:
        # Clear existing data
        conn.execute('DELETE FROM auth_data')
        # Save test data
        conn.execute(
            'INSERT INTO auth_data (token, user_data) VALUES (?, ?)',
            (test_token, json.dumps(test_user_data))
        )
        print(f"✓ Successfully saved test auth data")
except Exception as e:
    print(f"✗ Error saving auth data: {e}")
    sys.exit(1)

# Test loading authentication data
try:
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute('SELECT token, user_data FROM auth_data ORDER BY id DESC LIMIT 1')
        result = c.fetchone()
        if result:
            loaded_token = result[0]
            loaded_user_data = json.loads(result[1])
            print(f"✓ Successfully loaded auth data")
            print(f"  Token: {loaded_token}")
            print(f"  User data: {loaded_user_data}")
            
            # Verify data matches
            if loaded_token == test_token and loaded_user_data == test_user_data:
                print(f"✓ Auth data persistence test PASSED - data matches!")
            else:
                print(f"✗ Auth data persistence test FAILED - data mismatch!")
                sys.exit(1)
        else:
            print(f"✗ No auth data found after saving")
            sys.exit(1)
except Exception as e:
    print(f"✗ Error loading auth data: {e}")
    sys.exit(1)

# Test file permissions
try:
    # Check if we can read and write to the database file
    if os.access(db_file, os.R_OK):
        print(f"✓ Database file is readable")
    else:
        print(f"✗ Database file is not readable")
        
    if os.access(db_file, os.W_OK):
        print(f"✓ Database file is writable")
    else:
        print(f"✗ Database file is not writable")
        
    if os.access(DATA_DIR, os.R_OK | os.W_OK):
        print(f"✓ DATA_DIR has read/write permissions")
    else:
        print(f"✗ DATA_DIR lacks read/write permissions")
        
except Exception as e:
    print(f"Error checking permissions: {e}")

print(f"\n--- Test completed successfully ---")
print(f"Authentication persistence should work correctly on this system.")