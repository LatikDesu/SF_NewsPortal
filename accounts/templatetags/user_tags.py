from django import template

register = template.Library()


@register.filter(name='filter')
def filter_group(qs, group):
    return qs.filter(name__contains=group)
