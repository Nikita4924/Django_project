from django import template

register = template.Library()

@register.filter
def stars(value, max_stars=5):
    """Возвращает строку из ★ и ☆ по рейтингу"""
    try:
        value = int(value)
    except (ValueError, TypeError):
        value = 0
    return "★" * value + "☆" * (max_stars - value)