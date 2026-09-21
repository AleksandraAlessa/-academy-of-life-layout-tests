"""Тесты шрифтов."""
import allure
from playwright.sync_api import Page
from fixtures.design_tokens import FONTS, FONT_SIZES_BY_VIEWPORT


@allure.epic("Вёрстка")
@allure.feature("Шрифты")
class TestFonts:

    @allure.title("Шрифт body — Montserrat")
    def test_body_font(self, page: Page, base_url: str):
        page.goto(base_url, wait_until="domcontentloaded")
        font = page.evaluate("getComputedStyle(document.body).fontFamily")
        assert FONTS["body"].lower() in font.lower()

    @allure.title("Размер H2 соответствует разрешению")
    def test_h2_size(self, page: Page, base_url: str, viewport):
        page.goto(base_url, wait_until="domcontentloaded")
        h2 = page.locator("h2").first
        size = h2.evaluate("el => getComputedStyle(el).fontSize")
        expected = FONT_SIZES_BY_VIEWPORT[viewport["name"]]["h2"]
        assert size == expected, f"Ожидался {expected}, получен {size}"

    @allure.title("Размер body — 14px")
    def test_body_size(self, page: Page, base_url: str):
        page.goto(base_url, wait_until="domcontentloaded")
        size = page.evaluate("getComputedStyle(document.body).fontSize")
        assert size == "14px"

    @allure.title("Размер шрифта кнопки соответствует разрешению")
    def test_button_size(self, page: Page, base_url: str, viewport):
        page.goto(base_url, wait_until="domcontentloaded")
        button = page.locator(".nheader__btn").first
        size = button.evaluate("el => getComputedStyle(el).fontSize")
        expected = FONT_SIZES_BY_VIEWPORT[viewport["name"]]["button"]
        assert size == expected, f"Ожидался {expected}, получен {size}"