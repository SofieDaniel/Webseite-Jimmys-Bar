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
BACKEND_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://a35db976-944a-4ad4-bf66-aeabec535032.preview.emergentagent.com")
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Using backend URL: {BACKEND_URL}")

# Spanish restaurant client names for testing
SPANISH_CLIENTS = [
    "Tapas Delight",
    "Paella Paradise",
    "El Rincón de Sevilla",
    "Barcelona Bistro",
    "Madrid Mariscos",
    "Valencia Vino",
    "Flamenco Fusion",
    "Catalonia Cuisine",
    "Andalusia Appetizers",
    "Iberian Inspirations"
]

def test_root_endpoint():
    """Test the root endpoint GET /api/"""
    print("\n🧪 Testing GET /api/ endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Root endpoint returned status code 200")
        else:
            print(f"❌ Root endpoint returned unexpected status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected message
        if "message" in data and data["message"] == "Hello World":
            print("✅ Response contains expected 'Hello World' message")
        else:
            print("❌ Response does not contain expected 'Hello World' message")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to root endpoint: {e}")
        return False

def test_create_status_check():
    """Test POST /api/status to create a status check"""
    print("\n🧪 Testing POST /api/status endpoint...")
    
    # Use a random Spanish restaurant name
    client_name = SPANISH_CLIENTS[int(time.time()) % len(SPANISH_CLIENTS)]
    
    try:
        # Create payload
        payload = {"client_name": client_name}
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/status", json=payload)
        
        # Check if response is successful
        if response.status_code == 200:
            print(f"✅ Successfully created status check for '{client_name}'")
        else:
            print(f"❌ Failed to create status check. Status code: {response.status_code}")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains expected fields
        required_fields = ["id", "client_name", "timestamp"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False, None
        
        # Check if client_name matches what we sent
        if data["client_name"] == client_name:
            print("✅ Returned client_name matches input")
        else:
            print(f"❌ Returned client_name '{data['client_name']}' doesn't match input '{client_name}'")
            return False, None
            
        return True, data["id"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create status endpoint: {e}")
        return False, None

def test_get_status_checks():
    """Test GET /api/status to retrieve status checks"""
    print("\n🧪 Testing GET /api/status endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/status")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved status checks")
        else:
            print(f"❌ Failed to retrieve status checks. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} status checks")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are status checks, verify the structure of the first one
        if data:
            required_fields = ["id", "client_name", "timestamp"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Status check objects contain all required fields")
            else:
                print(f"❌ Status check objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample status checks:")
            for i, check in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {check['client_name']} (ID: {check['id']}, Time: {check['timestamp']})")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to get status endpoint: {e}")
        return False

def test_cors_configuration():
    """Test that CORS is properly configured"""
    print("\n🧪 Testing CORS configuration...")
    
    try:
        # Make OPTIONS request to check CORS headers with verbose output
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options(f"{API_BASE_URL}/", headers=headers)
        
        print(f"Response status code: {response.status_code}")
        print("Response headers:")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")
        
        # Check if response contains CORS headers
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers'
        ]
        
        missing_headers = [header for header in cors_headers if header not in response.headers]
        
        if not missing_headers:
            print("✅ CORS headers are properly configured")
            print(f"  - Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
            print(f"  - Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods')}")
            print(f"  - Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers')}")
            return True
        else:
            print(f"❌ Missing CORS headers: {missing_headers}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing CORS configuration: {e}")
        return False

def run_all_tests():
    """Run all tests and return overall result"""
    print("\n🔍 Starting Jimmy's Tapas Bar Backend API Tests")
    print("=" * 60)
    
    # Track test results
    results = {}
    
    # Test 1: Root endpoint
    results["root_endpoint"] = test_root_endpoint()
    
    # Test 2: Create status check
    results["create_status"], status_id = test_create_status_check()
    
    # Test 3: Test with specific Spanish restaurant name
    # Use the specific Spanish restaurant name
    client_name = "Reserva Mesa Paella"
    print(f"\n🧪 Testing POST /api/status with '{client_name}'...")
    
    try:
        # Create payload
        payload = {"client_name": client_name}
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/status", json=payload)
        
        # Check if response is successful
        if response.status_code == 200:
            print(f"✅ Successfully created status check for '{client_name}'")
            results["specific_spanish_restaurant"] = True
        else:
            print(f"❌ Failed to create status check. Status code: {response.status_code}")
            results["specific_spanish_restaurant"] = False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            results["specific_spanish_restaurant"] = False
        
        # Check if response contains expected fields
        required_fields = ["id", "client_name", "timestamp"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            results["specific_spanish_restaurant"] = False
        
        # Check if client_name matches what we sent
        if data["client_name"] == client_name:
            print("✅ Returned client_name matches input")
        else:
            print(f"❌ Returned client_name '{data['client_name']}' doesn't match input '{client_name}'")
            results["specific_spanish_restaurant"] = False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create status endpoint: {e}")
        results["specific_spanish_restaurant"] = False
    
    # Test 4: Get status checks
    results["get_status"] = test_get_status_checks()
    
    # Test 5: CORS configuration
    results["cors"] = test_cors_configuration()
    
    # Print summary
    print("\n📋 Test Summary")
    print("=" * 60)
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Overall result
    all_passed = all(results.values())
    print("\n🏁 Overall Result:", "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
