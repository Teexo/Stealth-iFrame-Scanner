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
