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

# Full introspection query
introspection_query = {
    "query": """
    {
        __schema {
            queryType { name }
            mutationType { name }
            types {
                name
                kind
                fields {
                    name
                    args {
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
                    type {
                        name
                        kind
                        ofType {
                            name
                            kind
                        }
                    }
                }
                inputFields {
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

print("[*] Performing GraphQL introspection...\n")
response = requests.post(TARGET, headers=headers, json=introspection_query, verify=False)

if response.status_code == 200:
    data = response.json()

    if 'errors' in data:
        print("[-] Introspection returned errors:")
        print(json.dumps(data['errors'], indent=2))
        exit(1)

    schema = data.get('data', {}).get('__schema', {})
    types = schema.get('types', [])

    print(f"[+] Query Type: {schema.get('queryType', {}).get('name')}")
    print(f"[+] Mutation Type: {schema.get('mutationType', {}).get('name')}\n")

    # Display all queries
    print("="*60)
    print("QUERIES")
    print("="*60)
    for t in types:
        if t['name'] == schema.get('queryType', {}).get('name'):
            if t.get('fields'):
                for field in t['fields']:
                    args = ', '.join([f"{arg['name']}: {arg['type'].get('name', 'Unknown')}"
                                     for arg in field.get('args', [])])
                    return_type = field['type'].get('name', 'Unknown')
                    if field['type'].get('ofType'):
                        return_type = field['type']['ofType'].get('name', return_type)

                    print(f"\n{field['name']}({args}): {return_type}")

    # Display all mutations
    print("\n" + "="*60)
    print("MUTATIONS")
    print("="*60)
    for t in types:
        if t['name'] == schema.get('mutationType', {}).get('name'):
            if t.get('fields'):
                for field in t['fields']:
                    args_list = []
                    for arg in field.get('args', []):
                        arg_type = arg['type'].get('name', 'Unknown')
                        if arg['type'].get('ofType'):
                            arg_type = arg['type']['ofType'].get('name', arg_type)
                        args_list.append(f"{arg['name']}: {arg_type}")

                    args = ', '.join(args_list)
                    return_type = field['type'].get('name', 'Unknown')
                    if field['type'].get('ofType'):
                        return_type = field['type']['ofType'].get('name', return_type)

                    print(f"\n{field['name']}({args}): {return_type}")

    # Display input types
    print("\n" + "="*60)
    print("INPUT TYPES")
    print("="*60)
    for t in types:
        if t['kind'] == 'INPUT_OBJECT':
            print(f"\n{t['name']}:")
            if t.get('inputFields'):
                for field in t['inputFields']:
                    field_type = field['type'].get('name', 'Unknown')
                    if field['type'].get('ofType'):
                        field_type = field['type']['ofType'].get('name', field_type)
                    print(f"  - {field['name']}: {field_type}")

    # Display object types
    print("\n" + "="*60)
    print("OBJECT TYPES")
    print("="*60)
    for t in types:
        if t['kind'] == 'OBJECT' and not t['name'].startswith('__'):
            print(f"\n{t['name']}:")
            if t.get('fields'):
                for field in t['fields']:
                    field_type = field['type'].get('name', 'Unknown')
                    if field['type'].get('ofType'):
                        field_type = field['type']['ofType'].get('name', field_type)
                    print(f"  - {field['name']}: {field_type}")

else:
    print(f"[-] Request failed: {response.status_code}")
    print(f"Response: {response.text}")
