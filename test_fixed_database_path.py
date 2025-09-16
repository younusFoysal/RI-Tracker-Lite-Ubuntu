#!/usr/bin/env python3
"""
Test script to verify authentication persistence with the fixed database path
"""

import os
import sys
import sqlite3
import json

# Add backend to path to import the main module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from main import Api, init_db, db_file, DATA_DIR

print("=== Testing Fixed Database Path Configuration ===")
print(f"DATA_DIR: {DATA_DIR}")
print(f"Database path: {db_file}")
print(f"Database directory exists: {os.path.exists(os.path.dirname(db_file))}")
print(f"Database file exists: {os.path.exists(db_file)}")

# Check if the database path is correctly using DATA_DIR
if DATA_DIR in db_file:
    print("✓ Database path is correctly configured to use DATA_DIR")
else:
    print("✗ Database path is NOT using DATA_DIR")
    sys.exit(1)

# Initialize database
init_db()
print("✓ Database initialized successfully")

# Test 1: Clear any existing data and verify clean start
print("\n--- Test 1: Clean Start ---")
api = Api()
api.clear_auth_data()

auth_status = api.is_authenticated()
print(f"Clean start auth status: {auth_status}")

if not auth_status['authenticated']:
    print("✓ Correct: Clean start shows not authenticated")
else:
    print("✗ Error: Clean start incorrectly shows authenticated")

# Test 2: Test real login with remember_me=True
print("\n--- Test 2: Real Login with Fixed Database Path ---")
try:
    login_result = api.login("test@test.com", "123456", remember_me=True)
    print(f"Login result: {login_result['success']}")
    
    if login_result['success']:
        print("✓ Login successful with fixed database path!")
        
        # Verify data is saved
        auth_status = api.is_authenticated()
        print(f"Auth status after login: {auth_status}")
        
        if auth_status['authenticated']:
            user_data = api.get_current_user()
            print(f"✓ User data available: {user_data['success']}")
            if user_data['success']:
                print(f"  User: {user_data['user']['name']} ({user_data['user']['email']})")
        else:
            print("✗ Authentication not set after login")
    else:
        print(f"✗ Login failed: {login_result.get('message', 'Unknown error')}")
        
except Exception as e:
    print(f"✗ Login error: {e}")

# Test 3: Verify database file exists in correct location
print("\n--- Test 3: Database File Verification ---")
if os.path.exists(db_file):
    print(f"✓ Database file exists at: {db_file}")
    
    # Check permissions
    if os.access(db_file, os.R_OK):
        print("✓ Database file is readable")
    else:
        print("✗ Database file is not readable")
        
    if os.access(db_file, os.W_OK):
        print("✓ Database file is writable")
    else:
        print("✗ Database file is not writable")
        
    # Check contents
    try:
        with sqlite3.connect(db_file) as conn:
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM auth_data')
            count = c.fetchone()[0]
            print(f"✓ Auth data records in database: {count}")
            
            if count > 0:
                c.execute('SELECT token, user_data FROM auth_data ORDER BY id DESC LIMIT 1')
                result = c.fetchone()
                if result:
                    print(f"✓ Latest auth data found:")
                    print(f"  Token: {result[0][:20]}... (truncated)")
                    user_data = json.loads(result[1])
                    print(f"  User: {user_data.get('name', 'N/A')} ({user_data.get('email', 'N/A')})")
                else:
                    print("✗ No auth data found")
            
    except Exception as e:
        print(f"✗ Database read error: {e}")
else:
    print(f"✗ Database file does not exist at: {db_file}")

# Test 4: App restart simulation
print("\n--- Test 4: App Restart Simulation ---")
api2 = Api()  # This should load auth data from the correct database location

auth_check = api2.is_authenticated()
print(f"Auth status after restart: {auth_check}")

if auth_check and auth_check.get('authenticated'):
    user_check = api2.get_current_user()
    print(f"User data after restart: {user_check['success']}")
    
    if user_check and user_check.get('success'):
        print("✓ SUCCESS: Authentication persisted after restart with fixed database path!")
        print(f"  User: {user_check['user']['name']} ({user_check['user']['email']})")
        
        # Test authenticated API call
        try:
            profile_result = api2.get_profile()
            if profile_result['success']:
                print("✓ SUCCESS: Authenticated API call works after restart!")
            else:
                print(f"✗ Authenticated API call failed: {profile_result.get('message')}")
        except Exception as e:
            print(f"✗ Profile API error: {e}")
    else:
        print("✗ FAILED: get_current_user() failed after restart")
else:
    print("✗ FAILED: Authentication not persisted after restart")

# Test 5: Check DATA_DIR permissions
print("\n--- Test 5: DATA_DIR Permissions Check ---")
if os.path.exists(DATA_DIR):
    print(f"✓ DATA_DIR exists: {DATA_DIR}")
    
    if os.access(DATA_DIR, os.R_OK | os.W_OK):
        print("✓ DATA_DIR has read/write permissions")
    else:
        print("✗ DATA_DIR lacks read/write permissions")
        
    # Test creating a file in DATA_DIR
    test_file = os.path.join(DATA_DIR, 'test_write.txt')
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✓ Can create and delete files in DATA_DIR")
    except Exception as e:
        print(f"✗ Cannot write to DATA_DIR: {e}")
else:
    print(f"✗ DATA_DIR does not exist: {DATA_DIR}")

print("\n=== Fixed Database Path Test Complete ===")
print("If all tests pass, the authentication persistence issue should now be resolved!")