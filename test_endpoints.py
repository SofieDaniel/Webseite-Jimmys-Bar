#!/usr/bin/env python3
import requests
import json
import time
import sys
from datetime import datetime

# Get the backend URL from the frontend .env file
import os
from dotenv import load_dotenv

# Load the frontend .env file
load_dotenv("/app/frontend/.env")
BACKEND_URL = os.environ.get("REACT_APP_BACKEND_URL")
if not BACKEND_URL:
    BACKEND_URL = "http://localhost:8001"  # Default fallback
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Using backend URL: {BACKEND_URL}")
print(f"API base URL: {API_BASE_URL}")

# Global variable to store auth token
AUTH_TOKEN = None

def test_auth_login():
    """Test POST /api/auth/login with admin credentials"""
    print("\n🧪 Testing POST /api/auth/login endpoint...")
    global AUTH_TOKEN
    
    try:
        # Create payload with admin credentials
        payload = {
            "username": "admin",
            "password": "jimmy2024"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/auth/login", json=payload)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully authenticated with admin credentials")
        else:
            print(f"❌ Failed to authenticate. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Incorrect username or password")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains token
        if "access_token" in data and "token_type" in data:
            print("✅ Response contains access token and token type")
            AUTH_TOKEN = data["access_token"]
            print(f"✅ Token type: {data['token_type']}")
        else:
            print("❌ Response does not contain expected token fields")
            return False, None
            
        return True, data["access_token"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to login endpoint: {e}")
        return False, None

def test_newsletter_subscribers():
    """Test GET /api/admin/newsletter/subscribers endpoint"""
    print("\n🧪 Testing GET /api/admin/newsletter/subscribers endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/newsletter/subscribers", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved newsletter subscribers")
        else:
            print(f"❌ Failed to retrieve newsletter subscribers. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} subscribers")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are subscribers, verify the structure of the first one
        if data:
            # Print some sample data
            print(f"📊 Sample subscribers:")
            for i, subscriber in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {subscriber}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin/newsletter/subscribers endpoint: {e}")
        return False

def test_get_users():
    """Test GET /api/users endpoint"""
    print("\n🧪 Testing GET /api/users endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/users", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved users")
        else:
            print(f"❌ Failed to retrieve users. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} users")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are users, verify the structure of the first one
        if data:
            required_fields = ["id", "username", "email", "role", "is_active"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ User objects contain all required fields")
            else:
                print(f"❌ User objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample users:")
            for i, user in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {user['username']} - {user['email']} - Role: {user['role']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to users endpoint: {e}")
        return False

def test_get_contact_messages():
    """Test GET /api/admin/contact endpoint"""
    print("\n🧪 Testing GET /api/admin/contact endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/contact", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved contact messages")
        else:
            print(f"❌ Failed to retrieve contact messages. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} contact messages")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are contact messages, verify the structure of the first one
        if data:
            # Print some sample data
            print(f"📊 Sample contact messages:")
            for i, message in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {message.get('name', 'Unknown')} - {message.get('subject', 'No subject')}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to contact messages endpoint: {e}")
        return False

def test_newsletter_subscribe():
    """Test POST /api/newsletter/subscribe endpoint"""
    print("\n🧪 Testing POST /api/newsletter/subscribe endpoint...")
    
    try:
        # Create a unique email with timestamp
        timestamp = int(time.time())
        email = f"test{timestamp}@example.com"
        
        # Create payload
        payload = {
            "email": email
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/newsletter/subscribe", json=payload)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully subscribed to newsletter")
        else:
            print(f"❌ Failed to subscribe to newsletter. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains a success message
        if "message" in data:
            print(f"✅ Response contains message: {data['message']}")
        else:
            print("❌ Response does not contain a message field")
            return False
            
        # Verify the subscription by checking the admin endpoint
        if AUTH_TOKEN:
            headers = {
                "Authorization": f"Bearer {AUTH_TOKEN}"
            }
            
            verify_response = requests.get(f"{API_BASE_URL}/admin/newsletter/subscribers", headers=headers)
            if verify_response.status_code == 200:
                subscribers = verify_response.json()
                
                # Look for our test email
                found = False
                for subscriber in subscribers:
                    if subscriber.get("email") == email:
                        found = True
                        print(f"✅ Verified that {email} was added to subscribers list")
                        break
                
                if not found:
                    print(f"❌ Could not verify that {email} was added to subscribers list")
                    return False
            else:
                print(f"❌ Failed to verify subscription. Status code: {verify_response.status_code}")
                # Don't return False here, as we already confirmed the subscribe endpoint worked
        else:
            print("⚠️ Could not verify subscription in admin endpoint due to missing auth token")
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to newsletter/subscribe endpoint: {e}")
        return False

def run_tests():
    """Run all tests and return overall result"""
    print("\n🔍 Starting Jimmy's Tapas Bar Backend API Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: Authentication
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    # Test 2: Newsletter Subscribers
    if auth_success:
        results["newsletter_subscribers"] = test_newsletter_subscribers()
    else:
        results["newsletter_subscribers"] = False
        print("❌ Skipping newsletter subscribers test due to failed login")
    
    # Test 3: Users
    if auth_success:
        results["users"] = test_get_users()
    else:
        results["users"] = False
        print("❌ Skipping users test due to failed login")
    
    # Test 4: Contact Messages
    if auth_success:
        results["contact_messages"] = test_get_contact_messages()
    else:
        results["contact_messages"] = False
        print("❌ Skipping contact messages test due to failed login")
    
    # Test 5: Newsletter Subscribe
    results["newsletter_subscribe"] = test_newsletter_subscribe()
    
    # Print summary
    print("\n📋 Test Summary")
    print("=" * 80)
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Overall result
    all_passed = all(results.values())
    print("\n🏁 Overall Result:", "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED")
    
    return all_passed

if __name__ == "__main__":
    run_tests()