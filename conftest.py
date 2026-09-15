"""Фикстуры для запуска тестов в Chrome и Firefox + Allure."""
import os
import allure
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://academy-of-life.ru"
VIEWPORT = {"width": 1440, "height": 900}


@pytest.fixture(scope="session", params=["chrome", "firefox"], ids=["Chrome", "Firefox"])
def browser_type(request):
    return request.param


@pytest.fixture(scope="session")
def browser_instance(browser_type):
    with sync_playwright() as p:
        if browser_type == "chrome":
            browser = p.chromium.launch(channel="chrome", headless=True)
        else:
            browser = p.firefox.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser_instance):
    context = browser_instance.new_context(viewport=VIEWPORT)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session", autouse=True)
def attach_environment():
    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w", encoding="utf-8") as f:
        f.write(f"Base.URL={BASE_URL}\n")
        f.write("OS=Windows 10\n")
        f.write("Browser=Chrome + Firefox\n")
        f.write("Viewport=1440x900\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            try:
                screenshot = page.screenshot(full_page=True)
                allure.attach(screenshot, name="Screenshot on failure",
                              attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass
