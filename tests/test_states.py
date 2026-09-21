"""Тесты состояний (hover / focus)."""
import allure
import pytest
from playwright.sync_api import Page
from fixtures.design_tokens import COLORS, hex_to_rgb


@allure.epic("Вёрстка")
@allure.feature("Состояния")
class TestStates:

    @allure.title("Кнопка «Помочь» меняет цвет при hover")
    def test_button_hover(self, page: Page, base_url: str, viewport):
        # На мобильных hover нет — пропускаем
        if viewport["width"] < 992:
            pytest.skip("Hover не работает на мобильных устройствах")

        page.goto(base_url, wait_until="domcontentloaded")
        button = page.locator(".nheader__btn").first

        bg_before = button.evaluate("el => getComputedStyle(el).backgroundColor")
        button.hover()
        page.wait_for_timeout(500)
        bg_after = button.evaluate("el => getComputedStyle(el).backgroundColor")

        assert bg_after != bg_before, f"Цвет не изменился: {bg_before}"
        assert bg_after == hex_to_rgb(COLORS["primary_hover"]), \
            f"Ожидался {hex_to_rgb(COLORS['primary_hover'])}, получен {bg_after}"
