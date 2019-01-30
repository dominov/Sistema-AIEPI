from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return bool(group in user.groups.all())

@register.filter
def is_visible(user, page):
    if page.protected and not user.is_authenticated():
        return False
    if not page.is_visible_in_session and user.is_authenticated():
        return False
    A = set(page.group.all())
    if len(A) == 0:
        return True
    B = set(user.groups.all())
    C = A.intersection(B)
    return bool(len(C))

@register.filter
def distinct(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result