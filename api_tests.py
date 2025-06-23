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

def test_cms_standorte_enhanced():
    """Test GET /api/cms/standorte-enhanced endpoint"""
    print("\n🧪 Testing GET /api/cms/standorte-enhanced endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/standorte-enhanced")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved standorte-enhanced data")
        else:
            print(f"❌ Failed to retrieve standorte-enhanced data. Status code: {response.status_code}")
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
        
        # Check Neustadt location data
        if "neustadt" in data and data["neustadt"]:
            print("✅ Neustadt location data is present")
            neustadt = data["neustadt"]
            
            # Check if Neustadt data contains expected fields
            neustadt_fields = ["name", "address", "phone", "email", "opening_hours", "features"]
            missing_neustadt_fields = [field for field in neustadt_fields if field not in neustadt]
            
            if not missing_neustadt_fields:
                print("✅ Neustadt data contains all required fields")
                print(f"✅ Neustadt address: {neustadt['address']}")
                print(f"✅ Neustadt phone: {neustadt['phone']}")
                print(f"✅ Neustadt email: {neustadt['email']}")
            else:
                print(f"❌ Neustadt data is missing required fields: {missing_neustadt_fields}")
        else:
            print("❌ Neustadt location data is missing or empty")
        
        # Check Großenbrode location data
        if "grossenbrode" in data and data["grossenbrode"]:
            print("✅ Großenbrode location data is present")
            grossenbrode = data["grossenbrode"]
            
            # Check if Großenbrode data contains expected fields
            grossenbrode_fields = ["name", "address", "phone", "email", "opening_hours", "features"]
            missing_grossenbrode_fields = [field for field in grossenbrode_fields if field not in grossenbrode]
            
            if not missing_grossenbrode_fields:
                print("✅ Großenbrode data contains all required fields")
                print(f"✅ Großenbrode address: {grossenbrode['address']}")
                print(f"✅ Großenbrode phone: {grossenbrode['phone']}")
                print(f"✅ Großenbrode email: {grossenbrode['email']}")
            else:
                print(f"❌ Großenbrode data is missing required fields: {missing_grossenbrode_fields}")
        else:
            print("❌ Großenbrode location data is missing or empty")
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/standorte-enhanced endpoint: {e}")
        return False

def test_cms_about():
    """Test GET /api/cms/about endpoint (old version)"""
    print("\n🧪 Testing GET /api/cms/about endpoint (old version)...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/about")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved about page data")
        else:
            print(f"❌ Failed to retrieve about page data. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["page_title", "hero_title", "story_title", "story_content", "team_title", "team_members", "values_title", "values_data"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check team members data
        if "team_members" in data and isinstance(data["team_members"], list):
            print(f"✅ Team members data is present with {len(data['team_members'])} members")
            
            if data["team_members"]:
                # Check first team member
                member = data["team_members"][0]
                member_fields = ["name", "role", "description", "image"]
                missing_member_fields = [field for field in member_fields if field not in member]
                
                if not missing_member_fields:
                    print(f"✅ Team member data contains all required fields")
                    print(f"✅ Team member: {member['name']}, Role: {member['role']}")
                else:
                    print(f"❌ Team member data is missing required fields: {missing_member_fields}")
        else:
            print("❌ Team members data is missing or not a list")
        
        # Check values data
        if "values_data" in data and isinstance(data["values_data"], list):
            print(f"✅ Values data is present with {len(data['values_data'])} values")
            
            if data["values_data"]:
                # Check first value
                value = data["values_data"][0]
                value_fields = ["title", "description", "icon"]
                missing_value_fields = [field for field in value_fields if field not in value]
                
                if not missing_value_fields:
                    print(f"✅ Value data contains all required fields")
                    print(f"✅ Value: {value['title']}")
                else:
                    print(f"❌ Value data is missing required fields: {missing_value_fields}")
        else:
            print("❌ Values data is missing or not a list")
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/about endpoint: {e}")
        return False

def test_cms_ueber_uns_enhanced():
    """Test GET /api/cms/ueber-uns-enhanced endpoint (new version)"""
    print("\n🧪 Testing GET /api/cms/ueber-uns-enhanced endpoint (new version)...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/ueber-uns-enhanced")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved enhanced about page data")
        else:
            print(f"❌ Failed to retrieve enhanced about page data. Status code: {response.status_code}")
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
        
        # Check Jimmy data
        if "jimmy" in data and data["jimmy"]:
            print("✅ Jimmy data is present")
            jimmy = data["jimmy"]
            
            # Check if Jimmy data contains expected fields
            jimmy_fields = ["name", "image", "story_paragraph1", "story_paragraph2", "quote"]
            missing_jimmy_fields = [field for field in jimmy_fields if field not in jimmy]
            
            if not missing_jimmy_fields:
                print("✅ Jimmy data contains all required fields")
                print(f"✅ Jimmy name: {jimmy['name']}")
                print(f"✅ Jimmy quote: {jimmy['quote']}")
            else:
                print(f"❌ Jimmy data is missing required fields: {missing_jimmy_fields}")
        else:
            print("❌ Jimmy data is missing or empty")
        
        # Check values section data
        if "values_section" in data and data["values_section"]:
            print("✅ Values section data is present")
            values = data["values_section"]
            
            # Check if values section contains title
            if "title" in values:
                print(f"✅ Values section title: {values['title']}")
            else:
                print("❌ Values section is missing title")
            
            # Check if at least one value is present
            value_keys = [key for key in values.keys() if key != "title"]
            if value_keys:
                print(f"✅ Values section contains {len(value_keys)} values")
                
                # Check first value
                first_value_key = value_keys[0]
                first_value = values[first_value_key]
                
                value_fields = ["title", "description", "image"]
                missing_value_fields = [field for field in value_fields if field not in first_value]
                
                if not missing_value_fields:
                    print(f"✅ Value data contains all required fields")
                    print(f"✅ Value: {first_value['title']}")
                else:
                    print(f"❌ Value data is missing required fields: {missing_value_fields}")
            else:
                print("❌ Values section does not contain any values")
        else:
            print("❌ Values section data is missing or empty")
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/ueber-uns-enhanced endpoint: {e}")
        return False

def test_cms_kontakt_page():
    """Test GET /api/cms/kontakt-page endpoint"""
    print("\n🧪 Testing GET /api/cms/kontakt-page endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/kontakt-page")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved kontakt page data")
        else:
            print(f"❌ Failed to retrieve kontakt page data. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "page_title", "page_subtitle", "header_background", "contact_form_title", 
                          "contact_form_subtitle", "locations_section_title", "opening_hours_title", "additional_info"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
            print(f"✅ Page title: {data['page_title']}")
            print(f"✅ Contact form title: {data['contact_form_title']}")
            print(f"✅ Locations section title: {data['locations_section_title']}")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/kontakt-page endpoint: {e}")
        return False

def test_contact_post():
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

def test_admin_contact_get():
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

def test_cms_bewertungen_page():
    """Test GET /api/cms/bewertungen-page endpoint"""
    print("\n🧪 Testing GET /api/cms/bewertungen-page endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/bewertungen-page")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved bewertungen page data")
        else:
            print(f"❌ Failed to retrieve bewertungen page data. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "page_title", "page_subtitle", "header_background", "reviews_section_title", 
                          "feedback_section_title", "feedback_note"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
            print(f"✅ Page title: {data['page_title']}")
            print(f"✅ Reviews section title: {data['reviews_section_title']}")
            print(f"✅ Feedback section title: {data['feedback_section_title']}")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/bewertungen-page endpoint: {e}")
        return False

def test_reviews_get():
    """Test GET /api/reviews endpoint"""
    print("\n🧪 Testing GET /api/reviews endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/reviews")
        
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
                
            # Print some sample data
            print(f"📊 Sample reviews:")
            for i, review in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {review['customer_name']} - {review['rating']}★ - {review['comment'][:30]}...")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to reviews endpoint: {e}")
        return False

def test_reviews_post():
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

def test_admin_reviews_pending():
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

def run_tests():
    """Run all tests for the requested APIs"""
    print("\n🔍 Starting Jimmy's Tapas Bar Backend API Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: Authentication
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    if auth_success:
        results["auth_me"] = test_auth_me()
    else:
        results["auth_me"] = False
        print("❌ Skipping auth/me test due to failed login")
    
    # Test 2: Standorte API
    results["cms_standorte_enhanced"] = test_cms_standorte_enhanced()
    
    # Test 3: Über uns APIs
    results["cms_about"] = test_cms_about()
    results["cms_ueber_uns_enhanced"] = test_cms_ueber_uns_enhanced()
    
    # Test 4: Kontakt APIs
    results["cms_kontakt_page"] = test_cms_kontakt_page()
    contact_success, contact_id = test_contact_post()
    results["contact_post"] = contact_success
    
    if auth_success:
        results["admin_contact_get"] = test_admin_contact_get()
    else:
        results["admin_contact_get"] = False
        print("❌ Skipping admin/contact test due to failed login")
    
    # Test 5: Bewertungen APIs
    results["cms_bewertungen_page"] = test_cms_bewertungen_page()
    results["reviews_get"] = test_reviews_get()
    review_success, review_id = test_reviews_post()
    results["reviews_post"] = review_success
    
    if auth_success:
        results["admin_reviews_pending"] = test_admin_reviews_pending()
    else:
        results["admin_reviews_pending"] = False
        print("❌ Skipping admin/reviews/pending test due to failed login")
    
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