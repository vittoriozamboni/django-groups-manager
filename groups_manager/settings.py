from django.conf import settings


GROUPS_MANAGER_SETTINGS = getattr(settings, 'GROUPS_MANAGER', {})

SETTINGS_PERMISSIONS = GROUPS_MANAGER_SETTINGS.get('PERMISSIONS', {})
PERMISSIONS = {
    'owner': ['view', 'change', 'delete'],
    'group': ['view', 'change'],
    'groups_upstream': ['view'],
    'groups_downstream': [],
    'groups_siblings': ['view'],
}
PERMISSIONS.update(SETTINGS_PERMISSIONS)

GROUPS_MANAGER = {
    # User and Groups sync settings
    'AUTH_MODELS_SYNC': GROUPS_MANAGER_SETTINGS.get('AUTH_MODELS_SYNC', False),
    'GROUP_NAME_PREFIX': GROUPS_MANAGER_SETTINGS.get('GROUP_NAME_PREFIX', 'DGM_'),
    'GROUP_NAME_SUFFIX': GROUPS_MANAGER_SETTINGS.get('GROUP_NAME_SUFFIX', '_$$random'),
    'USER_USERNAME_PREFIX': GROUPS_MANAGER_SETTINGS.get('USER_USERNAME_PREFIX', 'DGM_'),
    'USER_USERNAME_SUFFIX': GROUPS_MANAGER_SETTINGS.get('USER_USERNAME_SUFFIX', '_$$random'),
    # Permissions
    'PERMISSIONS': PERMISSIONS,
}
