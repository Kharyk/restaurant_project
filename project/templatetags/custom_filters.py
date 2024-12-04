
from django import template

register = template.Library()


@register.filter
def filter_by_status(queryset, status):
    if queryset is None:
        return queryset  # or return an empty queryset if you prefer
    return queryset.filter(status=status)


@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    else:
        return None 

@register.filter
def truncate_words(value, arg):
    words = value.split()
    if len(words) > arg:
        return ' '.join(words[:arg]) + '...'
    return value


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return None

