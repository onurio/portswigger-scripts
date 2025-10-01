#!/usr/bin/env python3
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET_HOST = "0a1000fc04d4fc0eb52e0496005100d9.web-security-academy.net"
SESSION = "GPdO56RgzjaIq6mPvQxz7jbi758RfNkf"

# Try common REST endpoints
endpoints = [
    "/login",
    "/api",
    "/",
    "/my-account",
    "/product",
]

headers = {
    "Cookie": f"session={SESSION}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

# Simple introspection query
introspection = {
    "query": "{ __schema { queryType { name } } }"
}

print("[*] Testing REST endpoints for GraphQL support...\n")

for endpoint in endpoints:
    url = f"https://{TARGET_HOST}{endpoint}"

    try:
        print(f"[*] Testing: {endpoint}")

        # Try POST with GraphQL query
        response = requests.post(url, headers=headers, json=introspection, verify=False, timeout=5)

        print(f"    Status: {response.status_code}")
        print(f"    Length: {len(response.text)}")

        # Check for GraphQL indicators
        if ('"data"' in response.text or '"errors"' in response.text or
            '__schema' in response.text or 'queryType' in response.text):
            print(f"    ✓✓✓ GraphQL DETECTED! ✓✓✓")
            print(f"    Response: {response.text[:300]}")
            print()

        # Check for error messages that might hint at GraphQL
        elif 'query' in response.text.lower() or 'graphql' in response.text.lower():
            print(f"    Possible GraphQL hints found")
            print(f"    Snippet: {response.text[:200]}")

        print()

    except Exception as e:
        print(f"    Error: {str(e)}\n")

print("[*] Testing complete")
