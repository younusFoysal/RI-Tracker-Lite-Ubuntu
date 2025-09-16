#!/usr/bin/env python3
"""
Test script to simulate the actual login and app restart scenario
"""

import os
import sys
import sqlite3
import json
import tempfile

# Add backend to path to import the main module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the main Api class and config
from main import Api, init_db, db_file, DATA_DIR

print("=== Testing Login and App Restart Simulation ===")
print(f"Database location: {db_file}")
print(f"Data directory: {DATA_DIR}")

# Initialize the database
init_db()

# Test 1: Fresh start - should not be authenticated
print("\n--- Test 1: Fresh API instance (simulating app start) ---")
api1 = Api()
auth_status = api1.is_authenticated()
print(f"Initial authentication status: {auth_status}")

if auth_status['authenticated']:
    print("✓ Found existing auth data")
    user_data = api1.get_current_user()
    print(f"Current user: {user_data}")
else:
    print("✗ No existing auth data (expected for fresh start)")

# Test 2: Simulate login with remember_me=True
print("\n--- Test 2: Simulating login with remember_me=True ---")

# Since we can't actually call the remote API, let's simulate a successful login
# by directly calling save_auth_data (which is what login() does when remember_me=True)
test_token = "simulated_login_token_12345"
test_user_data = {
    "employeeId": 1,
    "name": "Test User", 
    "email": "test@company.com",
    "role": "employee"
}

# Simulate what happens in login() when remember_me=True
login_success = api1.save_auth_data(test_token, test_user_data)
print(f"Login simulation result: {'SUCCESS' if login_success else 'FAILED'}")

# Verify the login worked
auth_status = api1.is_authenticated()
print(f"Authentication status after login: {auth_status}")

if auth_status['authenticated']:
    user_data = api1.get_current_user()
    print(f"Current user after login: {user_data}")

# Test 3: Simulate app restart by creating a new Api instance
print("\n--- Test 3: Simulating app restart (new Api instance) ---")
api2 = Api()  # This should load auth data from database in __init__

auth_status = api2.is_authenticated()
print(f"Authentication status after restart: {auth_status}")

if auth_status['authenticated']:
    user_data = api2.get_current_user()
    print(f"Current user after restart: {user_data}")
    print("✓ AUTH PERSISTENCE WORKS - User remains logged in after restart!")
else:
    print("✗ AUTH PERSISTENCE FAILED - User was logged out after restart!")
    
    # Let's debug why it failed
    print("\nDebugging the persistence issue...")
    
    # Check if data exists in database
    try:
        with sqlite3.connect(db_file) as conn:
            c = conn.cursor()
            c.execute('SELECT token, user_data FROM auth_data ORDER BY id DESC LIMIT 1')
            result = c.fetchone()
            if result:
                print(f"✓ Auth data found in database: token={result[0][:20]}..., user_data={result[1][:50]}...")
                
                # Try manual load
                load_result = api2.load_auth_data()
                print(f"Manual load_auth_data() result: {load_result}")
                
                if load_result:
                    print(f"✓ Manual load successful - token: {api2.auth_token is not None}")
                    print(f"✓ Manual load successful - user: {api2.user_data}")
                else:
                    print("✗ Manual load failed")
            else:
                print("✗ No auth data found in database")
                
                # Check all tables and their content
                c.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = c.fetchall()
                print(f"Available tables: {tables}")
                
                c.execute("SELECT COUNT(*) FROM auth_data")
                count = c.fetchone()[0]
                print(f"Auth data table row count: {count}")
                
    except Exception as e:
        print(f"✗ Database debug error: {e}")

# Test 4: Test login with remember_me=False
print("\n--- Test 4: Testing login with remember_me=False ---")
api3 = Api()
api3.clear_auth_data()  # Clear any existing data

# Set auth data in memory only (simulating remember_me=False)
api3.auth_token = "memory_only_token"
api3.user_data = {"name": "Memory User"}

print(f"Auth status with memory-only login: {api3.is_authenticated()}")

# Create new instance to simulate restart
api4 = Api()
auth_status = api4.is_authenticated()
print(f"Auth status after restart (should be false): {auth_status}")

if not auth_status['authenticated']:
    print("✓ CORRECT: Memory-only login was not persisted")
else:
    print("✗ ERROR: Memory-only login was incorrectly persisted")

print("\n=== Test Complete ===")