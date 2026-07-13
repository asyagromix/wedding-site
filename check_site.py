import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_console_logs():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Enable logging
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("Visiting site...")
        driver.get("https://wedding-site-taupe-eight.vercel.app/")
        
        # Wait a bit for the site to load and React to trigger errors
        time.sleep(5)
        
        print("Dumping console logs:")
        logs = driver.get_log("browser")
        for log in logs:
            if log['level'] == 'SEVERE':
                print(f"[ERROR] {log['message']}")
            else:
                print(f"[{log['level']}] {log['message']}")
                
    finally:
        driver.quit()

if __name__ == "__main__":
    get_console_logs()
