# pip install selenium webdriver-manager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

URL = "http://127.0.0.1:3000/#/contact"  # Change if needed

cnt = 0

def main():


    chrome_opts = Options()
    # chrome_opts.add_argument("--headless=new")  # optional
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_opts
    )

    while True:

        try:
            driver.get(URL)
            wait = WebDriverWait(driver, 10)

            # 1) Read CAPTCHA
            captcha_el = wait.until(EC.visibility_of_element_located((By.ID, "captcha")))
            captcha_text = captcha_el.text.strip()
            print("CAPTCHA:", captcha_text)

            sum = eval(captcha_text, {"__builtins__": None}, {})

            print(sum)

            # 2) Fill textarea
            comment_box = wait.until(EC.element_to_be_clickable((By.ID, "comment")))
            comment_box.clear()
            comment_box.send_keys("test")
            # print("Entered 'test' into textarea.")


            # Wait for textarea and enter text
            comment_box = wait.until(
                EC.element_to_be_clickable((By.ID, "captchaControl"))
            )
            comment_box.clear()
            comment_box.send_keys(sum)

            # print("Entered CAPTCHA into textarea.")

            # 3) Set Angular Material slider to value 2 (target the internal range input)
            slider_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#rating input[type='range']"))
            )

            driver.execute_script("""
                const el = arguments[0];
                const value = arguments[1];

                // Set value on the <input type="range">
                el.value = value;

                // Dispatch events Angular/Material listens to
                el.dispatchEvent(new Event('input',  { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            """, slider_input, 2)

            time.sleep(0.5)

            # print("Set rating slider to 2.")
            # time.sleep(0.5)  # allow UI to update

            # 4) Click submit
            submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "submitButton")))
            submit_btn.click()
            print("Clicked submit button.")

            time.sleep(0.5)

            cnt +=1
            print(f"success: {cnt}")

        except:
            print("ERROR")
            # driver.quit()

if __name__ == "__main__":
    main()