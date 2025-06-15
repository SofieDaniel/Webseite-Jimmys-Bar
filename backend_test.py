#!/usr/bin/env python3
import requests
import json
import time
import sys
import uuid
from datetime import datetime

# Get the backend URL from the frontend .env file
import os
from dotenv import load_dotenv

# Load the frontend .env file
load_dotenv("/app/frontend/.env")
BACKEND_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://974f34a6-6eef-4313-b696-dc3bb4a9db65.preview.emergentagent.com")
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

# Test email addresses for newsletter
TEST_EMAILS = [
    "test.user@example.com",
    "maria.garcia@example.es",
    "juan.rodriguez@example.com",
    "carmen.lopez@example.es",
    "antonio.martinez@example.com"
]

# Global variables to store tokens and IDs
AUTH_TOKEN = None
NEWSLETTER_TOKEN = None
MENU_ITEM_ID = None

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
        {"method": "get", "url": f"{API_BASE_URL}/admin/contact", "name": "Get contact messages"},
        {"method": "get", "url": f"{API_BASE_URL}/admin/newsletter/subscribers", "name": "Get newsletter subscribers"},
        {"method": "get", "url": f"{API_BASE_URL}/admin/newsletter/smtp", "name": "Get SMTP configuration"},
        {"method": "get", "url": f"{API_BASE_URL}/admin/newsletter/templates", "name": "Get newsletter templates"},
        {"method": "get", "url": f"{API_BASE_URL}/admin/newsletter/campaigns", "name": "Get newsletter campaigns"}
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

def test_admin_route_access():
    """Test direct access to admin route via HTTP"""
    print("\n🧪 Testing direct access to /admin route...")
    
    try:
        # Make GET request to the admin route
        response = requests.get(f"{BACKEND_URL}/admin")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully accessed admin route")
        else:
            print(f"❌ Failed to access admin route. Status code: {response.status_code}")
            return False
        
        # Check if response contains admin login page content
        content = response.text.lower()
        
        # Check if we're getting the main site content or admin login
        if "cms login" in content and "jimmy's tapas bar verwaltung" in content:
            print("✅ Response contains admin login page content")
            
            # Check that the main site header is not present
            if "speisekarte" in content and "startseite" in content and "kontakt" in content:
                print("❌ Main site header is present in admin page")
                return False
            else:
                print("✅ Admin route is properly isolated from main site layout")
                return True
        else:
            # We're not getting the admin login page
            print("❌ Admin login page not found in response")
            
            # Check if we're getting the main site or just the base HTML
            if "jimmy's" in content and "tapas bar" in content:
                print("❌ Main site content is being returned instead of admin login")
            else:
                print("❌ Neither admin login nor main site content found - likely a client-side routing issue")
                print("   The server is returning the base HTML without the admin component being rendered")
            
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin route: {e}")
        return False

