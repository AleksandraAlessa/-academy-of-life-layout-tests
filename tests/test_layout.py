"""Тесты структуры страницы."""
import allure
from playwright.sync_api import Page, expect
from fixtures.design_tokens import EXPECTED_ELEMENTS
import re

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

        def normalize(s: str) -> str:
            # Убираем переводы строк, nbsp и множественные пробелы
            return re.sub(r"\s+", " ", s.replace("\u00a0", " ")).strip()

        normalized_links = [normalize(text) for text in links_text]

        for expected in EXPECTED_ELEMENTS["footer_links"]:
            normalized_expected = normalize(expected)
            found = any(
                normalized_expected in link for link in normalized_links
            )
            assert found, \
                f"Не найдена: {expected}. Есть ссылки: {normalized_links}"