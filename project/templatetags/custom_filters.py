

from django import template

register = template.Library()

@register.filter
def truncate_words(value, arg):
    words = value.split()
    if len(words) > arg:
        return ' '.join(words[:arg]) + '...'
    return value


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})