import time
import os
import pickle
import random
# from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import audio_to_number
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()
EMAIL = os.getenv('email')
PASSWORD = os.getenv('password')
COOKIE_FILE = "cookies.pkl"

def save_cookies(driver, filename=COOKIE_FILE):
    try:
        with open(filename, 'wb') as file:
            pickle.dump(driver.get_cookies(), file)
        print(f"Cookies saved to {filename}")
    except Exception as e:
        print(f"Error saving cookies: {str(e)}")

def load_cookies(driver, filename=COOKIE_FILE):
    try:
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            print(f"Cookies loaded from {filename}")
            return True
        else:
            print(f"No cookie file found at {filename}")
            return False
    except Exception as e:
        print(f"Error loading cookies: {str(e)}")
        return False

def human_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))
def is_captcha_triggered(driver):
    try:
        captcha_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(captcha_iframe)
        
        if captcha_iframe:
            print("Captcha detected")
            human_delay(1, 2)
            try:
                audio_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "captcha__audio__button"))
                )
                print("Audio button found")
                human_delay(1, 3)
                audio_btn.click()
                audio_element = WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "audio-captcha-track"))
                )
                audio_src = audio_element.get_attribute("src")
                print("Audio Source URL:", audio_src)
                captcha_value = audio_to_number.audio_to_number(url=audio_src)
                input_fields = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "audio-captcha-inputs"))
                )
                
                if captcha_value:
                    for i, char in enumerate(captcha_value):
                        if i < len(input_fields):
                            human_delay(0.5, 1.5)  # Slow typing
                            input_fields[i].send_keys(char)
                else:
                    print("captcha is not solved")
            except Exception:
                print("Audio button not found")
            return driver
    except Exception as e:
        print("Captcha not found:", e)
    finally:
        driver.switch_to.default_content()

def login(driver):
    try:
        if not EMAIL or not PASSWORD:
            raise ValueError("Email or password not found in .env file")
      
        driver.get("https://wellfound.com")
        human_delay(2, 4)
        is_captcha_triggered(driver)
        if load_cookies(driver):
            driver.get("https://wellfound.com/login")
            human_delay(2, 4)
            if "login" not in driver.current_url:
                print("Logged in using cookies")
                return
        
        print("Navigating to https://wellfound.com/login...")
        driver.get("https://wellfound.com/login")
        human_delay(2, 4)
        is_captcha_triggered(driver)
        print("Locating email field...")
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user_email"))
        )
        human_delay(1, 3)
        email_field.send_keys(EMAIL)

        print("Locating password field...")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user_password"))
        )
        human_delay(1, 3)
        password_field.send_keys(PASSWORD)
        simulate_human_behavior(driver)
        print("Locating login button...")
        click_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "commit"))
        )
        human_delay(2, 4)
        click_btn.click()
        human_delay(1, 2)

        is_captcha_triggered(driver)
        human_delay(2, 4)

        print("Verifying login...")
        print("Again Locating password field...")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user_password"))
        )
        human_delay(1, 3)
        password_field.send_keys(PASSWORD)

        print("Again locating login button...")
        click_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "commit"))
        )
        human_delay(2, 4)
        click_btn.click()
        human_delay(1, 2)

        save_cookies(driver)

    except Exception as e:
        print(f"Error occurred Login process aborted : {str(e)}")

def setup_driver():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars") 
    chrome_options.add_argument("--start-maximized")
    
    driver = uc.Chrome(options=chrome_options)
    driver.set_window_size(random.randint(1800, 1920), random.randint(1000, 1080))
    return driver
def simulate_human_behavior(driver):

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    human_delay(1, 3)
    driver.execute_script("window.scrollTo(0, 0);")
    human_delay(1, 2)
    actions = ActionChains(driver)
    actions.move_by_offset(random.randint(50, 200), random.randint(50, 200)).perform()
    human_delay(0.5, 1.5)

if __name__ == "__main__":
    driver = None
    try:
        print("Starting browser...")
        driver=setup_driver()
        driver.set_page_load_timeout(30)
        print("Browser started successfully")

        login(driver)
        while True:
            time.sleep(200)
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        if driver:
            try:
                print("Closing browser...")
                save_cookies(driver)  # Update cookies before closing
                driver.quit()
                time.sleep(1)
                print("Browser closed")
            except Exception as e:
                print(f"Error closing browser: {str(e)}")