#!/usr/bin/env python3
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET_HOST = "0a1000fc04d4fc0eb52e0496005100d9.web-security-academy.net"
SESSION = "GPdO56RgzjaIq6mPvQxz7jbi758RfNkf"

# Common GraphQL endpoint paths
endpoints = [
    "/graphql",
    "/graphql/v1",
    "/api/graphql",
    "/v1/graphql",
    "/query",
    "/api",
    "/api/v1",
    "/gql",
    "/graphiql",
    "/console",
    "/api/query",
]

headers = {
    "Cookie": f"session={SESSION}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

# Simple introspection query
test_query = {
    "query": "{ __schema { queryType { name } } }"
}

print("[*] Probing for GraphQL endpoints...\n")

for endpoint in endpoints:
    url = f"https://{TARGET_HOST}{endpoint}"

    try:
        # Try POST with JSON
        response = requests.post(url, headers=headers, json=test_query, verify=False, timeout=5)

        if response.status_code == 200:
            print(f"[+] Found potential endpoint: {endpoint}")
            print(f"    Status: {response.status_code}")
            print(f"    Response length: {len(response.text)}")

            # Check if it looks like GraphQL
            if '"data"' in response.text or '"errors"' in response.text or '__schema' in response.text:
                print(f"    ✓ Confirmed GraphQL endpoint!")
                print(f"    Response snippet: {response.text[:200]}")
            print()

        # Also try GET
        response_get = requests.get(url, headers=headers, verify=False, timeout=5)
        if response_get.status_code in [200, 400] and 'graphql' in response_get.text.lower():
            print(f"[+] GET {endpoint} returned: {response_get.status_code}")
            print(f"    Looks like GraphQL interface")
            print()

    except Exception as e:
        pass

print("\n[*] Probing complete")
