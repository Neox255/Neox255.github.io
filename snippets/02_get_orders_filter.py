from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

ORDERS_URL = "https://example.internal/app/orders?type=licenses&status=new"
TABLE_ID = "orders_table"

def get_unprocessed_license_orders(driver, timeout=20):
    """
    Lädt die Bestellliste und filtert neue/unverarbeitete Lizenzbestellungen.
    """
    driver.get(ORDERS_URL)
    try:
        table = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, TABLE_ID))
        )
    except TimeoutException:
        return []

    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

    unprocessed = []
    for r in rows:
        try:
            cols = r.find_elements(By.TAG_NAME, "td")
            if len(cols) < 2:
                continue

            # Status-Spalte
            status = cols[-1].text.strip().lower()
            if status in ("neu", "nicht verarbeitet", ""):
                unprocessed.append(r)
        except StaleElementReferenceException:
            continue

    return unprocessed
