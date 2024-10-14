# your_app/templatetags/currency_filters.py

# core/templatetags/currency_filters.py

from django import template

register = template.Library()

@register.filter
def convert_to_rupees(value):
    try:
        dollars = float(value)
        rupees = dollars * 290  # Example conversion rate
        return f"{rupees:.2f}Rs"
    except (ValueError, TypeError):
        return value

