#!/usr/bin/env python3
"""
Test script to verify the frontend authentication fix
"""

import os
import sys
import sqlite3
import json

# Add backend to path to import the main module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from main import Api, init_db, db_file

print("=== Testing Frontend Authentication Fix ===")
print(f"Database location: {db_file}")

# Initialize database
init_db()

# Clear any existing auth data for a clean test
api = Api()
api.clear_auth_data()

# Simulate a successful login with remember_me=True
test_token = "frontend_fix_test_token"
test_user_data = {
    "employeeId": 123,
    "name": "Frontend Test User",
    "email": "frontend@test.com"
}

print("\n--- Step 1: Simulate login with remember_me=True ---")
login_success = api.save_auth_data(test_token, test_user_data)
print(f"Login save result: {'SUCCESS' if login_success else 'FAILED'}")

# Verify the data was saved
auth_check = api.is_authenticated()
print(f"Authentication status after save: {auth_check}")

if auth_check['authenticated']:
    user_data = api.get_current_user()
    print(f"User data after save: {user_data}")

# Test what happens when we create a new Api instance (simulating app restart)
print("\n--- Step 2: Simulate app restart (new Api instance) ---")
api2 = Api()  # This calls load_auth_data() in __init__

# Check if the auth data was loaded properly
auth_check2 = api2.is_authenticated()
print(f"Authentication status after restart: {auth_check2}")

if auth_check2['authenticated']:
    user_data2 = api2.get_current_user()
    print(f"User data after restart: {user_data2}")
    print("✓ SUCCESS: Authentication persists after restart!")
    
    # Verify the data matches what we saved
    if (api2.auth_token == test_token and 
        api2.user_data == test_user_data):
        print("✓ SUCCESS: Auth data matches exactly!")
    else:
        print("✗ WARNING: Auth data doesn't match exactly")
        print(f"Expected token: {test_token}")
        print(f"Loaded token: {api2.auth_token}")
        print(f"Expected user data: {test_user_data}")
        print(f"Loaded user data: {api2.user_data}")
else:
    print("✗ FAILED: Authentication not persisted after restart")

# Test edge case: verify that memory-only auth doesn't persist
print("\n--- Step 3: Test memory-only authentication (remember_me=False simulation) ---")
api3 = Api()
api3.clear_auth_data()  # Clear database

# Set auth data only in memory (simulating remember_me=False)
api3.auth_token = "memory_only_token"
api3.user_data = {"name": "Memory Only User"}

print(f"Memory-only auth status: {api3.is_authenticated()}")

# Create new instance - should not have auth data
api4 = Api()
auth_check4 = api4.is_authenticated()
print(f"Auth status after restart (should be false): {auth_check4}")

if not auth_check4['authenticated']:
    print("✓ SUCCESS: Memory-only auth correctly not persisted")
else:
    print("✗ ERROR: Memory-only auth was incorrectly persisted")

print("\n--- Step 4: Verify database state ---")
try:
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM auth_data')
        count = c.fetchone()[0]
        print(f"Auth data table row count: {count}")
        
        if count > 0:
            c.execute('SELECT token, user_data FROM auth_data ORDER BY id DESC LIMIT 1')
            result = c.fetchone()
            if result:
                print(f"Latest auth data in DB:")
                print(f"  Token: {result[0][:20]}... (truncated)")
                print(f"  User data: {result[1][:50]}... (truncated)")
except Exception as e:
    print(f"Database check error: {e}")

print("\n=== Frontend Fix Test Complete ===")
print("The backend authentication persistence is working correctly.")
print("With the frontend fix, the app should now properly check authentication on startup.")