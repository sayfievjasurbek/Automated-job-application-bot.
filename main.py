from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

ACCOUNT_EMAIL = "pythonlearingg@gmail.com"
ACCOUNT_PASSWORD = "Samarkand0820!"
PHONE = "+491723566804"

SEARCH_URL = "https://www.linkedin.com/jobs/search/?currentJobId=4204877344&keywords=sales&origin=JOBS_HOME_KEYWORD_SUGGESTION"

driver = webdriver.Chrome()
driver.maximize_window()

# --- LOGIN ---
driver.get("https://www.linkedin.com/login")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(ACCOUNT_EMAIL)
driver.find_element(By.ID, "password").send_keys(ACCOUNT_PASSWORD)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
print("✅ Logged into LinkedIn.")
time.sleep(5)

# --- OPEN JOB SEARCH PAGE ---
driver.get(SEARCH_URL)
time.sleep(5)

# --- GET JOB CARDS ---
job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container--clickable")
print(f"🔍 Found {len(job_cards)} jobs on the page.")

# --- APPLY LOOP ---
for index, card in enumerate(job_cards):
    try:
        print(f"\n➡️ Trying job {index + 1}...")
        card.click()
        time.sleep(3)

        # --- EASY APPLY BUTTON ---
        easy_apply_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button"))
        )
        easy_apply_btn.click()
        print("🟢 Easy Apply opened.")
        time.sleep(2)

        # --- SKIP COMPLEX FORMS ---
        if driver.find_elements(By.XPATH, "//button/span[text()='Next']"):
            print("⏩ Multi-step application. Skipping.")
            driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']").click()
            continue

        if driver.find_elements(By.XPATH, "//input[@type='file']"):
            print("📎 Upload field found. Skipping.")
            driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']").click()
            continue

        if driver.find_elements(By.XPATH, "//textarea[contains(@id, 'text-entity-list-form-component')]"):
            print("📝 Message field found. Skipping.")
            driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']").click()
            continue

        # --- ENTER PHONE IF NEEDED ---
        try:
            phone_input = driver.find_element(By.XPATH, "//input[contains(@id, 'phoneNumber')]")
            phone_input.clear()
            phone_input.send_keys(PHONE)
            print("📞 Phone number entered.")
        except:
            print("ℹ️ No phone field to fill.")

        # --- SUBMIT APPLICATION ---
        submit_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Submit application']"))
        )
        submit_btn.click()
        print("🎯 Application submitted.")

        # --- CLOSE POPUP ---
        time.sleep(2)
        driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']").click()
        print("✅ Application popup closed.")

        time.sleep(2)

    except Exception as e:
        print(f"❌ Failed to apply to job {index + 1}: {e}")
        continue

# --- DONE ---
print("\n✅ Done applying to all suitable jobs.")
driver.quit()
