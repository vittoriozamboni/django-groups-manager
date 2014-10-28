import copy

try:
    from guardian.shortcuts import assign_perm
except ImportError:
    def assign_perm(perm_name, group_or_user, obj):
        pass

from .utils import get_permission_name


def assign_object_to_member(group_member, obj, **kwargs):
    """Assign an object to a GroupMember instance object.
    """
    from settings import GROUPS_MANAGER
    if GROUPS_MANAGER['AUTH_MODELS_SYNC'] and \
            group_member.group.django_group and group_member.member.django_user:
        roles_attr = kwargs.get('roles_attr', 'roles')
        permissions = copy.deepcopy(GROUPS_MANAGER['PERMISSIONS'])
        permissions.update(kwargs.get('custom_permissions', {}))
        view_perm = get_permission_name('view', obj)
        change_perm = get_permission_name('change', obj)
        delete_perm = get_permission_name('delete', obj)
        # owner
        permission = permissions['owner']
        if isinstance(permission, dict):
            roles = getattr(group_member, roles_attr).values_list('codename', flat=True)
            permission = ''.join([permission.get(k, '') for k in
                    list(set(roles).union(set(permission.keys()))) + ['default']])
        if 'v' in permission:
            assign_perm(view_perm, group_member.member.django_user, obj)
        if 'c' in permission:
            assign_perm(change_perm, group_member.member.django_user, obj)
        if 'd' in permission:
            assign_perm(delete_perm, group_member.member.django_user, obj)
        # group
        permission = permissions.get('group', '')
        if 'v' in permission:
            assign_perm(view_perm, group_member.group.django_group, obj)
        if 'c' in permission:
            assign_perm(change_perm, group_member.group.django_group, obj)
        if 'd' in permission:
            assign_perm(delete_perm, group_member.group.django_group, obj)
        # groups_upstream
        upstream_groups = [group.django_group for group in group_member.group.get_ancestors()]
        for django_group in upstream_groups:
            permission = permissions.get('groups_upstream', '')
            if 'v' in permission:
                assign_perm(view_perm, django_group, obj)
            if 'c' in permission:
                assign_perm(change_perm, django_group, obj)
            if 'd' in permission:
                assign_perm(delete_perm, django_group, obj)
        # groups_downstream
        downstream_groups = \
            [group.django_group for group in group_member.group.get_descendants()]
        for django_group in downstream_groups:
            permission = permissions.get('groups_downstream', '')
            if 'v' in permission:
                assign_perm(view_perm, django_group, obj)
            if 'c' in permission:
                assign_perm(change_perm, django_group, obj)
            if 'd' in permission:
                assign_perm(delete_perm, django_group, obj)
        # groups_siblings
        siblings_groups = [group.django_group for group in group_member.group.get_siblings()]
        for django_group in siblings_groups:
            permission = permissions.get('groups_siblings', '')
            if 'v' in permission:
                assign_perm(view_perm, django_group, obj)
            if 'c' in permission:
                assign_perm(change_perm, django_group, obj)
            if 'd' in permission:
                assign_perm(delete_perm, django_group, obj)
