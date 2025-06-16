#!/usr/bin/env python3
"""
Clean backend server.py - Remove all old multi-language APIs and keep only German
"""

import re

def clean_backend_apis():
    """Remove all old multi-language CMS APIs"""
    
    print("🔧 Cleaning backend APIs...")
    
    # Read the current server.py
    with open('/app/backend/server.py', 'r') as f:
        content = f.read()
    
    # Find and remove old CMS API blocks (from line ~780 to ~1200)
    lines = content.split('\n')
    
    # Keep everything before old CMS APIs
    clean_lines = []
    skip_mode = False
    
    for i, line in enumerate(lines):
        # Start skipping at old CMS block
        if "# COMPLETE CMS API ENDPOINTS" in line or "# ===============================================" in line and i > 700:
            if any(x in line for x in ["COMPLETE CMS", "Multi-Language", "ENHANCED CMS"]):
                skip_mode = True
                continue
        
        # Stop skipping at Newsletter section
        if "# NEWSLETTER SYSTEM API ENDPOINTS" in line:
            skip_mode = False
            clean_lines.append(line)
            continue
            
        if not skip_mode:
            clean_lines.append(line)
    
    # Write cleaned version
    cleaned_content = '\n'.join(clean_lines)
    
    with open('/app/backend/server.py', 'w') as f:
        f.write(cleaned_content)
    
    print("✅ Backend APIs cleaned")
    print("🗑️  Removed old multi-language CMS APIs")
    print("🇩🇪 Kept only German CMS APIs")

if __name__ == "__main__":
    clean_backend_apis()