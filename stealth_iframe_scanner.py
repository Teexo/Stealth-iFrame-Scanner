#!/usr/bin/env python3
import os
import time
import random
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from colorama import Fore, Style, init

# Initialize colorama
init()

# ===== CONFIGURATION =====
HOME_DIR = os.path.expanduser("~")
RESULTS_FILE = os.path.join(HOME_DIR, "sqlmap_results.txt")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

# ===== COLOR SETUP =====
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
RESET = Style.RESET_ALL

def verify_file_access():
    """Verify we can write to the results file"""
    global RESULTS_FILE
    
    try:
        with open(RESULTS_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n\n=== New Scan Session: {time.ctime()} ===\n")
        print(f"{GREEN}[✓] Verified write access to: {RESULTS_FILE}{RESET}")
        return True
    except Exception as e:
        print(f"{RED}[X] Cannot write to {RESULTS_FILE}: {e}{RESET}")
        try:
            RESULTS_FILE = "sqlmap_results.txt"
            with open(RESULTS_FILE, "w", encoding="utf-8") as f:
                f.write(f"\n\n=== New Scan Session: {time.ctime()} ===\n")
            print(f"{GREEN}[✓] Using fallback location: {os.path.abspath(RESULTS_FILE)}{RESET}")
            return True
        except Exception as fallback_e:
            print(f"{RED}[X] Critical: Cannot write to any location: {fallback_e}{RESET}")
            return False

def configure_selenium():
    """Set up stealth browser options"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={USER_AGENT}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)

def get_target_url():
    """Prompt for target URL with validation"""
    print(f"\n{YELLOW}{'='*50}")
    print(f"{RED}WARNING: Only test authorized targets!{RESET}")
    print(f"{CYAN}Example safe targets:")
    print("- http://testphp.vulnweb.com")
    print("- http://localhost/dvwa{RESET}")
    print(f"{YELLOW}{'='*50}{RESET}\n")
    
    while True:
        url = input(f"{BLUE}Enter target URL: {RESET}").strip()
        if url.startswith(("http://", "https://")):
            return url
        print(f"{RED}URL must start with http:// or https://{RESET}")

def save_results(data):
    """Save results with extensive error handling"""
    try:
        with open(RESULTS_FILE, "a", encoding="utf-8") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        return True
    except Exception as e:
        print(f"{RED}[X] Failed to save results: {e}{RESET}")
        return False

def run_sqlmap_scan(target_url):
    """Execute SQLmap scan with proper error handling"""
    try:
        print(f"{YELLOW}[*] Preparing SQLmap scan...{RESET}")
        
        # More comprehensive SQLmap command
        sqlmap_cmd = [
            "sqlmap",
            "-u", target_url,
            "--batch",
            "--flush-session",
            "--random-agent",
            f"--delay={random.randint(2,5)}",
            "--tamper=space2comment",
            "--level=3",
            "--risk=2",
            "--dbs",
            "--output-dir=sqlmap_output"
        ]
        
        print(f"{YELLOW}[*] Running SQLmap command: {' '.join(sqlmap_cmd)}{RESET}")
        
        # Create timestamp for this scan
        start_time = time.time()
        timestamp = time.ctime(start_time)
        
        # Run SQLmap with timeout (2 minutes)
        result = subprocess.run(
            sqlmap_cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120
        )
        
        # Prepare report
        report = (
            f"\n\n{'='*80}\n"
            f"SQLmap Scan Report - {timestamp}\n"
            f"Target URL: {target_url}\n"
            f"Command: {' '.join(sqlmap_cmd)}\n"
            f"Duration: {time.time() - start_time:.2f} seconds\n"
            f"{'='*80}\n"
            f"\n=== STDOUT ===\n{result.stdout}\n"
            f"\n=== STDERR ===\n{result.stderr}\n"
            f"\n=== END OF REPORT ===\n"
        )
        
        if save_results(report):
            print(f"{GREEN}[✓] Results saved to {RESULTS_FILE}{RESET}")
        else:
            print(f"{RED}[X] Failed to save results{RESET}")
            
        return True
        
    except subprocess.TimeoutExpired:
        print(f"{RED}[X] SQLmap scan timed out after 2 minutes{RESET}")
        return False
    except Exception as e:
        print(f"{RED}[X] SQLmap execution failed: {str(e)}{RESET}")
        return False

def main():
    if not verify_file_access():
        print(f"{RED}[X] Cannot proceed without file access{RESET}")
        return

    driver = None
    try:
        driver = configure_selenium()
        target_url = get_target_url()

        print(f"\n{GREEN}[+] Scanning: {target_url}{RESET}")
        driver.get(target_url)
        time.sleep(random.uniform(2.0, 5.0))  # More realistic delay
        
        # Find all iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if not iframes:
            print(f"{YELLOW}[!] No iframes detected{RESET}")
        else:
            print(f"{GREEN}[+] Found {len(iframes)} iframe(s){RESET}")
            
            for i, iframe in enumerate(iframes, 1):
                iframe_src = iframe.get_attribute("src")
                if not iframe_src:
                    print(f"{YELLOW}[!] Iframe {i} has no src attribute{RESET}")
                    continue
                
                print(f"\n{CYAN}{i}. iframe URL: {iframe_src}{RESET}")
                
                # Check if URL has parameters
                if "?" in iframe_src:
                    print(f"{MAGENTA}[*] Found parameters in iframe URL{RESET}")
                    user_choice = input(f"{MAGENTA}Test with SQLmap? (y/n): {RESET}").lower()
                    if user_choice == 'y':
                        if not run_sqlmap_scan(iframe_src):
                            print(f"{RED}[X] SQLmap scan failed for {iframe_src}{RESET}")
    
    except Exception as e:
        print(f"{RED}[X] Critical error: {str(e)}{RESET}")
    finally:
        if driver:
            driver.quit()
        if os.path.exists(RESULTS_FILE):
            print(f"\n{GREEN}[+] Final results location: {os.path.abspath(RESULTS_FILE)}{RESET}")
            print(f"{YELLOW}File size: {os.path.getsize(RESULTS_FILE)} bytes{RESET}")
            print(f"{CYAN}You can view results with: cat {RESULTS_FILE}{RESET}")
        else:
            print(f"{RED}[X] No results file was created{RESET}")

if __name__ == "__main__":
    main()
