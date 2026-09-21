import allure
import pytest
from playwright.sync_api import Page, expect


@allure.epic("Вёрстка")
@allure.feature("Мобильная вёрстка")
class TestMobile:

    @allure.title("Меню-бургер виден на мобильных")
    def test_burger_visible_mobile(self, page: Page, base_url: str, viewport):
        if viewport["width"] > 991:
            pytest.skip("Только для мобильных разрешений")
        page.goto(base_url, wait_until="domcontentloaded")
        burger = page.locator(".nheader__burg").first
        expect(burger).to_be_visible()

    @allure.title("Меню-бургер скрыт на десктопе")
    def test_burger_hidden_desktop(self, page: Page, base_url: str, viewport):
        if viewport["width"] <= 991:
            pytest.skip("Только для десктопа")
        page.goto(base_url, wait_until="domcontentloaded")
        burger = page.locator(".nheader__burg").first
        expect(burger).to_be_hidden()

    @allure.title("Кнопки не меньше 44px (touch-цели)")
    def test_touch_targets(self, page: Page, base_url: str, viewport):
        if viewport["width"] > 991:
            pytest.skip("Только для мобильных")
        page.goto(base_url, wait_until="domcontentloaded")
        buttons = page.locator("button, a.btn, .nheader__btn")
        count = buttons.count()
        small = []
        for i in range(count):
            box = buttons.nth(i).bounding_box()
            if box and box["height"] > 0 and box["height"] < 44:
                small.append((i, box["height"]))
        assert not small, f"Маленькие кнопки: {small}"

    @allure.title("Логотип виден на мобильном")
    def test_logo_visible(self, page: Page, base_url: str, viewport):
        if viewport["width"] > 991:
            pytest.skip("Только для мобильных")
        page.goto(base_url, wait_until="domcontentloaded")
        logo = page.locator(".nheader__logo").first
        expect(logo).to_be_visible()