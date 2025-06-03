from django import template
from datetime import timedelta

register = template.Library()


@register.filter
def add_days(date, days):
    try:
        return date + timedelta(days=int(days))
    except (TypeError, ValueError):
        return date


@register.filter
def add(value, arg):
    """Добавляет значение к аргументу"""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        try:
            return value + arg
        except Exception:
            return value


@register.filter(name='times')
def times(number):
    """Генерирует последовательность чисел"""
    return range(1, number + 1)
