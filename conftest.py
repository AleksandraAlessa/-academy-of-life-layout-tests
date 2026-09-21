"""Фикстуры для запуска тестов в Chrome и Firefox + Allure + адаптивность."""
import os
import allure
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://academy-of-life.ru"

# ─── Разрешения для проверки адаптивности ───────────────────────────────────
VIEWPORTS = [
    {"name": "Desktop",   "width": 1440, "height": 900},
    {"name": "Tablet",    "width": 768,  "height": 1024},
    {"name": "Mobile390", "width": 390,  "height": 844},
    {"name": "Mobile320", "width": 320,  "height": 800},
]


# ─── Параметризация браузеров ───────────────────────────────────────────────

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


# ─── Разрешение экрана ──────────────────────────────────────────────────────

@pytest.fixture(scope="function", params=VIEWPORTS, ids=[v["name"] for v in VIEWPORTS])
def viewport(request):
    return request.param


# ─── Страница ───────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def page(browser_instance, viewport):
    context = browser_instance.new_context(
        viewport={"width": viewport["width"], "height": viewport["height"]},
        device_scale_factor=1,
    )
    page = context.new_page()
    page.set_default_timeout(60000)
    page.set_default_navigation_timeout(60000)
    yield page
    context.close()


@pytest.fixture(scope="function")
def base_url():
    return BASE_URL


# ─── Allure: окружение ──────────────────────────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def attach_environment():
    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w", encoding="utf-8") as f:
        f.write(f"Base.URL={BASE_URL}\n")
        f.write("OS=Windows 10\n")
        f.write("Browser=Chrome + Firefox\n")
        f.write("Viewports=1440x900, 768x1024, 390x844, 320x800\n")


# ─── Allure: скриншот при падении ───────────────────────────────────────────

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