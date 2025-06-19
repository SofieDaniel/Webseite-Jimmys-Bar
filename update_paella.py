#!/usr/bin/env python3
import requests
import json
import sys

# Use the same backend URL as in backend_test.py
BACKEND_URL = "http://localhost:8001"
API_BASE_URL = f"{BACKEND_URL}/api"

def update_paella_valenciana():
    """Update the preparation_method for Paella Valenciana"""
    print("Updating Paella Valenciana preparation method...")
    
    # First, authenticate to get a token
    auth_payload = {
        "username": "admin",
        "password": "jimmy2024"
    }
    
    auth_response = requests.post(f"{API_BASE_URL}/auth/login", json=auth_payload)
    if auth_response.status_code != 200:
        print(f"Authentication failed: {auth_response.status_code}")
        return False
    
    token = auth_response.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Get all menu items to find Paella Valenciana
    menu_response = requests.get(f"{API_BASE_URL}/menu/items")
    if menu_response.status_code != 200:
        print(f"Failed to get menu items: {menu_response.status_code}")
        return False
    
    menu_items = menu_response.json()
    paella_item = None
    
    for item in menu_items:
        if item["name"] == "Paella Valenciana":
            paella_item = item
            break
    
    if not paella_item:
        print("Paella Valenciana not found in menu items")
        return False
    
    print(f"Found Paella Valenciana with ID: {paella_item['id']}")
    print(f"Current preparation method: {paella_item['preparation_method']}")
    
    # Update the preparation method
    new_preparation_method = "Traditionell in einer flachen Paellapfanne zubereitet, mit angebratenem Reis, der langsam in Brühe gekocht wird, bis er die Aromen vollständig aufgenommen hat. Serviert direkt aus der Pfanne."
    
    update_payload = {
        "preparation_method": new_preparation_method
    }
    
    update_response = requests.put(
        f"{API_BASE_URL}/menu/items/{paella_item['id']}", 
        json=update_payload,
        headers=headers
    )
    
    if update_response.status_code != 200:
        print(f"Failed to update Paella Valenciana: {update_response.status_code}")
        return False
    
    updated_item = update_response.json()
    print(f"Updated preparation method: {updated_item['preparation_method']}")
    print("Update successful!")
    return True

if __name__ == "__main__":
    success = update_paella_valenciana()
    sys.exit(0 if success else 1)