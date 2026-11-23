from django import template
from django.utils.safestring import mark_safe

from core.utils.html_sanitizer import sanitize_rich_html

register = template.Library()


@register.filter(name='safe_html')
def safe_html(value):
    return mark_safe(sanitize_rich_html(value))
