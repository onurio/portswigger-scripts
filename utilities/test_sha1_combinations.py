#!/usr/bin/env python3
import hashlib

timestamp = "2025-10-01 00:49:58 +0000"
wiener_token = "5918b1c970efd19eba4ed48edfdd6d8cd921b4b9"

# Test different combinations
test_cases = [
    f"{timestamp}wiener",
    f"{timestamp}carlos",
    f"wiener{timestamp}",
    f"carlos{timestamp}",
    f"{timestamp} wiener",
    f"{timestamp} carlos",
    "wiener2025-10-01 00:49:58 +0000",
    "carlos2025-10-01 00:49:58 +0000",
    "2025-10-0100:49:58wiener",
    "2025-10-0100:49:58carlos",
    "wiener1727745058",  # Unix timestamp
    "carlos1727745058",
    "1727745058wiener",
    "1727745058carlos",
    "wiener20251001004958",
    "carlos20251001004958",
    "20251001004958wiener",
    "20251001004958carlos",
]

print(f"Target wiener token: {wiener_token}\n")

for test in test_cases:
    sha1_hash = hashlib.sha1(test.encode()).hexdigest()
    match = "✓ MATCH!" if sha1_hash == wiener_token else ""
    print(f"{test:50s} -> {sha1_hash} {match}")

# Also generate carlos tokens for each pattern
print("\n" + "="*100)
print("CARLOS PREDICTIONS:")
print("="*100 + "\n")

for test in test_cases:
    carlos_variant = test.replace("wiener", "carlos")
    sha1_hash = hashlib.sha1(carlos_variant.encode()).hexdigest()
    print(f"{carlos_variant:50s} -> {sha1_hash}")
