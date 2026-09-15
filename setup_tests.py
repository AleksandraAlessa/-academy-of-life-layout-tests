"""Создаёт все файлы тестов для проекта academy-layout-tests."""
from pathlib import Path

FILES = {
    "pytest.ini": """[pytest]
testpaths = tests
addopts = -v -s --alluredir=allure-results --clean-alluredir
""",

    "tests/__init__.py": "",

    "conftest.py": '''"""Фикстуры для запуска тестов в Chrome и Firefox + Allure."""
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
        f.write(f"Base.URL={BASE_URL}\\n")
        f.write("OS=Windows 10\\n")
        f.write("Browser=Chrome + Firefox\\n")
        f.write("Viewport=1440x900\\n")


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
''',

    "tests/test_colors.py": '''"""Тесты цветов."""
import allure
from playwright.sync_api import Page
from fixtures.design_tokens import COLORS, EXPECTED_ELEMENTS, hex_to_rgb


@allure.epic("Вёрстка")
@allure.feature("Цвета")
class TestColors:

    @allure.title("Цвет фона кнопки «Помочь»")
    def test_header_button_bg(self, page: Page, base_url: str):
        page.goto(base_url)
        button = page.locator(".nheader__btn").first
        bg = button.evaluate("el => getComputedStyle(el).backgroundColor")
        assert bg == hex_to_rgb(COLORS["primary"]), f"Ожидался {hex_to_rgb(COLORS['primary'])}, получен {bg}"

    @allure.title("Цвет текста кнопки «Помочь»")
    def test_header_button_text(self, page: Page, base_url: str):
        page.goto(base_url)
        button = page.locator(".nheader__btn").first
        color = button.evaluate("el => getComputedStyle(el).color")
        assert color == hex_to_rgb("#FFFFFF")

    @allure.title("Цвет заголовка H2")
    def test_h2_color(self, page: Page, base_url: str):
        page.goto(base_url)
        h2 = page.locator("h2").first
        color = h2.evaluate("el => getComputedStyle(el).color")
        assert color == hex_to_rgb(COLORS["text_primary"])

    @allure.title("Цвет фона страницы")
    def test_background(self, page: Page, base_url: str):
        page.goto(base_url)
        bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
        assert bg == hex_to_rgb(COLORS["background"])
''',

    "tests/test_fonts.py": '''"""Тесты шрифтов."""
import allure
from playwright.sync_api import Page
from fixtures.design_tokens import FONTS, FONT_SIZES


@allure.epic("Вёрстка")
@allure.feature("Шрифты")
class TestFonts:

    @allure.title("Шрифт body — Montserrat")
    def test_body_font(self, page: Page, base_url: str):
        page.goto(base_url)
        font = page.evaluate("getComputedStyle(document.body).fontFamily")
        assert FONTS["body"].lower() in font.lower()

    @allure.title("Размер H2 — 22px")
    def test_h2_size(self, page: Page, base_url: str):
        page.goto(base_url)
        h2 = page.locator("h2").first
        size = h2.evaluate("el => getComputedStyle(el).fontSize")
        assert size == FONT_SIZES["h2"], f"Ожидался {FONT_SIZES['h2']}, получен {size}"

    @allure.title("Размер body — 14px")
    def test_body_size(self, page: Page, base_url: str):
        page.goto(base_url)
        size = page.evaluate("getComputedStyle(document.body).fontSize")
        assert size == FONT_SIZES["body"]

    @allure.title("Размер шрифта кнопки — 22px")
    def test_button_size(self, page: Page, base_url: str):
        page.goto(base_url)
        button = page.locator(".nheader__btn").first
        size = button.evaluate("el => getComputedStyle(el).fontSize")
        assert size == FONT_SIZES["button"]
''',

    "tests/test_layout.py": '''"""Тесты структуры страницы."""
import allure
from playwright.sync_api import Page, expect
from fixtures.design_tokens import EXPECTED_ELEMENTS


@allure.epic("Вёрстка")
@allure.feature("Структура")
class TestLayout:

    @allure.title("Хедер виден")
    def test_header_visible(self, page: Page, base_url: str):
        page.goto(base_url)
        expect(page.locator("header").first).to_be_visible()

    @allure.title("Футер виден")
    def test_footer_visible(self, page: Page, base_url: str):
        page.goto(base_url)
        expect(page.locator("footer").first).to_be_visible()

    @allure.title("Нет горизонтального скролла")
    def test_no_horizontal_scroll(self, page: Page, base_url: str):
        page.goto(base_url)
        has_scroll = page.evaluate(
            "document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
        assert has_scroll is False

    @allure.title("Кнопка «Помочь» в хедере видна")
    def test_header_button(self, page: Page, base_url: str):
        page.goto(base_url)
        button = page.locator(".nheader__btn").first
        expect(button).to_be_visible()

    @allure.title("Все ссылки футера присутствуют")
    def test_footer_links(self, page: Page, base_url: str):
        page.goto(base_url)
        footer = page.locator("footer").first
        links_text = footer.locator("a").all_text_contents()
        for expected in EXPECTED_ELEMENTS["footer_links"]:
            assert any(expected in text for text in links_text), f"Не найдена: {expected}"
''',

    "tests/test_states.py": '''"""Тесты состояний (hover / focus)."""
import allure
from playwright.sync_api import Page
from fixtures.design_tokens import COLORS, hex_to_rgb


@allure.epic("Вёрстка")
@allure.feature("Состояния")
class TestStates:

    @allure.title("Кнопка «Помочь» меняет цвет при hover")
    def test_button_hover(self, page: Page, base_url: str):
        page.goto(base_url)
        button = page.locator(".nheader__btn").first

        bg_before = button.evaluate("el => getComputedStyle(el).backgroundColor")
        button.hover()
        page.wait_for_timeout(500)
        bg_after = button.evaluate("el => getComputedStyle(el).backgroundColor")

        assert bg_after != bg_before, f"Цвет не изменился: {bg_before}"
        assert bg_after == hex_to_rgb(COLORS["primary_hover"]), \\
            f"Ожидался {hex_to_rgb(COLORS['primary_hover'])}, получен {bg_after}"
''',

    "tests/test_accessibility.py": '''"""Тесты доступности."""
import allure
from playwright.sync_api import Page


@allure.epic("Вёрстка")
@allure.feature("Доступность")
class TestAccessibility:

    @allure.title("Язык страницы — русский")
    def test_html_lang(self, page: Page, base_url: str):
        page.goto(base_url)
        lang = page.locator("html").get_attribute("lang")
        assert lang and lang.startswith("ru")

    @allure.title("У страницы есть title")
    def test_page_title(self, page: Page, base_url: str):
        page.goto(base_url)
        assert len(page.title()) > 0

    @allure.title("Все изображения имеют alt")
    def test_images_have_alt(self, page: Page, base_url: str):
        page.goto(base_url)
        count = page.locator("img:not([alt])").count()
        assert count == 0, f"Найдено {count} изображений без alt"
''',
}


def main():
    for path, content in FILES.items():
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        print(f"✓ {path}")


if __name__ == "__main__":
    main()
    print("\\nВсе файлы созданы!")