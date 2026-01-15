from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def count_previous_license_usage(driver, license_type):
    """
    Zählt, wie oft eine bestimmte Lizenz in der Vergangenheit für die Lehrperson
    verwendet wurde. Grundlage ist eine Tabelle in der Detailansicht.
    (Tabellen-ID und Spaltenstruktur anonymisiert.)
    """
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "license_usage_table"))  # anonymisiert
    )
    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

    total = 0
    for tr in rows:
        tds = tr.find_elements(By.TAG_NAME, "td")
        if len(tds) < 2:
            continue

        title = tds[0].text.strip()
        amount_text = tds[1].text.strip()

        if license_type.lower() in title.lower():
            # solid Parsen ("1", "2", "1'000")
            cleaned = amount_text.replace("'", "").replace(".", "").replace(",", "")
            try:
                total += int(cleaned)
            except ValueError:
                pass

    return total
