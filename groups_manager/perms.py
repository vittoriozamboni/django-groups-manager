from distutils.version import StrictVersion
import django

if StrictVersion(django.get_version()) >= StrictVersion('1.6'):
    from django.contrib.auth import get_permission_codename

    def get_permission_name(action, obj):
        return get_permission_codename(action, obj._meta)
else:
    def get_permission_name(action, obj):
        # Follow standard guidelines: 'action_modelname'
        return '%s_%s' % (action, obj._meta.model_name)
