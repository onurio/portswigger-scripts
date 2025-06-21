# portswigger-scripts

A collection of security testing scripts for PortSwigger Web Security Academy labs.

## Installation

```bash
pip install -r requirements.txt
```

## Scripts

### SQL Injection

#### sql-injection/sql_injection_tester.py

A time-based blind SQL injection vulnerability tester that:
- Tests for SQL injection vulnerabilities using response time delays
- Extracts passwords character by character
- Supports continuous monitoring mode
- Provides detailed logging and debugging information

#### Usage

```bash
# Continuous monitoring (default)
python sql-injection/sql_injection_tester.py https://target-url.com

# Extract password once
python sql-injection/sql_injection_tester.py https://target-url.com --mode extract

# Custom interval for monitoring
python sql-injection/sql_injection_tester.py https://target-url.com --interval 30

# Custom delay threshold
python sql-injection/sql_injection_tester.py https://target-url.com --threshold 2.0
```

#### Options

- `--mode`: Choose between 'extract' (one-time) or 'monitor' (continuous) modes
- `--interval`: Check interval in seconds for monitor mode (default: 5)
- `--threshold`: Response delay threshold in seconds (default: 1.5)
- `--username`: Username to test (default: administrator)

## Disclaimer

These tools are for authorized security testing only. Do not use on systems you do not own or have permission to test.