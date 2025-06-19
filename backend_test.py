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
BACKEND_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://9761dddc-91bf-4ff6-952b-2a25ae7da603.preview.emergentagent.com")
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Using backend URL: {BACKEND_URL}")
print(f"API base URL: {API_BASE_URL}")

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
        if "message" in data and "Hello World" in data["message"]:
            print(f"✅ Response contains expected message: {data['message']}")
        else:
            print(f"❌ Response does not contain expected 'Hello World' message")
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
            
            # Check if response is 401 Unauthorized or 403 Forbidden (both are acceptable)
            if response.status_code in [401, 403]:
                print(f"✅ {endpoint['name']} correctly returned {response.status_code} (Unauthorized/Forbidden)")
                results[endpoint["name"]] = True
            else:
                print(f"❌ {endpoint['name']} returned {response.status_code} instead of 401/403")
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

def test_spanish_dishes():
    """Test GET /api/menu/items endpoint for specific Spanish dishes"""
    print("\n🧪 Testing GET /api/menu/items endpoint for Spanish dishes...")
    
    # List of Spanish dishes to check for
    spanish_dishes = [
        "Paella Valenciana",
        "Paella de Mariscos",
        "Gazpacho Andaluz",
        "Salmorejo Cordobés",
        "Jamón Ibérico de Bellota",
        "Arroz con Pollo",
        "Pulpo a la Gallega",
        "Migas Extremeñas",
        "Fabada Asturiana",
        "Caldereta de Langosta"
    ]
    
    # Required detailed fields for each dish
    required_detail_fields = [
        "detailed_description",
        "ingredients",
        "origin",
        "preparation_method",
        "allergens",
        "price"
    ]
    
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
            
            # Check if the total number of menu items is around 128 (118 original + 10 new dishes)
            if len(data) >= 125:  # Allow for some flexibility
                print(f"✅ Total menu items count ({len(data)}) is close to the expected 128 items")
            else:
                print(f"❌ Total menu items count ({len(data)}) is less than expected (around 128)")
                
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # Create a dictionary to track which Spanish dishes were found
        found_dishes = {dish: False for dish in spanish_dishes}
        dish_details = {}
        
        # Check for each Spanish dish in the menu items
        for item in data:
            if item["name"] in spanish_dishes:
                found_dishes[item["name"]] = True
                dish_details[item["name"]] = item
        
        # Print which dishes were found and which were not
        print("\n📊 Spanish Dishes Check:")
        all_dishes_found = True
        for dish, found in found_dishes.items():
            if found:
                print(f"  ✅ {dish} - Found")
            else:
                print(f"  ❌ {dish} - Not found")
                all_dishes_found = False
        
        if all_dishes_found:
            print("✅ All required Spanish dishes were found in the menu")
        else:
            print("❌ Some required Spanish dishes were not found in the menu")
            return False
        
        # Check detailed information for each found dish
        print("\n📊 Detailed Information Check:")
        all_details_complete = True
        
        for dish_name, dish_data in dish_details.items():
            print(f"\n  Checking details for: {dish_name}")
            
            # Check if all required detail fields are present
            missing_fields = [field for field in required_detail_fields if field not in dish_data or not dish_data[field]]
            
            if not missing_fields:
                print(f"  ✅ All required detail fields are present")
            else:
                print(f"  ❌ Missing required detail fields: {missing_fields}")
                all_details_complete = False
                continue
            
            # Check if detailed_description is in German and comprehensive
            if len(dish_data["detailed_description"]) > 50:  # Assuming a comprehensive description is at least 50 chars
                print(f"  ✅ Detailed description is comprehensive ({len(dish_data['detailed_description'])} chars)")
            else:
                print(f"  ❌ Detailed description is too short ({len(dish_data['detailed_description'])} chars)")
                all_details_complete = False
            
            # Check if ingredients list is complete
            if len(dish_data["ingredients"]) > 20:  # Assuming a complete ingredient list is at least 20 chars
                print(f"  ✅ Ingredients list is complete ({len(dish_data['ingredients'])} chars)")
            else:
                print(f"  ❌ Ingredients list is too short ({len(dish_data['ingredients'])} chars)")
                all_details_complete = False
            
            # Check if origin specifies a Spanish region
            if dish_data["origin"] and len(dish_data["origin"]) > 5:
                print(f"  ✅ Origin is specified: {dish_data['origin']}")
            else:
                print(f"  ❌ Origin is not properly specified: {dish_data['origin']}")
                all_details_complete = False
            
            # Check if preparation_method is detailed
            if len(dish_data["preparation_method"]) > 50:  # Assuming a detailed method is at least 50 chars
                print(f"  ✅ Preparation method is detailed ({len(dish_data['preparation_method'])} chars)")
            else:
                print(f"  ❌ Preparation method is too brief ({len(dish_data['preparation_method'])} chars)")
                all_details_complete = False
            
            # Check if allergens information is detailed
            if dish_data["allergens"] and len(dish_data["allergens"]) > 5:
                print(f"  ✅ Allergens information is provided: {dish_data['allergens']}")
            else:
                print(f"  ❌ Allergens information is missing or too brief: {dish_data['allergens']}")
                all_details_complete = False
            
            # Check if price is properly formatted in euros
            if "€" in dish_data["price"]:
                print(f"  ✅ Price is properly formatted in euros: {dish_data['price']}")
            else:
                print(f"  ❌ Price is not properly formatted in euros: {dish_data['price']}")
                all_details_complete = False
        
        if all_details_complete:
            print("\n✅ All Spanish dishes have comprehensive detailed information")
        else:
            print("\n❌ Some Spanish dishes are missing comprehensive detailed information")
            return False
            
        return all_dishes_found and all_details_complete
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to menu/items endpoint: {e}")
        return False

