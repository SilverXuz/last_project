import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import yaml
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Загрузка конфигурации из файла
with open("config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Локаторы
login_field_locator = config["xpath"]["LOCATOR_LOGIN_FIELD"]
password_field_locator = config["xpath"]["LOCATOR_PASS_FIELD"]
about_link_locator = config["xpath"]["LOCATOR_ABOUT_LINK"]
about_header_locator = config["xpath"]["LOCATOR_ABOUT_HEADER"]

# Учетные данные для авторизации
login = config["login"]
password = config["password"]


@pytest.fixture(scope="session")
def browser():
    service = Service(executable_path=ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def test_login(browser):
    browser.get("https://test-stand.gb.ru")

    # Логин на сайт
    login_field = browser.find_element("xpath", login_field_locator)
    password_field = browser.find_element("xpath", password_field_locator)

    login_field.send_keys(login)
    password_field.send_keys(password)

    login_field.submit()

    # Ожидание, чтобы удостовериться, что авторизация завершена
    WebDriverWait(browser, 10).until(
        EC.url_to_be("https://test-stand.gb.ru/")  # Ждем изменения URL после авторизации
    )

def test_about_page(browser):
    browser.get("https://test-stand.gb.ru")

    # Клик по ссылке "About"
    about_link = browser.find_element("xpath", about_link_locator)
    about_link.click()

    # Ожидание, чтобы удостовериться, что заголовок "About" загрузился
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, about_header_locator))
    )

    # Проверка, что заголовок в окне "About" имеет размер 32px
    about_header = browser.find_element("xpath", about_header_locator)
    font_size = about_header.value_of_css_property("font-size")

    assert font_size == "32px", f"Font size is not 32px, it's {font_size}"


if __name__ == "__main__":
    pytest.main()
