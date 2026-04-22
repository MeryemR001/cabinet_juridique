from django import template

from utilisateurs.permissions import get_role_label, has_permission, has_role

register = template.Library()


@register.filter(name='can')
def can(user, permission_key):
    return has_permission(user, permission_key)


@register.filter(name='role_label')
def role_label(user):
    return get_role_label(user)


@register.filter(name='role_is')
def role_is(user, roles):
    if not roles:
        return False
    if isinstance(roles, str):
        role_list = [role.strip() for role in roles.split(',') if role.strip()]
    else:
        role_list = list(roles)
    return has_role(user, *role_list)
