from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, ElementNotInteractableException

def safe_select_by_visible_text(select_elem, text, driver):
    """
    Mehrstufige Auswahl, weil Dropdowns in Web-UIs manchmal nicht sauber interactable sind.
    """
    try:
        Select(select_elem).select_by_visible_text(text)
        return True
    except (ElementNotInteractableException, WebDriverException, Exception):
        pass

    try:
        for opt in select_elem.find_elements("tag name", "option"):
            if opt.text.strip() == text.strip():
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", opt)
                try:
                    opt.click()
                except Exception:
                    driver.execute_script("arguments[0].selected = true;", opt)
                    driver.execute_script(
                        "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
                        select_elem
                    )
                return True
    except Exception:
        pass

    js = """
    var sel = arguments[0];
    var text = arguments[1].trim();
    for (var i=0;i<sel.options.length;i++){
        if (sel.options[i].text.trim() === text){
            sel.selectedIndex = i;
            sel.dispatchEvent(new Event('change', {bubbles:true}));
            return true;
        }
    }
    return false;
    """
    return bool(driver.execute_script(js, select_elem, text))


def mark_order_as_delivered(driver, status_select, save_button):
    ok = safe_select_by_visible_text(status_select, "ausgeliefert", driver)
    if not ok:
        raise RuntimeError("Status konnte nicht gesetzt werden (Fallback fehlgeschlagen).")
    try:
        save_button.click()
    except Exception:
        driver.execute_script("arguments[0].click();", save_button)
