"""Тесты цветов."""
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
        # Body может быть прозрачным — белый фон страницы это дефолт браузера
        valid_values = [
            hex_to_rgb(COLORS["background"]),   # rgb(255, 255, 255)
            "rgba(0, 0, 0, 0)",                 # прозрачный = белый по умолчанию
        ]
        assert bg in valid_values, \
            f"Ожидался белый или прозрачный, получен {bg}"