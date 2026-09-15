"""Дизайн-токены сайта БФ «Академия Жизни».

Источники:
- DevTools (шрифты, цвета, размеры) — проверено
- HTML-код сайта (цвета из SVG) — проверено
- CSS-классы (.nheader__btn, .newhome-programs__title) — проверено
"""

# ─── Цвета ──────────────────────────────────────────────────────────────────

COLORS = {
    # Оранжевый — кнопки CTA
    "primary": "#EB5D1D",                # ✅ проверено
    "primary_hover": "#3EBBD5",          # ✅ проверено — становится бирюзовым

    # Тёмный текст
    "text_primary": "#000000",           # ✅
    "text_secondary": "#000000",         # ✅ абзацы тоже чёрные

    # Фоны
    "background": "#FFFFFF",             # ✅
    "background_alt": "#E8F4F9",         # ⚠️ уточнить на секции «Как помочь»
    "footer_bg": "#FFFFFF",              # ✅

    # Акценты (проверено из SVG)
    "accent": "#3EBBD5",                 # бирюзовый
    "accent_dark": "#5368B4",            # тёмно-синий

    # Границы
    "border": "#D6EAF1",                 # ⚠️ уточнить на поле ввода
    "error": "#E53935",
}

# ─── Шрифты ─────────────────────────────────────────────────────────────────

FONTS = {
    "heading": "Montserrat",             # ✅
    "body": "Montserrat",                # ✅
}

FONT_WEIGHTS = {
    "regular": 400,
    "semibold": 600,
    "bold": 700,
}

# ─── Размеры шрифтов ────────────────────────────────────────────────────────

FONT_SIZES = {
    "h1": "22px",                        # ✅ (H1 нет, размер как у H2)
    "h2": "22px",                        # ✅
    "h3": "18px",                        # ⚠️
    "body": "14px",                      # ✅
    "button": "22px",                    # ✅
    "small": "12px",                     # ⚠️
}

# ─── Кнопки (из CSS .nheader__btn) ──────────────────────────────────────────

BUTTON_STYLES = {
    "border_radius": "65px",             # ✅ «таблетка»
    "padding": "10px 30px 10px 35px",    # ✅
    "font_weight": 600,                  # ✅
    "font_size": "22px",                 # ✅
    "line_height": "118%",               # ✅
    "transition": "all 0.3s",            # ✅
}

# ─── Стили H2 (из CSS .newhome-programs__title) ─────────────────────────────

H2_STYLES = {
    "font_weight": 700,
    "font_size": "22px",
    "line_height": "209%",
    "text_transform": "uppercase",
    "color": "#000000",
    "margin_bottom": "32px",
}

# ─── Ожидаемые элементы — проверено из HTML ─────────────────────────────────

EXPECTED_ELEMENTS = {
    "header_button": "Помочь",
    "header_menu": ["О фонде", "Программы", "Как помочь", "Отчеты"],
    "donation_button": "Поддержать работу фонда",
    "volunteer_button": "Стать волонтером",
    "subscribe_button": "Подписаться на рассылку",
    "footer_links": [
        "Уставные документы",
        "Контакты и реквизиты",
        "Для бизнеса",
        "О социальной проблеме",
    ],
    "footer_legal_links": [
        "Политика безопасности платежей",
        "Политика конфиденциальности",
        "Сведения об обработке персональных данных",
        "Пользовательское соглашение",
    ],
    "phone": "+7 (495) 198-12-23",
    "email": "info@academy-of-life.ru",
    "address": "123376, г. Москва, ул. Красная Пресня, д. 22",
}


def hex_to_rgb(hex_color: str) -> str:
    """Перевод HEX в rgb() — getComputedStyle возвращает rgb."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgb({r}, {g}, {b})"