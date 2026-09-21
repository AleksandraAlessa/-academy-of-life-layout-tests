"""Тесты адаптивности вёрстки."""
import allure
from playwright.sync_api import Page, expect


@allure.epic("Вёрстка")
@allure.feature("Адаптивность")
class TestResponsive:

    # ─── Горизонтальный скролл ──────────────────────────────────────────────

    @allure.title("Нет горизонтального скролла")
    def test_no_horizontal_scroll(self, page: Page, base_url: str):
        page.goto(base_url, wait_until="domcontentloaded")
        has_scroll = page.evaluate(
            "document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
        assert has_scroll is False, "Горизонтальный скролл на этом разрешении"

    # ─── Overflow (только видимые элементы) ─────────────────────────────────

    @allure.title("Видимые элементы не выходят за пределы viewport")
    def test_no_overflow(self, page: Page, base_url: str):
        page.goto(base_url, wait_until="domcontentloaded")
        overflowing = page.evaluate("""
            () => Array.from(document.querySelectorAll('*'))
                .filter(el => {
                    const rect = el.getBoundingClientRect();
                    const style = getComputedStyle(el);

                    // Пропускаем невидимые элементы
                    if (rect.width === 0 || rect.height === 0) return false;
                    if (style.visibility === 'hidden') return false;
                    if (style.display === 'none') return false;
                    if (parseFloat(style.opacity) === 0) return false;

                    // Пропускаем элементы внутри overflow: hidden родителей
                    let parent = el.parentElement;
                    while (parent) {
                        const pStyle = getComputedStyle(parent);
                        if (pStyle.overflow === 'hidden' || pStyle.overflowX === 'hidden') {
                            return false;
                        }
                        parent = parent.parentElement;
                    }

                    // Только те, что реально выходят
                    return rect.right > window.innerWidth + 1;
                })
                .length
        """)
        assert overflowing == 0, f"{overflowing} видимых элементов выходят за viewport"

    # ─── Хедер и футер ──────────────────────────────────────────────────────

    @allure.title("Хедер виден на всех разрешениях")
    def test_header_visible(self, page: Page, base_url: str):
        page.goto(base_url, wait_until="domcontentloaded")
        expect(page.locator("header").first).to_be_visible()

    @allure.title("Футер виден на всех разрешениях")
    def test_footer_visible(self, page: Page, base_url: str):
        page.goto(base_url, wait_until="domcontentloaded")
        expect(page.locator("footer").first).to_be_visible()

    # ─── Логотип ────────────────────────────────────────────────────────────

    @allure.title("Логотип виден и не деформирован")
    def test_logo_visible(self, page: Page, base_url: str):
        page.goto(base_url, wait_until="domcontentloaded")
        logo = page.locator(".nheader__logo").first
        expect(logo).to_be_visible()

        box = logo.bounding_box()
        assert box is not None, "Логотип не имеет размеров"
        assert box["width"] > 0, "Логотип имеет нулевую ширину"
        assert box["height"] > 0, "Логотип имеет нулевую высоту"
        # Пропорции: логотип не должен быть растянут по высоте/ширине
        ratio = box["width"] / box["height"]
        assert 1.5 < ratio < 4.0, f"Странные пропорции логотипа: {ratio:.2f}"

    # ─── Контент не вылезает за экран ───────────────────────────────────────

    @allure.title("Основной контент не превышает ширину viewport")
    def test_content_fits_viewport(self, page: Page, base_url: str):
        page.goto(base_url, wait_until="domcontentloaded")
        body_width = page.evaluate("document.body.scrollWidth")
        viewport_width = page.evaluate("window.innerWidth")
        # Допускаем расхождение в 2px (округление)
        assert body_width <= viewport_width + 2, \
            f"body шириной {body_width}px не влезает в viewport {viewport_width}px"