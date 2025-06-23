#!/usr/bin/env python3
import requests
import json
import time
import sys
from datetime import datetime
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

def test_create_review():
    """Test POST /api/reviews endpoint"""
    print("\n🧪 Testing POST /api/reviews endpoint...")
    
    try:
        # Create payload
        payload = {
            "customer_name": "Elena Rodríguez",
            "rating": 5,
            "comment": "¡Excelente comida! Las tapas son auténticas y el ambiente es muy acogedor. Volveré pronto."
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/reviews", json=payload)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created new review")
        else:
            print(f"❌ Failed to create review. Status code: {response.status_code}")
            if response.status_code == 500:
                print(f"   Server error: {response.text}")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains expected fields
        required_fields = ["id", "customer_name", "rating", "comment", "date", "is_approved"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False, None
        
        # Check if fields match what we sent
        if (data["customer_name"] == payload["customer_name"] and 
            data["rating"] == payload["rating"] and
            data["comment"] == payload["comment"]):
            print("✅ Returned review data matches input")
        else:
            print(f"❌ Returned review data doesn't match input")
            return False, None
            
        # Check if review is not approved by default
        if data["is_approved"] == False:
            print("✅ Review is not approved by default as expected")
        else:
            print("❌ Review is approved by default, which is unexpected")
            
        return True, data["id"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create review endpoint: {e}")
        return False, None

def test_get_reviews(approved_only=True):
    """Test GET /api/reviews endpoint"""
    print(f"\n🧪 Testing GET /api/reviews endpoint with approved_only={approved_only}...")
    
    try:
        # Make GET request with approved_only parameter
        response = requests.get(f"{API_BASE_URL}/reviews?approved_only={str(approved_only).lower()}")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved reviews")
        else:
            print(f"❌ Failed to retrieve reviews. Status code: {response.status_code}")
            if response.status_code == 500:
                print(f"   Server error: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} reviews")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are reviews, verify the structure of the first one
        if data:
            required_fields = ["id", "customer_name", "rating", "comment", "date", "is_approved"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Review objects contain all required fields")
            else:
                print(f"❌ Review objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample reviews:")
            for i, review in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {review['customer_name']} - {review['rating']}★ - {review['comment'][:30]}...")
                
            # If approved_only is True, verify all reviews are approved
            if approved_only:
                all_approved = all(review["is_approved"] for review in data)
                if all_approved:
                    print("✅ All reviews are correctly marked as approved")
                else:
                    print("❌ Some reviews are marked as not approved in the approved reviews list")
                    return False
                    
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to reviews endpoint: {e}")
        return False

def test_get_pending_reviews():
    """Test GET /api/admin/reviews/pending endpoint"""
    print("\n🧪 Testing GET /api/admin/reviews/pending endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/reviews/pending", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved pending reviews")
        else:
            print(f"❌ Failed to retrieve pending reviews. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            elif response.status_code == 500:
                print(f"   Server error: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} pending reviews")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are pending reviews, verify the structure of the first one
        if data:
            required_fields = ["id", "customer_name", "rating", "comment", "date", "is_approved"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Review objects contain all required fields")
            else:
                print(f"❌ Review objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample pending reviews:")
            for i, review in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {review['customer_name']} - {review['rating']}★ - {review['comment'][:30]}...")
                
            # Verify all reviews are not approved
            all_pending = all(not review["is_approved"] for review in data)
            if all_pending:
                print("✅ All reviews are correctly marked as not approved")
            else:
                print("❌ Some reviews are marked as approved in the pending reviews list")
                return False
                
            # Return the ID of the first pending review for approval testing
            return True, data[0]["id"] if data else None
        
        return True, None
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to pending reviews endpoint: {e}")
        return False, None

def test_approve_review(review_id):
    """Test PUT /api/reviews/{id}/approve endpoint"""
    print(f"\n🧪 Testing PUT /api/reviews/{review_id}/approve endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    if not review_id:
        print("❌ No review ID provided. Cannot test approval.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make PUT request
        response = requests.put(f"{API_BASE_URL}/reviews/{review_id}/approve", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully approved review")
        else:
            print(f"❌ Failed to approve review. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            elif response.status_code == 404:
                print("   Review not found")
            elif response.status_code == 500:
                print(f"   Server error: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains success message
        if "message" in data and "approved" in data["message"].lower():
            print(f"✅ Response contains success message: {data['message']}")
        else:
            print(f"❌ Response does not contain expected success message")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to approve review endpoint: {e}")
        return False

def run_review_tests():
    """Run all review-related tests"""
    print("\n🔍 Starting Jimmy's Tapas Bar Review System Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: Create a new review
    review_success, review_id = test_create_review()
    results["create_review"] = review_success
    
    # Test 2: Get reviews with approved_only=true
    results["get_reviews_approved"] = test_get_reviews(approved_only=True)
    
    # Test 3: Get reviews with approved_only=false
    results["get_reviews_all"] = test_get_reviews(approved_only=False)
    
    # Test 4: Authentication for admin endpoints
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    # Test 5: Get pending reviews
    if auth_success:
        pending_success, pending_id = test_get_pending_reviews()
        results["get_pending_reviews"] = pending_success
        
        # Test 6: Approve a review
        if pending_success and pending_id:
            results["approve_review"] = test_approve_review(pending_id)
        else:
            # If no pending reviews, try to approve the one we just created
            if review_success and review_id:
                results["approve_review"] = test_approve_review(review_id)
            else:
                results["approve_review"] = False
                print("❌ Skipping review approval test due to no available reviews")
    else:
        results["get_pending_reviews"] = False
        results["approve_review"] = False
        print("❌ Skipping admin review tests due to failed login")
    
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
    run_review_tests()