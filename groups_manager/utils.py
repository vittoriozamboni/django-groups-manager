from django.contrib.auth import get_permission_codename

def get_permission_name(action, obj):
    if action in ['add', 'view', 'change', 'delete']:
        return get_permission_codename(action, obj._meta)
    return action