def test_admin_api_integration():
    """Test that admin panel can communicate with backend APIs"""
    print("\n🧪 Testing admin panel API integration...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Test a few admin-specific API endpoints
        endpoints = [
            {"url": f"{API_BASE_URL}/admin/reviews/pending", "name": "Pending Reviews"},
            {"url": f"{API_BASE_URL}/admin/contact", "name": "Contact Messages"},
            {"url": f"{API_BASE_URL}/admin/maintenance", "name": "Maintenance Mode"}
        ]
        
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        all_successful = True
        
        for endpoint in endpoints:
            response = requests.get(endpoint["url"], headers=headers)
            
            if response.status_code == 200:
                print(f"✅ Successfully accessed {endpoint['name']} API")
                
                # Check if response is valid JSON
                try:
                    data = response.json()
                    print(f"  ✅ Response is valid JSON")
                except json.JSONDecodeError:
                    print(f"  ❌ Response is not valid JSON")
                    all_successful = False
            else:
                print(f"❌ Failed to access {endpoint['name']} API. Status code: {response.status_code}")
                all_successful = False
        
        return all_successful
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing admin API integration: {e}")
        return False

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

def run_admin_route_tests():
    """Run tests for admin route functionality"""
    print("\n🔍 Starting Jimmy's Tapas Bar Admin Route Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: Admin Route Access
    results["admin_route_access"] = test_admin_route_access()
    
    # Test 2: Authentication login
    auth_success, token = test_auth_login()
    results["admin_login"] = auth_success
    
    # Test 3: JWT token validation
    if auth_success:
        results["jwt_token_validation"] = test_auth_me()
    else:
        results["jwt_token_validation"] = False
        print("❌ Skipping JWT token validation test due to failed login")
    
    # Test 4: Admin API Integration
    if auth_success:
        results["admin_api_integration"] = test_admin_api_integration()
    else:
        results["admin_api_integration"] = False
        print("❌ Skipping admin API integration test due to failed login")
    
    # Test 5: Unauthorized Access
    results["unauthorized_access"] = test_unauthorized_access()
    
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

# Newsletter System Tests
def test_newsletter_subscribe():
    """Test POST /api/newsletter/subscribe endpoint"""
    print("\n🧪 Testing POST /api/newsletter/subscribe endpoint...")
    
    try:
        # Create payload with a unique email
        timestamp = int(time.time())
        email = f"test.user{timestamp}@example.com"
        payload = {
            "email": email,
            "name": "Test User"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/newsletter/subscribe", json=payload)
        
        # Check if response is successful
        if response.status_code == 200:
            print(f"✅ Successfully subscribed to newsletter with email: {email}")
        else:
            print(f"❌ Failed to subscribe to newsletter. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains success message
        if "message" in data:
            print(f"✅ Response contains message: {data['message']}")
        else:
            print("❌ Response does not contain a message")
            return False, None
            
        return True, email
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to newsletter subscribe endpoint: {e}")
        return False, None

def test_get_newsletter_subscribers():
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
            print(f"   Response: {response.text}")
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
            required_fields = ["id", "email", "subscribed_at", "is_active", "unsubscribe_token"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Subscriber objects contain all required fields")
            else:
                print(f"❌ Subscriber objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample subscribers:")
            for i, subscriber in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {subscriber.get('name', 'No name')} - {subscriber['email']} - Active: {subscriber['is_active']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to newsletter subscribers endpoint: {e}")
        return False

def test_get_smtp_config():
    """Test GET /api/admin/newsletter/smtp endpoint"""
    print("\n🧪 Testing GET /api/admin/newsletter/smtp endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/newsletter/smtp", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved SMTP configuration")
        else:
            print(f"❌ Failed to retrieve SMTP configuration. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # If no SMTP config exists, the response should contain a message
        if "message" in data and data["message"] == "Keine SMTP-Konfiguration gefunden":
            print("✅ No SMTP configuration found (expected message)")
            return True
        
        # If SMTP config exists, check required fields
        required_fields = ["host", "port", "username", "from_email", "from_name"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ SMTP configuration contains all required fields")
        else:
            print(f"❌ SMTP configuration is missing required fields: {missing_fields}")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to SMTP configuration endpoint: {e}")
        return False

def test_create_smtp_config():
    """Test POST /api/admin/newsletter/smtp endpoint"""
    print("\n🧪 Testing POST /api/admin/newsletter/smtp endpoint...")
    
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
            "host": "smtp.example.com",
            "port": 587,
            "username": "test@example.com",
            "password": "securePassword123!",
            "use_tls": True,
            "from_email": "newsletter@jimmys-tapasbar.de",
            "from_name": "Jimmy's Tapas Bar"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/admin/newsletter/smtp", json=payload, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created SMTP configuration")
        else:
            print(f"❌ Failed to create SMTP configuration. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains success message
        if "message" in data and data["message"] == "SMTP-Konfiguration erfolgreich erstellt":
            print("✅ Response contains success message")
        else:
            print("❌ Response does not contain expected success message")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create SMTP configuration endpoint: {e}")
        return False

def test_get_newsletter_templates():
    """Test GET /api/admin/newsletter/templates endpoint"""
    print("\n🧪 Testing GET /api/admin/newsletter/templates endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/newsletter/templates", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved newsletter templates")
        else:
            print(f"❌ Failed to retrieve newsletter templates. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} templates")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are templates, verify the structure of the first one
        if data:
            required_fields = ["id", "name", "subject", "content", "created_at", "created_by", "is_active"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Template objects contain all required fields")
            else:
                print(f"❌ Template objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample templates:")
            for i, template in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {template['name']} - {template['subject']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to newsletter templates endpoint: {e}")
        return False

def test_create_newsletter_template():
    """Test POST /api/admin/newsletter/templates endpoint"""
    print("\n🧪 Testing POST /api/admin/newsletter/templates endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Create a unique template name with timestamp
        timestamp = int(time.time())
        
        # Create payload
        payload = {
            "name": f"Test Template {timestamp}",
            "subject": "Willkommen bei Jimmy's Tapas Bar Newsletter",
            "content": "<h1>Willkommen!</h1><p>Vielen Dank für Ihre Anmeldung zu unserem Newsletter.</p>"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/admin/newsletter/templates", json=payload, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created newsletter template")
        else:
            print(f"❌ Failed to create newsletter template. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains success message and template
        if "message" in data and "template" in data:
            print(f"✅ Response contains message: {data['message']}")
            
            # Verify template fields
            template = data["template"]
            required_fields = ["id", "name", "subject", "content", "created_at", "created_by", "is_active"]
            missing_fields = [field for field in required_fields if field not in template]
            
            if not missing_fields:
                print("✅ Template object contains all required fields")
            else:
                print(f"❌ Template object is missing required fields: {missing_fields}")
                return False
                
            # Check if fields match what we sent
            if (template["name"] == payload["name"] and 
                template["subject"] == payload["subject"] and
                template["content"] == payload["content"]):
                print("✅ Returned template data matches input")
            else:
                print(f"❌ Returned template data doesn't match input")
                return False
        else:
            print("❌ Response does not contain expected message and template")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create newsletter template endpoint: {e}")
        return False

def test_get_newsletter_campaigns():
    """Test GET /api/admin/newsletter/campaigns endpoint"""
    print("\n🧪 Testing GET /api/admin/newsletter/campaigns endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/newsletter/campaigns", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved newsletter campaigns")
        else:
            print(f"❌ Failed to retrieve newsletter campaigns. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} campaigns")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are campaigns, verify the structure of the first one
        if data:
            required_fields = ["id", "subject", "content", "created_at", "created_by", "status"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Campaign objects contain all required fields")
            else:
                print(f"❌ Campaign objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample campaigns:")
            for i, campaign in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {campaign['subject']} - Status: {campaign['status']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to newsletter campaigns endpoint: {e}")
        return False

def test_create_newsletter_campaign():
    """Test POST /api/admin/newsletter/campaigns endpoint"""
    print("\n🧪 Testing POST /api/admin/newsletter/campaigns endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Create a unique campaign subject with timestamp
        timestamp = int(time.time())
        
        # Create payload
        payload = {
            "subject": f"Test Campaign {timestamp}",
            "content": "<h1>Neue Angebote!</h1><p>Entdecken Sie unsere neuen Tapas-Spezialitäten.</p>",
            "template_id": None  # Optional
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/admin/newsletter/campaigns", json=payload, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created newsletter campaign")
        else:
            print(f"❌ Failed to create newsletter campaign. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains success message and newsletter
        if "message" in data and "newsletter" in data:
            print(f"✅ Response contains message: {data['message']}")
            
            # Verify newsletter fields
            newsletter = data["newsletter"]
            required_fields = ["id", "subject", "content", "created_at", "created_by", "status"]
            missing_fields = [field for field in required_fields if field not in newsletter]
            
            if not missing_fields:
                print("✅ Newsletter object contains all required fields")
            else:
                print(f"❌ Newsletter object is missing required fields: {missing_fields}")
                return False
                
            # Check if fields match what we sent
            if (newsletter["subject"] == payload["subject"] and 
                newsletter["content"] == payload["content"]):
                print("✅ Returned newsletter data matches input")
            else:
                print(f"❌ Returned newsletter data doesn't match input")
                return False
                
            # Check if status is draft by default
            if newsletter["status"] == "draft":
                print("✅ Newsletter is in draft status by default as expected")
            else:
                print(f"❌ Newsletter has unexpected status: {newsletter['status']}")
                return False
        else:
            print("❌ Response does not contain expected message and newsletter")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create newsletter campaign endpoint: {e}")
        return False

# CMS Content Tests
def test_get_homepage_hero():
    """Test GET /api/cms/homepage/hero endpoint"""
    print("\n🧪 Testing GET /api/cms/homepage/hero endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/homepage/hero")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved homepage hero content")
        else:
            print(f"❌ Failed to retrieve homepage hero content. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["title", "subtitle", "description", "location_text", "background_image", 
                          "menu_button_text", "locations_button_text"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
            
        # Check if multilanguage fields are properly structured
        multilang_fields = ["title", "subtitle", "description", "location_text", 
                           "menu_button_text", "locations_button_text"]
        
        for field in multilang_fields:
            if field in data:
                if not isinstance(data[field], dict) or not all(lang in data[field] for lang in ["de", "en", "es"]):
                    print(f"❌ Field '{field}' is not properly structured as multilanguage")
                    return False
        
        print("✅ All multilanguage fields are properly structured")
        
        # Print some sample data
        print(f"📊 Sample hero content:")
        print(f"  Title (DE): {data['title']['de']}")
        print(f"  Subtitle (DE): {data['subtitle']['de']}")
        print(f"  Background Image: {data['background_image']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to homepage hero endpoint: {e}")
        return False

def test_get_homepage_features():
    """Test GET /api/cms/homepage/features endpoint"""
    print("\n🧪 Testing GET /api/cms/homepage/features endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/homepage/features")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved homepage features content")
        else:
            print(f"❌ Failed to retrieve homepage features content. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["section_title", "section_description", "features"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
            
        # Check if features is a list
        if not isinstance(data["features"], list):
            print("❌ Features is not a list")
            return False
            
        # If there are features, verify the structure of the first one
        if data["features"]:
            feature = data["features"][0]
            feature_required_fields = ["title", "description", "image_url", "image_alt"]
            feature_missing_fields = [field for field in feature_required_fields if field not in feature]
            
            if not feature_missing_fields:
                print("✅ Feature objects contain all required fields")
            else:
                print(f"❌ Feature objects are missing required fields: {feature_missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample features content:")
            print(f"  Section Title (DE): {data['section_title']['de']}")
            print(f"  Number of features: {len(data['features'])}")
            for i, feature in enumerate(data["features"][:2]):  # Show up to 2 samples
                print(f"  Feature {i+1}: {feature['title']['de']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to homepage features endpoint: {e}")
        return False

def test_get_homepage_food_gallery():
    """Test GET /api/cms/homepage/food-gallery endpoint"""
    print("\n🧪 Testing GET /api/cms/homepage/food-gallery endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/homepage/food-gallery")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved homepage food gallery content")
        else:
            print(f"❌ Failed to retrieve homepage food gallery content. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["section_title", "gallery_items"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
            
        # Check if gallery_items is a list
        if not isinstance(data["gallery_items"], list):
            print("❌ Gallery items is not a list")
            return False
            
        # If there are gallery items, verify the structure of the first one
        if data["gallery_items"]:
            item = data["gallery_items"][0]
            item_required_fields = ["name", "description", "image_url", "category_link"]
            item_missing_fields = [field for field in item_required_fields if field not in item]
            
            if not item_missing_fields:
                print("✅ Gallery item objects contain all required fields")
            else:
                print(f"❌ Gallery item objects are missing required fields: {item_missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample food gallery content:")
            print(f"  Section Title (DE): {data['section_title']['de']}")
            print(f"  Number of gallery items: {len(data['gallery_items'])}")
            for i, item in enumerate(data["gallery_items"][:2]):  # Show up to 2 samples
                print(f"  Item {i+1}: {item['name']['de']} - {item['category_link']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to homepage food gallery endpoint: {e}")
        return False

def test_get_homepage_lieferando():
    """Test GET /api/cms/homepage/lieferando endpoint"""
    print("\n🧪 Testing GET /api/cms/homepage/lieferando endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/homepage/lieferando")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved homepage lieferando content")
        else:
            print(f"❌ Failed to retrieve homepage lieferando content. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["title", "description", "button_text", "delivery_text", 
                          "authentic_text", "availability_text", "lieferando_url"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
            
        # Check if multilanguage fields are properly structured
        multilang_fields = ["title", "description", "button_text", "delivery_text", 
                           "authentic_text", "availability_text"]
        
        for field in multilang_fields:
            if field in data:
                if not isinstance(data[field], dict) or not all(lang in data[field] for lang in ["de", "en", "es"]):
                    print(f"❌ Field '{field}' is not properly structured as multilanguage")
                    return False
        
        print("✅ All multilanguage fields are properly structured")
        
        # Print some sample data
        print(f"📊 Sample lieferando content:")
        print(f"  Title (DE): {data['title']['de']}")
        print(f"  Description (DE): {data['description']['de'][:50]}...")
        print(f"  Lieferando URL: {data['lieferando_url']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to homepage lieferando endpoint: {e}")
        return False

def run_jimmy_tapas_tests():
    """Run tests for Jimmy's Tapas Bar backend after fixes"""
    print("\n🔍 Starting Jimmy's Tapas Bar Backend Tests After Fixes")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # First, authenticate to get a token for protected endpoints
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    if not auth_success:
        print("❌ Authentication failed. Cannot proceed with tests requiring authentication.")
    
    # Priority 1: Fixed issues
    print("\n📋 Priority 1: Testing Fixed Issues")
    print("-" * 80)
    
    # Test Menu-System GET endpoint (fixed data type issue)
    results["menu_items_get"] = test_get_menu_items()
    
    # Test Newsletter SMTP POST endpoint (fixed import issue)
    if auth_success:
        results["smtp_config_post"] = test_create_smtp_config()
    else:
        results["smtp_config_post"] = False
        print("❌ Skipping SMTP configuration test due to failed login")
    
    # Priority 2: Newsletter System
    print("\n📋 Priority 2: Testing Newsletter System")
    print("-" * 80)
    
    # Test Newsletter Registration
    results["newsletter_subscribe"], subscriber_email = test_newsletter_subscribe()
    
    # Test SMTP Configuration GET
    if auth_success:
        results["smtp_config_get"] = test_get_smtp_config()
    else:
        results["smtp_config_get"] = False
        print("❌ Skipping SMTP configuration GET test due to failed login")
    
    # Test Newsletter Templates
    if auth_success:
        results["newsletter_templates_get"] = test_get_newsletter_templates()
        results["newsletter_templates_post"] = test_create_newsletter_template()
    else:
        results["newsletter_templates_get"] = False
        results["newsletter_templates_post"] = False
        print("❌ Skipping newsletter templates tests due to failed login")
    
    # Test Newsletter Campaigns
    if auth_success:
        results["newsletter_campaigns_get"] = test_get_newsletter_campaigns()
        results["newsletter_campaigns_post"] = test_create_newsletter_campaign()
    else:
        results["newsletter_campaigns_get"] = False
        results["newsletter_campaigns_post"] = False
        print("❌ Skipping newsletter campaigns tests due to failed login")
    
    # Test Subscribers Management
    if auth_success:
        results["newsletter_subscribers_get"] = test_get_newsletter_subscribers()
    else:
        results["newsletter_subscribers_get"] = False
        print("❌ Skipping newsletter subscribers test due to failed login")
    
    # Priority 3: CMS Content
    print("\n📋 Priority 3: Testing CMS Content")
    print("-" * 80)
    
    # Test Homepage Hero
    results["homepage_hero_get"] = test_get_homepage_hero()
    
    # Test Homepage Features
    results["homepage_features_get"] = test_get_homepage_features()
    
    # Test Homepage Food Gallery
    results["homepage_food_gallery_get"] = test_get_homepage_food_gallery()
    
    # Test Homepage Lieferando
    results["homepage_lieferando_get"] = test_get_homepage_lieferando()
    
    # Print summary
    print("\n📋 Test Summary")
    print("=" * 80)
    
    # Priority 1 summary
    print("\nPriority 1: Fixed Issues")
    print("-" * 40)
    priority1_tests = ["menu_items_get", "smtp_config_post"]
    for test_name in priority1_tests:
        status = "✅ PASSED" if results[test_name] else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Priority 2 summary
    print("\nPriority 2: Newsletter System")
    print("-" * 40)
    priority2_tests = ["newsletter_subscribe", "smtp_config_get", "newsletter_templates_get", 
                      "newsletter_templates_post", "newsletter_campaigns_get", 
                      "newsletter_campaigns_post", "newsletter_subscribers_get"]
    for test_name in priority2_tests:
        status = "✅ PASSED" if results[test_name] else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Priority 3 summary
    print("\nPriority 3: CMS Content")
    print("-" * 40)
    priority3_tests = ["homepage_hero_get", "homepage_features_get", 
                      "homepage_food_gallery_get", "homepage_lieferando_get"]
    for test_name in priority3_tests:
        status = "✅ PASSED" if results[test_name] else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Overall result
    all_passed = all(results.values())
    print("\n🏁 Overall Result:", "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED")
    
    return all_passed

if __name__ == "__main__":
    # Check if a specific test is requested
    if len(sys.argv) > 1:
        if sys.argv[1] == "admin-route":
            # Run the admin route tests
            success = run_admin_route_tests()
        elif sys.argv[1] == "jimmy-tapas":
            # Run the Jimmy's Tapas Bar tests after fixes
            success = run_jimmy_tapas_tests()
        else:
            # Run the specific tests for admin login system
            success = run_admin_login_tests()
    else:
        # Run the Jimmy's Tapas Bar tests after fixes by default
        success = run_jimmy_tapas_tests()
    sys.exit(0 if success else 1)
