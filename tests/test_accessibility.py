"""Тесты доступности."""
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
