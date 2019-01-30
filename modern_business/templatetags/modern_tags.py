from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    field.field.widget.attrs['class'] = field.field.widget.attrs.get('class', '') + ' ' + css
    return field


@register.filter
def setclass(field, css):
    field.field.widget.attrs['class'] = css
    return field


@register.filter
def placeholder(field, value):
    field.field.widget.attrs['placeholder'] = value
    return field


@register.filter(name='qs')
def query_string(field, value):
    return '&' + str(field) + "=" + str(value)