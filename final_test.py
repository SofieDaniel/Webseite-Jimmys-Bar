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

# Global variables to store tokens and IDs
AUTH_TOKEN = None
MENU_ITEM_ID = None

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
        
        # Check if we have 55 items as expected
        if len(data) != 55:
            print(f"❌ Expected 55 menu items, but got {len(data)}")
        else:
            print(f"✅ Retrieved exactly 55 menu items as expected")
        
        # If there are menu items, verify the structure of the first one
        if data:
            required_fields = ["id", "name", "description", "price", "category"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Menu item objects contain all required fields")
            else:
                print(f"❌ Menu item objects are missing required fields: {missing_fields}")
                return False
            
            # Check that image field is empty
            for item in data:
                if item.get("image") and item["image"] != "":
                    print(f"❌ Menu item '{item['name']}' has a non-empty image field: {item['image']}")
                    return False
            
            print("✅ All menu items have empty image fields as expected")
                
            # Print some sample data
            print(f"📊 Sample menu items:")
            for i, item in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {item['name']} - {item['price']} ({item['category']})")
            
            # Store the first item ID for later tests
            global MENU_ITEM_ID
            MENU_ITEM_ID = data[0]["id"]
                
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
        timestamp = int(time.time())
        payload = {
            "name": f"Test Tapas {timestamp}",
            "description": "Eine köstliche Testspezialität",
            "price": "8,90 €",
            "category": "Tapas Vegetarian",
            "image": "",  # Empty image as required
            "vegetarian": True,
            "vegan": False,
            "glutenfree": True,
            "order_index": 100
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

def test_update_menu_item(item_id):
    """Test PUT /api/menu/items/{item_id} endpoint"""
    print(f"\n🧪 Testing PUT /api/menu/items/{item_id} endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    if not item_id:
        print("❌ No menu item ID available. Create menu item test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Create payload with updated fields
        timestamp = int(time.time())
        payload = {
            "name": f"Updated Tapas {timestamp}",
            "price": "9,90 €",
            "description": "Eine aktualisierte köstliche Testspezialität"
        }
        
        # Make PUT request
        response = requests.put(f"{API_BASE_URL}/menu/items/{item_id}", json=payload, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully updated menu item")
        else:
            print(f"❌ Failed to update menu item. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            elif response.status_code == 404:
                print("   Menu item not found")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if fields match what we sent
        if (data["name"] == payload["name"] and 
            data["description"] == payload["description"] and
            data["price"] == payload["price"]):
            print("✅ Returned menu item data matches updated values")
        else:
            print(f"❌ Returned menu item data doesn't match updated values")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to update menu item endpoint: {e}")
        return False

def test_delete_menu_item(item_id):
    """Test DELETE /api/menu/items/{item_id} endpoint"""
    print(f"\n🧪 Testing DELETE /api/menu/items/{item_id} endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    if not item_id:
        print("❌ No menu item ID available. Create menu item test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make DELETE request
        response = requests.delete(f"{API_BASE_URL}/menu/items/{item_id}", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully deleted menu item")
        else:
            print(f"❌ Failed to delete menu item. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            elif response.status_code == 404:
                print("   Menu item not found")
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
            print("✅ Response contains success message")
        else:
            print("❌ Response does not contain expected success message")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to delete menu item endpoint: {e}")
        return False

def test_get_cms_homepage_hero():
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
        
        # Print some sample data
        print(f"📊 Sample hero content:")
        print(f"  Title: {data['title']}")
        print(f"  Subtitle: {data['subtitle']}")
        print(f"  Background Image: {data['background_image']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to homepage hero endpoint: {e}")
        return False

def test_get_cms_homepage_features():
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
            print(f"  Section Title: {data['section_title']}")
            print(f"  Number of features: {len(data['features'])}")
            for i, feature in enumerate(data["features"][:2]):  # Show up to 2 samples
                print(f"  Feature {i+1}: {feature['title']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to homepage features endpoint: {e}")
        return False

def test_get_cms_homepage_food_gallery():
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
            print(f"  Section Title: {data['section_title']}")
            print(f"  Number of gallery items: {len(data['gallery_items'])}")
            for i, item in enumerate(data["gallery_items"][:2]):  # Show up to 2 samples
                print(f"  Item {i+1}: {item['name']} - {item['category_link']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to homepage food gallery endpoint: {e}")
        return False

def test_get_cms_homepage_lieferando():
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
        
        # Print some sample data
        print(f"📊 Sample lieferando content:")
        print(f"  Title: {data['title']}")
        print(f"  Lieferando URL: {data['lieferando_url']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to homepage lieferando endpoint: {e}")
        return False

def test_get_cms_about():
    """Test GET /api/cms/about endpoint"""
    print("\n🧪 Testing GET /api/cms/about endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/about")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved about page content")
        else:
            print(f"❌ Failed to retrieve about page content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["hero_title", "hero_description", "hero_image", "story_title", "story_content"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Print some sample data
        print(f"📊 Sample about content:")
        print(f"  Hero Title: {data['hero_title']}")
        print(f"  Story Title: {data['story_title']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to about endpoint: {e}")
        return False

def test_get_cms_locations():
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
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are locations, verify the structure of the first one
        if data:
            location = data[0]
            required_fields = ["name", "address", "phone", "email", "opening_hours", "description"]
            missing_fields = [field for field in required_fields if field not in location]
            
            if not missing_fields:
                print("✅ Location objects contain all required fields")
            else:
                print(f"❌ Location objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample locations content:")
            print(f"  Number of locations: {len(data)}")
            for i, location in enumerate(data):
                print(f"  Location {i+1}: {location['name']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to locations endpoint: {e}")
        return False

def test_get_cms_contact():
    """Test GET /api/cms/contact endpoint"""
    print("\n🧪 Testing GET /api/cms/contact endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/contact")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved contact content")
        else:
            print(f"❌ Failed to retrieve contact content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["page_title", "page_description", "contact_form_title", "contact_form_description", 
                          "general_email", "general_phone"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Print some sample data
        print(f"📊 Sample contact content:")
        print(f"  Page Title: {data['page_title']}")
        print(f"  General Email: {data['general_email']}")
        print(f"  General Phone: {data['general_phone']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to contact endpoint: {e}")
        return False

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

def run_final_tests():
    """Run all tests for Jimmy's Tapas Bar backend"""
    print("\n🔍 Starting Jimmy's Tapas Bar Final Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # First, authenticate to get a token for protected endpoints
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    if auth_success:
        results["auth_me"] = test_auth_me()
    else:
        results["auth_me"] = False
        print("❌ Authentication failed. Cannot proceed with tests requiring authentication.")
    
    # Test Menu System
    print("\n📋 Testing Menu System")
    print("-" * 80)
    
    results["menu_items_get"] = test_get_menu_items()
    
    if auth_success:
        menu_success, menu_item_id = test_create_menu_item()
        results["menu_items_post"] = menu_success
        
        if menu_success and menu_item_id:
            results["menu_items_put"] = test_update_menu_item(menu_item_id)
            results["menu_items_delete"] = test_delete_menu_item(menu_item_id)
        else:
            results["menu_items_put"] = False
            results["menu_items_delete"] = False
            print("❌ Skipping menu item update and delete tests due to failed creation")
    else:
        results["menu_items_post"] = False
        results["menu_items_put"] = False
        results["menu_items_delete"] = False
        print("❌ Skipping menu item creation, update, and delete tests due to failed login")
    
    # Test CMS APIs (German-only)
    print("\n📋 Testing CMS APIs (German-only)")
    print("-" * 80)
    
    results["cms_homepage_hero"] = test_get_cms_homepage_hero()
    results["cms_homepage_features"] = test_get_cms_homepage_features()
    results["cms_homepage_food_gallery"] = test_get_cms_homepage_food_gallery()
    results["cms_homepage_lieferando"] = test_get_cms_homepage_lieferando()
    results["cms_about"] = test_get_cms_about()
    results["cms_locations"] = test_get_cms_locations()
    results["cms_contact"] = test_get_cms_contact()
    
    # Test Newsletter System
    print("\n📋 Testing Newsletter System")
    print("-" * 80)
    
    results["newsletter_subscribe"], subscriber_email = test_newsletter_subscribe()
    
    if auth_success:
        results["newsletter_subscribers_get"] = test_get_newsletter_subscribers()
        results["newsletter_smtp_post"] = test_create_smtp_config()
        results["newsletter_templates_get"] = test_get_newsletter_templates()
        results["newsletter_templates_post"] = test_create_newsletter_template()
        results["newsletter_campaigns_get"] = test_get_newsletter_campaigns()
        results["newsletter_campaigns_post"] = test_create_newsletter_campaign()
    else:
        results["newsletter_subscribers_get"] = False
        results["newsletter_smtp_post"] = False
        results["newsletter_templates_get"] = False
        results["newsletter_templates_post"] = False
        results["newsletter_campaigns_get"] = False
        results["newsletter_campaigns_post"] = False
        print("❌ Skipping newsletter admin tests due to failed login")
    
    # Print summary
    print("\n📋 Test Summary")
    print("=" * 80)
    
    # Authentication summary
    print("\nAuthentication:")
    print("-" * 40)
    auth_tests = ["auth_login", "auth_me"]
    for test_name in auth_tests:
        status = "✅ PASSED" if results[test_name] else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Menu System summary
    print("\nMenu System:")
    print("-" * 40)
    menu_tests = ["menu_items_get", "menu_items_post", "menu_items_put", "menu_items_delete"]
    for test_name in menu_tests:
        status = "✅ PASSED" if results[test_name] else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # CMS APIs summary
    print("\nCMS APIs (German-only):")
    print("-" * 40)
    cms_tests = ["cms_homepage_hero", "cms_homepage_features", "cms_homepage_food_gallery", 
                "cms_homepage_lieferando", "cms_about", "cms_locations", "cms_contact"]
    for test_name in cms_tests:
        status = "✅ PASSED" if results[test_name] else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Newsletter System summary
    print("\nNewsletter System:")
    print("-" * 40)
    newsletter_tests = ["newsletter_subscribe", "newsletter_subscribers_get", "newsletter_smtp_post",
                       "newsletter_templates_get", "newsletter_templates_post", 
                       "newsletter_campaigns_get", "newsletter_campaigns_post"]
    for test_name in newsletter_tests:
        status = "✅ PASSED" if results[test_name] else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Overall result
    all_passed = all(results.values())
    print("\n🏁 Overall Result:", "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED")
    
    return all_passed, results

if __name__ == "__main__":
    success, results = run_final_tests()
    sys.exit(0 if success else 1)