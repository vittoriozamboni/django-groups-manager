from distutils.version import StrictVersion
import django

if StrictVersion(django.get_version()) >= StrictVersion('1.6'):
    from django.contrib.auth import get_permission_codename

    def get_permission_name(action, obj):
        if action in ['add', 'view', 'change', 'delete']:
            return get_permission_codename(action, obj._meta)
        return action
else:
    def get_permission_name(action, obj):
        if action in ['add', 'view', 'change', 'delete']:
            # Follow standard guidelines: 'action_modelname'
            if hasattr(obj._meta, 'model_name'):
                return '%s_%s' % (action, obj._meta.model_name)
            return '%s_%s' % (action, obj._meta.module_name)
        return action
