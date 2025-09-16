#!/usr/bin/env python3
"""
Test script to test authentication persistence with real API and credentials
Using real credentials: test@test.com / 123456
"""

import os
import sys
import sqlite3
import json
import time

# Add backend to path to import the main module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the main Api class and config
from main import Api, init_db, db_file, DATA_DIR

print("=== Testing Authentication Persistence with Real API ===")
print(f"Database location: {db_file}")
print(f"Data directory: {DATA_DIR}")
print(f"Database exists: {os.path.exists(db_file)}")
print(f"Data directory exists: {os.path.exists(DATA_DIR)}")

# Initialize the database
init_db()

# Test credentials provided by user
test_email = "test@test.com"
test_password = "123456"

print("\n--- Step 1: Clear any existing auth data ---")
api1 = Api()
api1.clear_auth_data()
print("✓ Cleared existing auth data")

# Check initial authentication status
initial_auth = api1.is_authenticated()
print(f"Initial authentication status: {initial_auth}")
assert not initial_auth['authenticated'], "Should not be authenticated initially"

print("\n--- Step 2: Test real login with remember_me=True ---")
try:
    login_result = api1.login(test_email, test_password, remember_me=True)
    print(f"Login result: {login_result}")
    
    if login_result.get('success'):
        print("✓ Login successful!")
        
        # Check if authentication data is set in memory
        auth_after_login = api1.is_authenticated()
        print(f"Auth status after login: {auth_after_login}")
        
        if auth_after_login['authenticated']:
            print("✓ Authentication set in memory")
            
            # Get current user data
            user_data = api1.get_current_user()
            print(f"Current user data: {user_data}")
            
            # Check if data was saved to database
            try:
                with sqlite3.connect(db_file) as conn:
                    c = conn.cursor()
                    c.execute('SELECT token, user_data FROM auth_data ORDER BY id DESC LIMIT 1')
                    result = c.fetchone()
                    if result:
                        print(f"✓ Auth data saved to database")
                        print(f"  Token (first 20 chars): {result[0][:20]}...")
                        saved_user_data = json.loads(result[1])
                        print(f"  User data: {saved_user_data}")
                    else:
                        print("✗ No auth data found in database!")
                        sys.exit(1)
            except Exception as db_error:
                print(f"✗ Database error: {db_error}")
                sys.exit(1)
                
        else:
            print("✗ Authentication not set in memory after login!")
            sys.exit(1)
    else:
        print(f"✗ Login failed: {login_result.get('message', 'Unknown error')}")
        sys.exit(1)
        
except Exception as login_error:
    print(f"✗ Login error: {login_error}")
    sys.exit(1)

print("\n--- Step 3: Test app restart (new Api instance) ---")
# Create a new Api instance to simulate app restart
api2 = Api()

# Check if authentication is restored
auth_after_restart = api2.is_authenticated()
print(f"Auth status after restart: {auth_after_restart}")

if auth_after_restart['authenticated']:
    print("✓ Authentication restored after restart!")
    
    # Get user data
    user_data_after_restart = api2.get_current_user()
    print(f"User data after restart: {user_data_after_restart}")
    
    # Test that we can make authenticated API calls
    try:
        profile_result = api2.get_profile()
        print(f"Profile fetch result: {profile_result}")
        
        if profile_result.get('success'):
            print("✓ Authenticated API call successful after restart!")
        else:
            print(f"✗ Authenticated API call failed: {profile_result.get('message')}")
    except Exception as profile_error:
        print(f"✗ Profile fetch error: {profile_error}")
        
else:
    print("✗ Authentication NOT restored after restart!")
    
    # Debug: Check what's in the database
    try:
        with sqlite3.connect(db_file) as conn:
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM auth_data')
            count = c.fetchone()[0]
            print(f"Database row count: {count}")
            
            if count > 0:
                c.execute('SELECT token, user_data FROM auth_data ORDER BY id DESC LIMIT 1')
                result = c.fetchone()
                if result:
                    print(f"Database contains token: {result[0][:20]}...")
                    print(f"Database contains user data: {result[1][:100]}...")
                    
                    # Try manual load
                    print("Attempting manual load_auth_data()...")
                    manual_load = api2.load_auth_data()
                    print(f"Manual load result: {manual_load}")
                    
                    if manual_load:
                        print(f"After manual load - token set: {api2.auth_token is not None}")
                        print(f"After manual load - user data set: {api2.user_data is not None}")
            else:
                print("Database is empty - data was not saved!")
    except Exception as debug_error:
        print(f"Debug error: {debug_error}")

print("\n--- Step 4: Test login with remember_me=False ---")
api3 = Api()
api3.clear_auth_data()

try:
    login_result_no_remember = api3.login(test_email, test_password, remember_me=False)
    print(f"Login result (remember_me=False): {login_result_no_remember}")
    
    if login_result_no_remember.get('success'):
        print("✓ Login successful with remember_me=False")
        
        # Check database - should be empty
        try:
            with sqlite3.connect(db_file) as conn:
                c = conn.cursor()
                c.execute('SELECT COUNT(*) FROM auth_data')
                count = c.fetchone()[0]
                if count == 0:
                    print("✓ Correctly no data saved to database with remember_me=False")
                else:
                    print("✗ Data was saved to database even with remember_me=False")
        except Exception as db_error:
            print(f"Database check error: {db_error}")
            
        # Simulate restart
        api4 = Api()
        auth_no_remember = api4.is_authenticated()
        if not auth_no_remember['authenticated']:
            print("✓ Correctly not authenticated after restart with remember_me=False")
        else:
            print("✗ Incorrectly still authenticated after restart with remember_me=False")
    else:
        print(f"✗ Login failed with remember_me=False: {login_result_no_remember.get('message')}")
        
except Exception as no_remember_error:
    print(f"Login error (remember_me=False): {no_remember_error}")

print("\n--- Step 5: Final database and file system checks ---")
print(f"Database file exists: {os.path.exists(db_file)}")
print(f"Database file readable: {os.access(db_file, os.R_OK)}")
print(f"Database file writable: {os.access(db_file, os.W_OK)}")
print(f"Data directory readable: {os.access(DATA_DIR, os.R_OK)}")
print(f"Data directory writable: {os.access(DATA_DIR, os.W_OK)}")

# Check database content one more time
try:
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        
        # Check if table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_data';")
        table_exists = c.fetchone()
        print(f"Auth table exists: {table_exists is not None}")
        
        if table_exists:
            c.execute('SELECT COUNT(*) FROM auth_data')
            count = c.fetchone()[0]
            print(f"Final auth data row count: {count}")
            
            if count > 0:
                c.execute('SELECT id, token, user_data FROM auth_data ORDER BY id DESC LIMIT 1')
                result = c.fetchone()
                if result:
                    print(f"Final auth data:")
                    print(f"  ID: {result[0]}")
                    print(f"  Token: {result[1][:30]}...")
                    print(f"  User data: {result[2][:100]}...")
except Exception as final_db_error:
    print(f"Final database check error: {final_db_error}")

print("\n=== Test Complete ===")
print("Check the output above to see if authentication persistence is working correctly.")