# Stealth-iFrame-Scanner
A Python tool that automatically detects iframes on web pages and tests them for SQL injection vulnerabilities using SQLmap with stealth techniques.



![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Security](https://img.shields.io/badge/security-tool-red.svg)

## Features

- 🕵️‍♂️ **Stealth scanning** using headless Chrome with randomized delays
- 🔍 **Automatic iframe detection** on target websites
- 🎯 **Smart targeting** of iframes with URL parameters
- 📝 **Comprehensive reporting** with timestamped results
- 🛡️ **Anti-detection** measures including:
  - Random user agents
  - Request delays
  - Tamper scripts
- 📊 **SQLmap integration** with optimized parameters

## Installation

### Prerequisites
- Python 3.7+
- Chrome/Chromium
- SQLmap
- Selenium WebDriver

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/stealth-iframe-scanner.git
cd stealth-iframe-scanner

# Install dependencies
pip install -r requirements.txt


# Install ChromeDriver (Linux example)
sudo apt update
sudo apt install chromium-chromedriver

#Usage
python3 stealth_iframe_scanner.py
When prompted, enter the target URL (must start with http:// or https://).


Example workflow:

-Tool scans the target page for iframes

-Identifies iframes with parameters

-Prompts to test each vulnerable-looking iframe

-Executes SQLmap with optimal stealth settings

-Saves results to ~/sqlmap_results.txt

Configuration
Edit these variables in the script:

RESULTS_FILE = os.path.join(HOME_DIR, "sqlmap_results.txt")  # Output file
USER_AGENT = "Mozilla/5.0 (...)"  # Default user agent
SCAN_DELAY = random.uniform(1.5, 3.5)  # Anti-detection delay


Sample Output:

Enter target URL: https://example.com/vulnerable-page

[+] Scanning: https://example.com/vulnerable-page
[+] Found 3 iframe(s)

1. iframe URL: https://example.com/app?id=123
[*] Found parameters in iframe URL
Test with SQLmap? (y/n): y

[*] Running SQLmap command: sqlmap -u 'https://...' --batch --random-agent...
[✓] Results saved to /home/user/sqlmap_results.txt