def test_delivery_info():
    """Test GET /api/delivery/info endpoint"""
    print("\n🧪 Testing GET /api/delivery/info endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/delivery/info")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved delivery information")
        else:
            print(f"❌ Failed to retrieve delivery information. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["delivery_time_min", "delivery_time_max", "minimum_order_value", "delivery_fee"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if delivery time is 30-45 minutes
        if data["delivery_time_min"] == 30 and data["delivery_time_max"] == 45:
            print("✅ Delivery time is correctly set to 30-45 minutes")
        else:
            print(f"❌ Delivery time is not 30-45 minutes. Got: {data['delivery_time_min']}-{data['delivery_time_max']} minutes")
            return False
        
        # Check if minimum order value is 15€
        if data["minimum_order_value"] == 15.0:
            print("✅ Minimum order value is correctly set to 15€")
        else:
            print(f"❌ Minimum order value is not 15€. Got: {data['minimum_order_value']}€")
            return False
        
        # Check if delivery fee is 2.50€
        if data["delivery_fee"] == 2.5:
            print("✅ Delivery fee is correctly set to 2.50€")
        else:
            print(f"❌ Delivery fee is not 2.50€. Got: {data['delivery_fee']}€")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to delivery/info endpoint: {e}")
        return False

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
    
    # Test 11: Delivery Info
    results["delivery_info"] = test_delivery_info()
    
    # Test 12: CMS Endpoints
    results["cms_locations_get"] = test_cms_locations_get()
    results["cms_about_get"] = test_cms_about_get()
    
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

def test_cms_homepage_get():
    """Test GET /api/cms/homepage endpoint"""
    print("\n🧪 Testing GET /api/cms/homepage endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/homepage")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved homepage content")
        else:
            print(f"❌ Failed to retrieve homepage content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "hero", "features", "specialties", "delivery", "updated_at"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if hero section contains expected fields
        hero_fields = ["title", "subtitle", "description", "location", "background_image"]
        missing_hero_fields = [field for field in hero_fields if field not in data["hero"]]
        
        if not missing_hero_fields:
            print("✅ Hero section contains all required fields")
            print(f"✅ Hero title: {data['hero']['title']}")
        else:
            print(f"❌ Hero section is missing required fields: {missing_hero_fields}")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/homepage endpoint: {e}")
        return False

def test_cms_homepage_put():
    """Test PUT /api/cms/homepage endpoint"""
    print("\n🧪 Testing PUT /api/cms/homepage endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # First get the current homepage content
        get_response = requests.get(f"{API_BASE_URL}/cms/homepage")
        if get_response.status_code != 200:
            print(f"❌ Failed to retrieve current homepage content. Status code: {get_response.status_code}")
            return False
        
        current_data = get_response.json()
        
        # Make a copy of the current data to modify
        updated_data = current_data.copy()
        
        # Update the hero title with a timestamp to ensure it's different
        timestamp = int(time.time())
        updated_data["hero"]["title"] = f"JIMMY'S TAPAS BAR - {timestamp}"
        
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Make PUT request
        response = requests.put(f"{API_BASE_URL}/cms/homepage", json=updated_data, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully updated homepage content")
        else:
            print(f"❌ Failed to update homepage content. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if the title was updated correctly
        if data["hero"]["title"] == updated_data["hero"]["title"]:
            print(f"✅ Hero title was updated correctly to: {data['hero']['title']}")
        else:
            print(f"❌ Hero title was not updated correctly. Expected: {updated_data['hero']['title']}, Got: {data['hero']['title']}")
            return False
        
        # Restore the original data
        restore_response = requests.put(f"{API_BASE_URL}/cms/homepage", json=current_data, headers=headers)
        if restore_response.status_code == 200:
            print("✅ Successfully restored original homepage content")
        else:
            print(f"❌ Failed to restore original homepage content. Status code: {restore_response.status_code}")
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/homepage endpoint: {e}")
        return False

def test_cms_website_texts_get(section):
    """Test GET /api/cms/website-texts/{section} endpoint"""
    print(f"\n🧪 Testing GET /api/cms/website-texts/{section} endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/website-texts/{section}")
        
        # Check if response is successful
        if response.status_code == 200:
            print(f"✅ Successfully retrieved {section} texts")
        else:
            print(f"❌ Failed to retrieve {section} texts. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "section", "updated_at"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if section matches the requested section
        if data["section"] == section:
            print(f"✅ Section field matches requested section: {section}")
        else:
            print(f"❌ Section field doesn't match requested section. Expected: {section}, Got: {data['section']}")
            return False
        
        # Check if section-specific data is present
        if section == "navigation" and "navigation" in data:
            print(f"✅ Navigation texts are present: {data['navigation']}")
        elif section == "footer" and "footer" in data:
            print(f"✅ Footer texts are present: {data['footer']}")
        elif section == "buttons" and "buttons" in data:
            print(f"✅ Button texts are present: {data['buttons']}")
        elif section == "general" and "general" in data:
            print(f"✅ General texts are present: {data['general']}")
        else:
            print(f"❌ Section-specific data is missing for {section}")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/website-texts/{section} endpoint: {e}")
        return False

def test_cms_website_texts_put(section):
    """Test PUT /api/cms/website-texts/{section} endpoint"""
    print(f"\n🧪 Testing PUT /api/cms/website-texts/{section} endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # First get the current website texts
        get_response = requests.get(f"{API_BASE_URL}/cms/website-texts/{section}")
        if get_response.status_code != 200:
            print(f"❌ Failed to retrieve current {section} texts. Status code: {get_response.status_code}")
            return False
        
        current_data = get_response.json()
        
        # Make a copy of the current data to modify
        updated_data = current_data.copy()
        
        # Update a field based on the section
        timestamp = int(time.time())
        if section == "navigation" and "navigation" in updated_data:
            updated_data["navigation"]["home"] = f"Startseite-{timestamp}"
        elif section == "footer" and "footer" in updated_data:
            updated_data["footer"]["copyright"] = f"© 2024 Jimmy's Tapas Bar - {timestamp}. Alle Rechte vorbehalten."
        elif section == "buttons" and "buttons" in updated_data:
            updated_data["buttons"]["menu_button"] = f"Zur Speisekarte-{timestamp}"
        elif section == "general" and "general" in updated_data:
            updated_data["general"]["loading"] = f"Lädt...-{timestamp}"
        else:
            print(f"❌ Unable to find appropriate field to update for {section}")
            return False
        
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Make PUT request
        response = requests.put(f"{API_BASE_URL}/cms/website-texts/{section}", json=updated_data, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print(f"✅ Successfully updated {section} texts")
        else:
            print(f"❌ Failed to update {section} texts. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Verify the update was successful
        if section == "navigation" and "navigation" in data and data["navigation"]["home"] == updated_data["navigation"]["home"]:
            print(f"✅ Navigation home text was updated correctly to: {data['navigation']['home']}")
        elif section == "footer" and "footer" in data and data["footer"]["copyright"] == updated_data["footer"]["copyright"]:
            print(f"✅ Footer copyright text was updated correctly")
        elif section == "buttons" and "buttons" in data and data["buttons"]["menu_button"] == updated_data["buttons"]["menu_button"]:
            print(f"✅ Menu button text was updated correctly to: {data['buttons']['menu_button']}")
        elif section == "general" and "general" in data and data["general"]["loading"] == updated_data["general"]["loading"]:
            print(f"✅ Loading text was updated correctly to: {data['general']['loading']}")
        else:
            print(f"❌ Text update verification failed for {section}")
            return False
        
        # Restore the original data
        restore_response = requests.put(f"{API_BASE_URL}/cms/website-texts/{section}", json=current_data, headers=headers)
        if restore_response.status_code == 200:
            print(f"✅ Successfully restored original {section} texts")
        else:
            print(f"❌ Failed to restore original {section} texts. Status code: {restore_response.status_code}")
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/website-texts/{section} endpoint: {e}")
        return False

def test_cms_locations_get():
    """Test GET /api/cms/locations endpoint"""
    print("\n🧪 Testing GET /api/cms/locations endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/locations")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved locations content")
        else:
            print(f"❌ Failed to retrieve locations content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "page_title", "page_description", "locations", "updated_at"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if locations array is present and has items
        if "locations" in data and isinstance(data["locations"], list):
            print(f"✅ Locations array contains {len(data['locations'])} locations")
            
            # If there are locations, check the structure of the first one
            if data["locations"]:
                location_fields = ["name", "address", "phone", "email", "opening_hours"]
                missing_location_fields = [field for field in location_fields if field not in data["locations"][0]]
                
                if not missing_location_fields:
                    print("✅ Location objects contain all required fields")
                    print(f"✅ First location: {data['locations'][0]['name']}")
                else:
                    print(f"❌ Location objects are missing required fields: {missing_location_fields}")
                    return False
        else:
            print("❌ Locations array is missing or not an array")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/locations endpoint: {e}")
        return False

def test_cms_locations_put():
    """Test PUT /api/cms/locations endpoint"""
    print("\n🧪 Testing PUT /api/cms/locations endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # First get the current locations content
        get_response = requests.get(f"{API_BASE_URL}/cms/locations")
        if get_response.status_code != 200:
            print(f"❌ Failed to retrieve current locations content. Status code: {get_response.status_code}")
            return False
        
        current_data = get_response.json()
        
        # Make a copy of the current data to modify
        updated_data = current_data.copy()
        
        # Update the page title with a timestamp to ensure it's different
        timestamp = int(time.time())
        updated_data["page_title"] = f"Unsere Standorte - {timestamp}"
        
        # If there are locations, update the first one's name
        if updated_data["locations"]:
            updated_data["locations"][0]["name"] = f"Jimmy's Tapas Bar Kühlungsborn - {timestamp}"
        
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Make PUT request
        response = requests.put(f"{API_BASE_URL}/cms/locations", json=updated_data, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully updated locations content")
        else:
            print(f"❌ Failed to update locations content. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if the title was updated correctly
        if data["page_title"] == updated_data["page_title"]:
            print(f"✅ Page title was updated correctly to: {data['page_title']}")
        else:
            print(f"❌ Page title was not updated correctly. Expected: {updated_data['page_title']}, Got: {data['page_title']}")
            return False
        
        # Check if the first location name was updated correctly
        if data["locations"] and data["locations"][0]["name"] == updated_data["locations"][0]["name"]:
            print(f"✅ First location name was updated correctly to: {data['locations'][0]['name']}")
        else:
            print("❌ First location name was not updated correctly")
            return False
        
        # Restore the original data
        restore_response = requests.put(f"{API_BASE_URL}/cms/locations", json=current_data, headers=headers)
        if restore_response.status_code == 200:
            print("✅ Successfully restored original locations content")
        else:
            print(f"❌ Failed to restore original locations content. Status code: {restore_response.status_code}")
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/locations endpoint: {e}")
        return False

def test_cms_about_get():
    """Test GET /api/cms/about endpoint"""
    print("\n🧪 Testing GET /api/cms/about endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/about")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved about content")
        else:
            print(f"❌ Failed to retrieve about content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "page_title", "hero_title", "story_title", "story_content", "team_title", "team_members", "values_title", "values", "updated_at"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if team_members array is present
        if "team_members" in data and isinstance(data["team_members"], list):
            print(f"✅ Team members array contains {len(data['team_members'])} members")
            
            # If there are team members, check the structure of the first one
            if data["team_members"]:
                member_fields = ["name", "position", "description"]
                missing_member_fields = [field for field in member_fields if field not in data["team_members"][0]]
                
                if not missing_member_fields:
                    print("✅ Team member objects contain all required fields")
                    print(f"✅ First team member: {data['team_members'][0]['name']}")
                else:
                    print(f"❌ Team member objects are missing required fields: {missing_member_fields}")
                    return False
        else:
            print("❌ Team members array is missing or not an array")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/about endpoint: {e}")
        return False

def test_cms_about_put():
    """Test PUT /api/cms/about endpoint"""
    print("\n🧪 Testing PUT /api/cms/about endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # First get the current about content
        get_response = requests.get(f"{API_BASE_URL}/cms/about")
        if get_response.status_code != 200:
            print(f"❌ Failed to retrieve current about content. Status code: {get_response.status_code}")
            return False
        
        current_data = get_response.json()
        
        # Make a copy of the current data to modify
        updated_data = current_data.copy()
        
        # Update the hero title with a timestamp to ensure it's different
        timestamp = int(time.time())
        updated_data["hero_title"] = f"Unsere Geschichte - {timestamp}"
        
        # If there are team members, update the first one's name
        if updated_data["team_members"]:
            updated_data["team_members"][0]["name"] = f"Jimmy Rodriguez - {timestamp}"
        
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Make PUT request
        response = requests.put(f"{API_BASE_URL}/cms/about", json=updated_data, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully updated about content")
        else:
            print(f"❌ Failed to update about content. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if the hero title was updated correctly
        if data["hero_title"] == updated_data["hero_title"]:
            print(f"✅ Hero title was updated correctly to: {data['hero_title']}")
        else:
            print(f"❌ Hero title was not updated correctly. Expected: {updated_data['hero_title']}, Got: {data['hero_title']}")
            return False
        
        # Check if the first team member name was updated correctly
        if data["team_members"] and data["team_members"][0]["name"] == updated_data["team_members"][0]["name"]:
            print(f"✅ First team member name was updated correctly to: {data['team_members'][0]['name']}")
        else:
            print("❌ First team member name was not updated correctly")
            return False
        
        # Restore the original data
        restore_response = requests.put(f"{API_BASE_URL}/cms/about", json=current_data, headers=headers)
        if restore_response.status_code == 200:
            print("✅ Successfully restored original about content")
        else:
            print(f"❌ Failed to restore original about content. Status code: {restore_response.status_code}")
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/about endpoint: {e}")
        return False

def run_cms_tests():
    """Run tests for the CMS endpoints"""
    print("\n🔍 Starting Jimmy's Tapas Bar CMS API Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test authentication first
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    # Test Homepage endpoints
    results["cms_homepage_get"] = test_cms_homepage_get()
    
    if auth_success:
        results["cms_homepage_put"] = test_cms_homepage_put()
    else:
        results["cms_homepage_put"] = False
        print("❌ Skipping homepage update test due to failed login")
    
    # Test Website Texts endpoints
    for section in ["navigation", "footer", "buttons", "general"]:
        results[f"cms_website_texts_get_{section}"] = test_cms_website_texts_get(section)
        
        if auth_success:
            results[f"cms_website_texts_put_{section}"] = test_cms_website_texts_put(section)
        else:
            results[f"cms_website_texts_put_{section}"] = False
            print(f"❌ Skipping {section} texts update test due to failed login")
    
    # Test Locations endpoints
    results["cms_locations_get"] = test_cms_locations_get()
    
    if auth_success:
        results["cms_locations_put"] = test_cms_locations_put()
    else:
        results["cms_locations_put"] = False
        print("❌ Skipping locations update test due to failed login")
    
    # Test About endpoints
    results["cms_about_get"] = test_cms_about_get()
    
    if auth_success:
        results["cms_about_put"] = test_cms_about_put()
    else:
        results["cms_about_put"] = False
        print("❌ Skipping about update test due to failed login")
    
    # Test unauthorized access
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

def test_cms_legal_get(page_type):
    """Test GET /api/cms/legal/{page_type} endpoint"""
    print(f"\n🧪 Testing GET /api/cms/legal/{page_type} endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/legal/{page_type}")
        
        # Check if response is successful
        if response.status_code == 200:
            print(f"✅ Successfully retrieved {page_type} page content")
        else:
            print(f"❌ Failed to retrieve {page_type} page content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "page_type", "title", "content"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if page_type matches the requested page_type
        if data["page_type"] == page_type:
            print(f"✅ Page type matches requested type: {page_type}")
        else:
            print(f"❌ Page type doesn't match requested type. Expected: {page_type}, Got: {data['page_type']}")
            return False
        
        # Print some content info
        print(f"✅ Page title: {data['title']}")
        print(f"✅ Content length: {len(data['content'])} characters")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/legal/{page_type} endpoint: {e}")
        return False

def test_cms_legal_put(page_type):
    """Test PUT /api/cms/legal/{page_type} endpoint"""
    print(f"\n🧪 Testing PUT /api/cms/legal/{page_type} endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # First get the current legal page content
        get_response = requests.get(f"{API_BASE_URL}/cms/legal/{page_type}")
        if get_response.status_code != 200:
            print(f"❌ Failed to retrieve current {page_type} page content. Status code: {get_response.status_code}")
            return False
        
        current_data = get_response.json()
        
        # Make a copy of the current data to modify
        updated_data = current_data.copy()
        
        # Update the title with a timestamp to ensure it's different
        timestamp = int(time.time())
        updated_data["title"] = f"{current_data['title']} - {timestamp}"
        
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Make PUT request
        response = requests.put(f"{API_BASE_URL}/cms/legal/{page_type}", json=updated_data, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print(f"✅ Successfully updated {page_type} page content")
        else:
            print(f"❌ Failed to update {page_type} page content. Status code: {response.status_code}")
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
        
        # Verify the update by getting the page again
        verify_response = requests.get(f"{API_BASE_URL}/cms/legal/{page_type}")
        if verify_response.status_code != 200:
            print(f"❌ Failed to verify {page_type} page update. Status code: {verify_response.status_code}")
            return False
        
        verify_data = verify_response.json()
        if verify_data["title"] == updated_data["title"]:
            print(f"✅ Title was updated correctly to: {verify_data['title']}")
        else:
            print(f"❌ Title was not updated correctly. Expected: {updated_data['title']}, Got: {verify_data['title']}")
            return False
        
        # Restore the original data
        restore_response = requests.put(f"{API_BASE_URL}/cms/legal/{page_type}", json=current_data, headers=headers)
        if restore_response.status_code == 200:
            print(f"✅ Successfully restored original {page_type} page content")
        else:
            print(f"❌ Failed to restore original {page_type} page content. Status code: {restore_response.status_code}")
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/legal/{page_type} endpoint: {e}")
        return False

def test_admin_system_info():
    """Test GET /api/admin/system/info endpoint"""
    print("\n🧪 Testing GET /api/admin/system/info endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/system/info", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved system information")
        else:
            print(f"❌ Failed to retrieve system information. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected sections
        required_sections = ["system", "mysql", "application"]
        missing_sections = [section for section in required_sections if section not in data]
        
        if not missing_sections:
            print("✅ Response contains all required sections")
        else:
            print(f"❌ Response is missing required sections: {missing_sections}")
            return False
        
        # Check MySQL section
        if "mysql" in data:
            mysql_info = data["mysql"]
            print(f"✅ MySQL version: {mysql_info.get('version', 'N/A')}")
            print(f"✅ MySQL connection status: {mysql_info.get('connection_status', 'N/A')}")
            
            # Check if database info is present
            if "database_info" in mysql_info:
                db_info = mysql_info["database_info"]
                print(f"✅ Database name: {db_info.get('name', 'N/A')}")
                print(f"✅ Number of tables: {db_info.get('tables_count', 'N/A')}")
            else:
                print("❌ MySQL database_info section is missing")
                return False
        else:
            print("❌ MySQL section is missing")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin/system/info endpoint: {e}")
        return False

def test_backup_list():
    """Test GET /api/admin/backup/list endpoint"""
    print("\n🧪 Testing GET /api/admin/backup/list endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/backup/list", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved backup list")
        else:
            print(f"❌ Failed to retrieve backup list. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} backups")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are backups, verify the structure of the first one
        if data:
            required_fields = ["id", "filename", "type", "created_at", "created_by", "size_human"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Backup objects contain all required fields")
            else:
                print(f"❌ Backup objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample backups:")
            for i, backup in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {backup['filename']} - Type: {backup['type']}, Size: {backup['size_human']}, Created: {backup['created_at']}")
                
            # Check if created_at is properly formatted as ISO date string
            try:
                datetime.fromisoformat(data[0]['created_at'].replace('Z', '+00:00'))
                print("✅ created_at is properly formatted as ISO date string")
            except (ValueError, TypeError):
                print("❌ created_at is not properly formatted as ISO date string")
                return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin/backup/list endpoint: {e}")
        return False

def test_create_database_backup():
    """Test POST /api/admin/backup/database endpoint"""
    print("\n🧪 Testing POST /api/admin/backup/database endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/admin/backup/database", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created database backup")
        else:
            print(f"❌ Failed to create database backup. Status code: {response.status_code}")
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
        required_fields = ["id", "filename", "type", "created_at", "created_by", "size_human"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False, None
        
        # Check if backup type is correct
        if data["type"] == "database":
            print("✅ Backup type is correctly set to 'database'")
        else:
            print(f"❌ Backup type is not 'database', got: {data['type']}")
            return False, None
            
        # Check if created_at is properly formatted as ISO date string
        try:
            datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            print("✅ created_at is properly formatted as ISO date string")
        except (ValueError, TypeError):
            print("❌ created_at is not properly formatted as ISO date string")
            return False, None
            
        return True, data["id"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin/backup/database endpoint: {e}")
        return False, None

def test_create_full_backup():
    """Test POST /api/admin/backup/full endpoint"""
    print("\n🧪 Testing POST /api/admin/backup/full endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/admin/backup/full", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created full backup")
        else:
            print(f"❌ Failed to create full backup. Status code: {response.status_code}")
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
        required_fields = ["id", "filename", "type", "created_at", "created_by", "size_human"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False, None
        
        # Check if backup type is correct
        if data["type"] == "full":
            print("✅ Backup type is correctly set to 'full'")
        else:
            print(f"❌ Backup type is not 'full', got: {data['type']}")
            return False, None
            
        # Check if created_at is properly formatted as ISO date string
        try:
            datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            print("✅ created_at is properly formatted as ISO date string")
        except (ValueError, TypeError):
            print("❌ created_at is not properly formatted as ISO date string")
            return False, None
            
        return True, data["id"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin/backup/full endpoint: {e}")
        return False, None

def test_backup_download(backup_id):
    """Test GET /api/admin/backup/download/{backup_id} endpoint"""
    print(f"\n🧪 Testing GET /api/admin/backup/download/{backup_id} endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/backup/download/{backup_id}", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved backup download information")
        else:
            print(f"❌ Failed to retrieve backup download information. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            elif response.status_code == 404:
                print("   Backup not found")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "filename", "download_url", "type", "created_at"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if backup ID matches
        if data["id"] == backup_id:
            print("✅ Backup ID matches requested ID")
        else:
            print(f"❌ Backup ID doesn't match requested ID. Expected: {backup_id}, Got: {data['id']}")
            return False
            
        # Check if download_url is present
        if data["download_url"]:
            print(f"✅ Download URL is present: {data['download_url']}")
        else:
            print("❌ Download URL is missing or empty")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin/backup/download/{backup_id} endpoint: {e}")
        return False

def test_delete_backup(backup_id):
    """Test DELETE /api/admin/backup/{backup_id} endpoint"""
    print(f"\n🧪 Testing DELETE /api/admin/backup/{backup_id} endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make DELETE request
        response = requests.delete(f"{API_BASE_URL}/admin/backup/{backup_id}", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully deleted backup")
        else:
            print(f"❌ Failed to delete backup. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            elif response.status_code == 404:
                print("   Backup not found")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains success message
        if "message" in data and "deleted" in data["message"].lower():
            print(f"✅ Response contains success message: {data['message']}")
        else:
            print("❌ Response does not contain expected success message")
            return False
            
        # Verify deletion by trying to download the backup
        verify_response = requests.get(f"{API_BASE_URL}/admin/backup/download/{backup_id}", headers=headers)
        if verify_response.status_code == 404:
            print("✅ Backup was successfully deleted (404 Not Found when trying to download)")
        else:
            print(f"❌ Backup may not have been deleted. Got status code {verify_response.status_code} when trying to download")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin/backup/{backup_id} endpoint: {e}")
        return False

def test_reviews_with_datetime():
    """Test POST /api/reviews endpoint with datetime handling"""
    print("\n🧪 Testing POST /api/reviews endpoint with datetime handling...")
    
    try:
        # Create payload
        payload = {
            "customer_name": "Elena Rodríguez",
            "rating": 5,
            "comment": "¡Excelente experiencia! La comida estaba deliciosa y el servicio fue impecable. Volveré pronto."
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
        
        # Check if date field is properly formatted as ISO date string
        try:
            datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
            print("✅ Date field is properly formatted as ISO date string")
        except (ValueError, TypeError):
            print("❌ Date field is not properly formatted as ISO date string")
            return False, None
            
        # Check if fields match what we sent
        if (data["customer_name"] == payload["customer_name"] and 
            data["rating"] == payload["rating"] and
            data["comment"] == payload["comment"]):
            print("✅ Returned review data matches input")
        else:
            print(f"❌ Returned review data doesn't match input")
            return False, None
            
        return True, data["id"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to reviews endpoint: {e}")
        return False, None

def test_get_reviews_with_datetime():
    """Test GET /api/reviews endpoint with datetime handling"""
    print("\n🧪 Testing GET /api/reviews endpoint with datetime handling...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/reviews?approved_only=false")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved reviews")
        else:
            print(f"❌ Failed to retrieve reviews. Status code: {response.status_code}")
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
                
            # Check if date field is properly formatted as ISO date string
            try:
                datetime.fromisoformat(data[0]['date'].replace('Z', '+00:00'))
                print("✅ Date field is properly formatted as ISO date string")
            except (ValueError, TypeError):
                print("❌ Date field is not properly formatted as ISO date string")
                return False
                
            # Print some sample data
            print(f"📊 Sample reviews:")
            for i, review in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {review['customer_name']} - {review['rating']}★ - {review['date']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to reviews endpoint: {e}")
        return False

def run_mysql_migration_tests():
    """Run tests for MySQL migration and enhanced backup system"""
    print("\n🔍 Starting Jimmy's Tapas Bar MySQL Migration and Backup System Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test authentication first
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    if auth_success:
        results["auth_me"] = test_auth_me()
    else:
        results["auth_me"] = False
        print("❌ Skipping auth/me test due to failed login")
    
    # Test CMS endpoints
    results["cms_homepage_get"] = test_cms_homepage_get()
    results["cms_locations_get"] = test_cms_locations_get()
    results["cms_about_get"] = test_cms_about_get()
    
    # Test legal pages
    for page_type in ["imprint", "privacy"]:
        results[f"cms_legal_get_{page_type}"] = test_cms_legal_get(page_type)
    
    # Test menu items
    results["menu_items_get"] = test_get_menu_items()
    
    # Test reviews with datetime handling
    review_success, review_id = test_reviews_with_datetime()
    results["reviews_create_with_datetime"] = review_success
    results["reviews_get_with_datetime"] = test_get_reviews_with_datetime()
    
    if auth_success:
        results["pending_reviews_get"] = test_get_pending_reviews()
    else:
        results["pending_reviews_get"] = False
        print("❌ Skipping pending reviews test due to failed login")
    
    # Test enhanced backup system
    if auth_success:
        results["backup_list"] = test_backup_list()
        
        # Create database backup
        db_backup_success, db_backup_id = test_create_database_backup()
        results["create_database_backup"] = db_backup_success
        
        # Test backup download if database backup was created
        if db_backup_success and db_backup_id:
            results["backup_download"] = test_backup_download(db_backup_id)
        else:
            results["backup_download"] = False
            print("❌ Skipping backup download test due to failed database backup creation")
        
        # Create full backup
        full_backup_success, full_backup_id = test_create_full_backup()
        results["create_full_backup"] = full_backup_success
        
        # Test backup deletion if any backup was created
        if db_backup_success and db_backup_id:
            results["delete_backup"] = test_delete_backup(db_backup_id)
        elif full_backup_success and full_backup_id:
            results["delete_backup"] = test_delete_backup(full_backup_id)
        else:
            results["delete_backup"] = False
            print("❌ Skipping backup deletion test due to failed backup creation")
        
        # Test system info
        results["system_info"] = test_admin_system_info()
    else:
        results["backup_list"] = False
        results["create_database_backup"] = False
        results["create_full_backup"] = False
        results["backup_download"] = False
        results["delete_backup"] = False
        results["system_info"] = False
        print("❌ Skipping backup system tests due to failed login")
    
    # Test user management
    if auth_success:
        results["users_get"] = test_get_users()
    else:
        results["users_get"] = False
        print("❌ Skipping user management test due to failed login")
    
    # Test contact system
    contact_success, contact_id = test_create_contact_message()
    results["contact_create"] = contact_success
    
    if auth_success:
        results["contact_messages_get"] = test_get_contact_messages()
    else:
        results["contact_messages_get"] = False
        print("❌ Skipping contact messages test due to failed login")
    
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

def run_mysql_migration_validation():
    """Run comprehensive validation tests for MySQL migration"""
    print("\n🔍 Starting Jimmy's Tapas Bar MySQL Migration Validation Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: MySQL Backend Authentication
    auth_success, token = test_auth_login()
    results["mysql_auth_login"] = auth_success
    
    if auth_success:
        results["mysql_auth_me"] = test_auth_me()
    else:
        results["mysql_auth_me"] = False
        print("❌ Skipping auth/me test due to failed login")
    
    # Test 2: MySQL CMS Data Structure
    results["mysql_cms_homepage"] = test_cms_homepage_get()
    results["mysql_cms_locations"] = test_cms_locations_get()
    results["mysql_cms_about"] = test_cms_about_get()
    
    # Test 3: MySQL Menu Items
    results["mysql_menu_items"] = test_get_menu_items()
    
    # Test 4: MySQL Review System with Datetime Serialization
    review_success, review_id = test_reviews_with_datetime()
    results["mysql_review_create"] = review_success
    results["mysql_reviews_get"] = test_get_reviews_with_datetime()
    
    if auth_success:
        results["mysql_pending_reviews"] = test_get_pending_reviews()
    else:
        results["mysql_pending_reviews"] = False
        print("❌ Skipping pending reviews test due to failed login")
    
    # Test 5: MySQL Enhanced Backup System
    if auth_success:
        results["mysql_backup_list"] = test_backup_list()
        
        # Create database backup
        db_backup_success, db_backup_id = test_create_database_backup()
        results["mysql_database_backup"] = db_backup_success
        
        # Create full backup
        full_backup_success, full_backup_id = test_create_full_backup()
        results["mysql_full_backup"] = full_backup_success
        
        # Test backup download if database backup was created
        if db_backup_success and db_backup_id:
            results["mysql_backup_download"] = test_backup_download(db_backup_id)
        else:
            results["mysql_backup_download"] = False
            print("❌ Skipping backup download test due to failed database backup creation")
        
        # Test backup deletion if any backup was created
        if db_backup_success and db_backup_id:
            results["mysql_backup_delete"] = test_delete_backup(db_backup_id)
        elif full_backup_success and full_backup_id:
            results["mysql_backup_delete"] = test_delete_backup(full_backup_id)
        else:
            results["mysql_backup_delete"] = False
            print("❌ Skipping backup deletion test due to failed backup creation")
    else:
        results["mysql_backup_list"] = False
        results["mysql_database_backup"] = False
        results["mysql_full_backup"] = False
        results["mysql_backup_download"] = False
        results["mysql_backup_delete"] = False
        print("❌ Skipping backup system tests due to failed login")
    
    # Test 6: MySQL User Management
    if auth_success:
        results["mysql_users"] = test_get_users()
    else:
        results["mysql_users"] = False
        print("❌ Skipping user management test due to failed login")
    
    # Test 7: MySQL Contact Management
    contact_success, contact_id = test_create_contact_message()
    results["mysql_contact_create"] = contact_success
    
    if auth_success:
        results["mysql_contact_messages"] = test_get_contact_messages()
    else:
        results["mysql_contact_messages"] = False
        print("❌ Skipping contact messages test due to failed login")
    
    # Test 8: MySQL System Info
    if auth_success:
        results["mysql_system_info"] = test_admin_system_info()
    else:
        results["mysql_system_info"] = False
        print("❌ Skipping system info test due to failed login")
    
    # Print summary
    print("\n📋 MySQL Migration Validation Summary")
    print("=" * 80)
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Overall result
    all_passed = all(results.values())
    print("\n🏁 Overall MySQL Migration Result:", "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED")
    
    return all_passed

def test_cms_standorte_enhanced():
    """Test GET /api/cms/standorte-enhanced endpoint"""
    print("\n🧪 Testing GET /api/cms/standorte-enhanced endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/standorte-enhanced")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved enhanced locations content")
        else:
            print(f"❌ Failed to retrieve enhanced locations content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "page_title", "page_subtitle", "header_background", "neustadt", "grossenbrode", "info_section"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if location data is present
        if "neustadt" in data and isinstance(data["neustadt"], dict):
            print(f"✅ Neustadt location data is present")
            
            # Check neustadt location fields
            neustadt_fields = ["name", "badge", "address_line1", "address_line2", "opening_hours"]
            missing_neustadt_fields = [field for field in neustadt_fields if field not in data["neustadt"]]
            
            if not missing_neustadt_fields:
                print("✅ Neustadt location contains all required fields")
                print(f"✅ Neustadt location name: {data['neustadt']['name']}")
            else:
                print(f"❌ Neustadt location is missing required fields: {missing_neustadt_fields}")
                return False
        else:
            print("❌ Neustadt location data is missing or not a dictionary")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/standorte-enhanced endpoint: {e}")
        return False

def test_cms_bewertungen_page():
    """Test GET /api/cms/bewertungen-page endpoint"""
    print("\n🧪 Testing GET /api/cms/bewertungen-page endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/bewertungen-page")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved reviews page content")
        else:
            print(f"❌ Failed to retrieve reviews page content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "page_title", "page_subtitle", "header_background", "reviews_section_title", "feedback_section_title", "feedback_note"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Print some sample data
        print(f"✅ Page title: {data['page_title']}")
        print(f"✅ Reviews section title: {data['reviews_section_title']}")
        print(f"✅ Feedback section title: {data['feedback_section_title']}")
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/bewertungen-page endpoint: {e}")
        return False

def test_cms_ueber_uns_enhanced():
    """Test GET /api/cms/ueber-uns-enhanced endpoint"""
    print("\n🧪 Testing GET /api/cms/ueber-uns-enhanced endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/ueber-uns-enhanced")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved enhanced about page content")
        else:
            print(f"❌ Failed to retrieve enhanced about page content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "page_title", "page_subtitle", "header_background", "jimmy", "values_section", "team_section"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if jimmy data is present
        if "jimmy" in data and isinstance(data["jimmy"], dict):
            print(f"✅ Jimmy data is present")
            
            # Check jimmy fields
            jimmy_fields = ["name", "image", "story_paragraph1", "story_paragraph2", "quote"]
            missing_jimmy_fields = [field for field in jimmy_fields if field not in data["jimmy"]]
            
            if not missing_jimmy_fields:
                print("✅ Jimmy data contains all required fields")
                print(f"✅ Jimmy name: {data['jimmy']['name']}")
            else:
                print(f"❌ Jimmy data is missing required fields: {missing_jimmy_fields}")
                return False
        else:
            print("❌ Jimmy data is missing or not a dictionary")
            return False
            
        # Check if values section is present
        if "values_section" in data and isinstance(data["values_section"], dict):
            print(f"✅ Values section is present")
            
            # Check values section fields
            if "title" in data["values_section"]:
                print(f"✅ Values section title: {data['values_section']['title']}")
            else:
                print("❌ Values section is missing title field")
                return False
        else:
            print("❌ Values section is missing or not a dictionary")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/ueber-uns-enhanced endpoint: {e}")
        return False

def test_get_reviews_with_approved_param():
    """Test GET /api/reviews with approved_only parameter"""
    print("\n🧪 Testing GET /api/reviews?approved_only=true endpoint...")
    
    try:
        # Make GET request with approved_only=true
        response = requests.get(f"{API_BASE_URL}/reviews?approved_only=true")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved approved reviews")
        else:
            print(f"❌ Failed to retrieve approved reviews. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} approved reviews")
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
            print(f"📊 Sample approved reviews:")
            for i, review in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {review['customer_name']} - {review['rating']}★ - {review['comment'][:30]}...")
                
            # Verify all reviews are approved
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

def run_requested_tests():
    """Run the specific tests requested in the review request"""
    print("\n🔍 Starting Jimmy's Tapas Bar Backend API Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: Authentication & Users
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    if auth_success:
        results["auth_me"] = test_auth_me()
        results["users_get"] = test_get_users()
    else:
        results["auth_me"] = False
        results["users_get"] = False
        print("❌ Skipping auth/me and users tests due to failed login")
    
    # Test 2: CMS Enhanced Endpoints
    results["cms_standorte_enhanced"] = test_cms_standorte_enhanced()
    results["cms_bewertungen_page"] = test_cms_bewertungen_page()
    results["cms_ueber_uns_enhanced"] = test_cms_ueber_uns_enhanced()
    
    # Test 3: Menu & Reviews
    results["menu_items"] = test_get_menu_items()
    results["reviews_approved"] = test_get_reviews_with_approved_param()
    
    review_success, review_id = test_create_review()
    results["review_create"] = review_success
    
    # Test 4: System Status
    results["root_endpoint"] = test_root_endpoint()
    
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
    # Run the requested tests
    success = run_requested_tests()
    sys.exit(0 if success else 1)
