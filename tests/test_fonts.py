"""Тесты шрифтов."""
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
