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

# Global variable to store auth token
AUTH_TOKEN = None

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

def test_auth_me():
    """Test GET /api/auth/me with auth token"""
    print("\n🧪 Testing GET /api/auth/me endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved user profile")
        else:
            print(f"❌ Failed to retrieve user profile. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected user fields
        required_fields = ["id", "username", "email", "role"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ User profile contains all required fields")
            print(f"✅ Username: {data['username']}, Role: {data['role']}")
        else:
            print(f"❌ User profile is missing required fields: {missing_fields}")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to auth/me endpoint: {e}")
        return False

def test_content_home():
    """Test GET /api/content/home endpoint"""
    print("\n🧪 Testing GET /api/content/home endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/content/home")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved home page content")
        else:
            print(f"❌ Failed to retrieve home page content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} content sections")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are content sections, print them
        if data:
            print(f"📊 Content sections:")
            for i, section in enumerate(data):
                print(f"  {i+1}. Page: {section.get('page')}, Section: {section.get('section')}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to content/home endpoint: {e}")
        return False

def test_update_content_section():
    """Test PUT /api/content/home/hero endpoint"""
    print("\n🧪 Testing PUT /api/content/home/hero endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Create payload
        payload = {
            "content": {
                "title": "Willkommen bei Jimmy's Tapas Bar",
                "subtitle": "Die beste spanische Küche in der Stadt",
                "description": "Genießen Sie authentische spanische Tapas in gemütlicher Atmosphäre."
            },
            "images": []
        }
        
        # Make PUT request
        response = requests.put(f"{API_BASE_URL}/content/home/hero", json=payload, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully updated home hero section")
        else:
            print(f"❌ Failed to update home hero section. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "page", "section", "content", "updated_at", "updated_by"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if content matches what we sent
        if data["content"] == payload["content"]:
            print("✅ Returned content matches input")
        else:
            print(f"❌ Returned content doesn't match input")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to content update endpoint: {e}")
        return False

def test_get_menu_items():
    """Test GET /api/menu/items endpoint"""
    print("\n🧪 Testing GET /api/menu/items endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/menu/items")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved menu items")
        else:
            print(f"❌ Failed to retrieve menu items. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} menu items")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are menu items, verify the structure of the first one
        if data:
            required_fields = ["id", "name", "description", "price", "category"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Menu item objects contain all required fields")
            else:
                print(f"❌ Menu item objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample menu items:")
            for i, item in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {item['name']} - {item['price']} ({item['category']})")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to menu/items endpoint: {e}")
        return False

def test_create_menu_item():
    """Test POST /api/menu/items endpoint"""
    print("\n🧪 Testing POST /api/menu/items endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Create payload
        payload = {
            "name": "Patatas Bravas Especiales",
            "description": "Knusprige Kartoffelwürfel mit scharfer Tomatensoße und Aioli",
            "price": "6,90 €",
            "category": "Tapas Vegetarian",
            "vegetarian": True,
            "vegan": False,
            "glutenfree": True,
            "order_index": 10
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/menu/items", json=payload, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created new menu item")
        else:
            print(f"❌ Failed to create menu item. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains expected fields
        required_fields = ["id", "name", "description", "price", "category", "vegetarian", "vegan", "glutenfree"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False, None
        
        # Check if fields match what we sent
        if (data["name"] == payload["name"] and 
            data["description"] == payload["description"] and
            data["price"] == payload["price"] and
            data["category"] == payload["category"]):
            print("✅ Returned menu item data matches input")
        else:
            print(f"❌ Returned menu item data doesn't match input")
            return False, None
            
        return True, data["id"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create menu item endpoint: {e}")
        return False, None

def test_create_review():
    """Test POST /api/reviews endpoint"""
    print("\n🧪 Testing POST /api/reviews endpoint...")
    
    try:
        # Create payload
        payload = {
            "customer_name": "Maria García",
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
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to pending reviews endpoint: {e}")
        return False

def test_create_contact_message():
    """Test POST /api/contact endpoint"""
    print("\n🧪 Testing POST /api/contact endpoint...")
    
    try:
        # Create payload
        payload = {
            "name": "Carlos Rodríguez",
            "email": "carlos.rodriguez@example.com",
            "phone": "+49 176 12345678",
            "subject": "Reservierung für Samstag",
            "message": "Hallo, ich möchte gerne einen Tisch für 6 Personen am Samstag um 20 Uhr reservieren. Vielen Dank!"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/contact", json=payload)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created new contact message")
        else:
            print(f"❌ Failed to create contact message. Status code: {response.status_code}")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains expected fields
        required_fields = ["id", "name", "email", "subject", "message", "date", "is_read", "responded"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False, None
        
        # Check if fields match what we sent
        if (data["name"] == payload["name"] and 
            data["email"] == payload["email"] and
            data["subject"] == payload["subject"] and
            data["message"] == payload["message"]):
            print("✅ Returned contact message data matches input")
        else:
            print(f"❌ Returned contact message data doesn't match input")
            return False, None
            
        # Check if message is not read by default
        if data["is_read"] == False and data["responded"] == False:
            print("✅ Contact message is not read and not responded by default as expected")
        else:
            print("❌ Contact message has unexpected default values for is_read or responded")
            
        return True, data["id"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create contact message endpoint: {e}")
        return False, None

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
            required_fields = ["id", "name", "email", "subject", "message", "date", "is_read", "responded"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Contact message objects contain all required fields")
            else:
                print(f"❌ Contact message objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample contact messages:")
            for i, message in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {message['name']} - {message['subject']} - Read: {message['is_read']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to contact messages endpoint: {e}")
        return False

def test_get_maintenance_status():
    """Test GET /api/maintenance endpoint"""
    print("\n🧪 Testing GET /api/maintenance endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/maintenance")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved maintenance status")
        else:
            print(f"❌ Failed to retrieve maintenance status. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["is_active", "message"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
            print(f"✅ Maintenance mode is {'active' if data['is_active'] else 'inactive'}")
            print(f"✅ Message: {data['message']}")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to maintenance endpoint: {e}")
        return False

def test_update_maintenance_mode():
    """Test PUT /api/admin/maintenance endpoint"""
    print("\n🧪 Testing PUT /api/admin/maintenance endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Get current maintenance status first
        current_response = requests.get(f"{API_BASE_URL}/maintenance")
        current_data = current_response.json()
        current_status = current_data.get("is_active", False)
        
        # Create payload with opposite status
        payload = {
            "is_active": not current_status,
            "message": "Die Website befindet sich derzeit im Wartungsmodus für Systemupdates."
        }
        
        # Make PUT request
        response = requests.put(f"{API_BASE_URL}/admin/maintenance", json=payload, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print(f"✅ Successfully {'activated' if payload['is_active'] else 'deactivated'} maintenance mode")
        else:
            print(f"❌ Failed to update maintenance mode. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["is_active", "message", "activated_by", "activated_at"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if status matches what we sent
        if data["is_active"] == payload["is_active"] and data["message"] == payload["message"]:
            print("✅ Returned maintenance status matches input")
            print(f"✅ Activated by: {data['activated_by']}")
        else:
            print(f"❌ Returned maintenance status doesn't match input")
            return False
            
        # Now set it back to original state
        restore_payload = {
            "is_active": current_status,
            "message": current_data.get("message", "Die Website befindet sich derzeit im Wartungsmodus.")
        }
        
        restore_response = requests.put(f"{API_BASE_URL}/admin/maintenance", json=restore_payload, headers=headers)
        if restore_response.status_code == 200:
            print(f"✅ Successfully restored maintenance mode to original state")
        else:
            print(f"❌ Failed to restore maintenance mode. Status code: {restore_response.status_code}")
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to update maintenance endpoint: {e}")
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

def test_create_user():
    """Test POST /api/users endpoint"""
    print("\n🧪 Testing POST /api/users endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Create a unique username with timestamp
        timestamp = int(time.time())
        
        # Create payload
        payload = {
            "username": f"editor{timestamp}",
            "email": f"editor{timestamp}@jimmys-tapasbar.de",
            "password": "securePassword123!",
            "role": "editor"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/users", json=payload, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created new user")
        else:
            print(f"❌ Failed to create user. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            elif response.status_code == 400:
                print("   Bad request: Username might already exist")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains expected fields
        required_fields = ["id", "username", "email", "role", "is_active"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False, None
        
        # Check if fields match what we sent
        if (data["username"] == payload["username"] and 
            data["email"] == payload["email"] and
            data["role"] == payload["role"]):
            print("✅ Returned user data matches input")
        else:
            print(f"❌ Returned user data doesn't match input")
            return False, None
            
        # Check if user is active by default
        if data["is_active"] == True:
            print("✅ User is active by default as expected")
        else:
            print("❌ User is not active by default, which is unexpected")
            
        return True, data["id"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create user endpoint: {e}")
        return False, None

def test_unauthorized_access():
    """Test unauthorized access to protected endpoints"""
    print("\n🧪 Testing unauthorized access to protected endpoints...")
    
    # List of protected endpoints to test
    protected_endpoints = [
        {"method": "get", "url": f"{API_BASE_URL}/auth/me", "name": "Get user profile"},
        {"method": "get", "url": f"{API_BASE_URL}/users", "name": "Get users"},
        {"method": "get", "url": f"{API_BASE_URL}/admin/reviews/pending", "name": "Get pending reviews"},
        {"method": "get", "url": f"{API_BASE_URL}/admin/contact", "name": "Get contact messages"}
    ]
    
    results = {}
    
    for endpoint in protected_endpoints:
        print(f"\n  Testing unauthorized access to: {endpoint['name']}")
        
        try:
            # Make request without auth token
            if endpoint["method"] == "get":
                response = requests.get(endpoint["url"])
            elif endpoint["method"] == "post":
                response = requests.post(endpoint["url"], json={})
            elif endpoint["method"] == "put":
                response = requests.put(endpoint["url"], json={})
            
            # Check if response is 401 Unauthorized
            if response.status_code == 401:
                print(f"✅ {endpoint['name']} correctly returned 401 Unauthorized")
                results[endpoint["name"]] = True
            else:
                print(f"❌ {endpoint['name']} returned {response.status_code} instead of 401 Unauthorized")
                results[endpoint["name"]] = False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error connecting to {endpoint['name']}: {e}")
            results[endpoint["name"]] = False
    
    # Check overall result
    all_passed = all(results.values())
    if all_passed:
        print("\n✅ All unauthorized access tests passed")
    else:
        print("\n❌ Some unauthorized access tests failed")
        
    return all_passed

def run_all_tests():
    """Run all tests and return overall result"""
    print("\n🔍 Starting Jimmy's Tapas Bar CMS Backend API Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: Root endpoint
    results["root_endpoint"] = test_root_endpoint()
    
    # Test 2: Authentication
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    if auth_success:
        results["auth_me"] = test_auth_me()
    else:
        results["auth_me"] = False
        print("❌ Skipping auth/me test due to failed login")
    
    # Test 3: Content Management
    results["content_home"] = test_content_home()
    
    if auth_success:
        results["update_content"] = test_update_content_section()
    else:
        results["update_content"] = False
        print("❌ Skipping content update test due to failed login")
    
    # Test 4: Menu Management
    results["get_menu_items"] = test_get_menu_items()
    
    if auth_success:
        menu_success, menu_id = test_create_menu_item()
        results["create_menu_item"] = menu_success
    else:
        results["create_menu_item"] = False
        print("❌ Skipping menu item creation test due to failed login")
    
    # Test 5: Review Management
    review_success, review_id = test_create_review()
    results["create_review"] = review_success
    
    if auth_success:
        results["get_pending_reviews"] = test_get_pending_reviews()
    else:
        results["get_pending_reviews"] = False
        print("❌ Skipping pending reviews test due to failed login")
    
    # Test 6: Contact Messages
    contact_success, contact_id = test_create_contact_message()
    results["create_contact"] = contact_success
    
    if auth_success:
        results["get_contact_messages"] = test_get_contact_messages()
    else:
        results["get_contact_messages"] = False
        print("❌ Skipping contact messages test due to failed login")
    
    # Test 7: Maintenance Mode
    results["get_maintenance"] = test_get_maintenance_status()
    
    if auth_success:
        results["update_maintenance"] = test_update_maintenance_mode()
    else:
        results["update_maintenance"] = False
        print("❌ Skipping maintenance mode update test due to failed login")
    
    # Test 8: User Management
    if auth_success:
        results["get_users"] = test_get_users()
        user_success, user_id = test_create_user()
        results["create_user"] = user_success
    else:
        results["get_users"] = False
        results["create_user"] = False
        print("❌ Skipping user management tests due to failed login")
    
    # Test 9: Unauthorized Access
    results["unauthorized_access"] = test_unauthorized_access()
    
    # Test 10: Basic endpoints
    results["create_status"], status_id = test_create_status_check()
    results["get_status"] = test_get_status_checks()
    results["cors"] = test_cors_configuration()
    
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

def run_admin_login_tests():
    """Run specific tests for admin login system"""
    print("\n🔍 Starting Jimmy's Tapas Bar Admin Login System Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: Authentication login
    auth_success, token = test_auth_login()
    results["admin_login"] = auth_success
    
    # Test 2: JWT token validation
    if auth_success:
        results["jwt_token_validation"] = test_auth_me()
    else:
        results["jwt_token_validation"] = False
        print("❌ Skipping JWT token validation test due to failed login")
    
    # Test 3: Admin endpoint access
    if auth_success:
        results["admin_endpoint_access"] = test_get_users()
    else:
        results["admin_endpoint_access"] = False
        print("❌ Skipping admin endpoint access test due to failed login")
    
    # Test 4: CORS configuration
    results["cors_configuration"] = test_cors_configuration()
    
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
    # Run the specific tests for admin login system
    success = run_admin_login_tests()
    sys.exit(0 if success else 1)
