from django import template

register = template.Library()

@register.filter()
def flnm(value):
    return value.split('/')[-1]