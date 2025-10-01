#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://0a3900c304b67111838b512800a90077.web-security-academy.net"

session = requests.Session()

# Get CSRF token from feedback page
feedback_url = f"{BASE_URL}/feedback"
response = session.get(feedback_url)
soup = BeautifulSoup(response.text, 'html.parser')

csrf = soup.find('input', {'name': 'csrf'})
csrf_token = csrf.get('value') if csrf else None

print(f"[*] CSRF token: {csrf_token}")

# Submit simple H1 tag
payload = '<h1>TEST</h1>'
form_data = {
    'name': payload,
    'email': 'test@test.com', 
    'subject': 'Test',
    'message': 'Test message'
}

if csrf_token:
    form_data['csrf'] = csrf_token

print(f"[*] Submitting payload: {payload}")

submit_response = session.post(
    f"{BASE_URL}/feedback/submit",
    data=form_data,
    headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': feedback_url
    }
)

print(f"[*] Submit response: {submit_response.text}")
print(f"[*] Status code: {submit_response.status_code}")

# Now check the feedback page to see if H1 is rendered
print("\n[*] Checking feedback page for rendered HTML...")
feedback_page = session.get(feedback_url)

# Save the feedback page
with open('feedback_page_after_h1.html', 'w') as f:
    f.write(feedback_page.text)

print("[*] Feedback page saved to feedback_page_after_h1.html")

# Check if our H1 appears
if '<h1>TEST</h1>' in feedback_page.text:
    print("[✓] H1 tag found rendered in page!")
elif 'TEST' in feedback_page.text:
    print("[!] Text 'TEST' found but checking if it's an H1...")
    soup = BeautifulSoup(feedback_page.text, 'html.parser')
    h1_tags = soup.find_all('h1')
    for h1 in h1_tags:
        if 'TEST' in str(h1):
            print(f"[✓] Found as H1: {h1}")
else:
    print("[✗] H1 not found in feedback page")