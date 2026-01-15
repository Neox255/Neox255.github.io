import os
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver):
    """
    Login über Umgebungsvariablen (.env)
    """
    load_dotenv()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    if not username or not password:
        raise RuntimeError("USERNAME/PASSWORD fehlen (bitte in .env setzen).")

    driver.get("https://example.internal/app/login")  # anonymisiert
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "usr")))

    driver.find_element(By.NAME, "usr").clear()
    driver.find_element(By.NAME, "usr").send_keys(username)

    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "pwd").send_keys(password + Keys.RETURN)
