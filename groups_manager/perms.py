import copy

try:
    from guardian.shortcuts import assign_perm
except ImportError:
    def assign_perm(perm_name, group_or_user, obj):
        pass

from groups_manager.utils import get_permission_name


def assign_related(related_groups, perms, obj):
    if isinstance(perms, dict):
        default = set(perms.pop('default', []))

        for group in related_groups:
            django_group = group.django_group

            for permission in default:
                perm_name = get_permission_name(permission, obj)
                assign_perm(perm_name, django_group, obj)

            if group.group_type is not None:
                for permission in set(perms.get(group.group_type.codename, [])):
                    perm_name = get_permission_name(permission, obj)
                    assign_perm(perm_name, django_group, obj)

    else:
        for group in related_groups:
            django_group = group.django_group
            for permission in list(set(perms)):
                perm_name = get_permission_name(permission, obj)
                assign_perm(perm_name, django_group, obj)


def assign_object_to_member(group_member, obj, **kwargs):
    """Assign an object to a GroupMember instance object.

    :Parameters:
      - `group_member`: groups_manager.model.GroupMember instance
      - `obj`: object to set permissions

    :Kwargs:
      - `custom_permissions`: updates settings.GROUPS_MANAGER['PERMISSIONS']
    """
    from groups_manager.settings import GROUPS_MANAGER
    if GROUPS_MANAGER['AUTH_MODELS_SYNC'] and \
            group_member.group.django_group and group_member.member.django_user:
        roles_attr = kwargs.get('roles_attr', 'roles')
        permissions = copy.deepcopy(GROUPS_MANAGER['PERMISSIONS'])
        permissions.update(kwargs.get('custom_permissions', {}))
        # owner
        if isinstance(permissions['owner'], dict):
            roles = getattr(group_member, roles_attr).values_list('codename', flat=True)
            owner_perms = []
            for role in list(set(roles).intersection(set(permissions['owner'].keys()))) + ['default']:
                owner_perms += permissions['owner'].get(role, [])
        else:
            owner_perms = permissions['owner']
        for permission in list(set(owner_perms)):
            perm_name = get_permission_name(permission, obj)
            assign_perm(perm_name, group_member.member.django_user, obj)
        # group
        group_perms = permissions.get('group', [])
        for permission in list(set(group_perms)):
            perm_name = get_permission_name(permission, obj)
            assign_perm(perm_name, group_member.group.django_group, obj)

        # groups_upstream
        upstream_groups = group_member.group.get_ancestors()
        upstream_perms = permissions.get('groups_upstream', [])
        assign_related(upstream_groups, upstream_perms, obj)

        # groups_downstream
        downstream_groups = group_member.group.get_descendants()
        downstream_perms = permissions.get('groups_downstream', [])
        assign_related(downstream_groups, downstream_perms, obj)

        # groups_siblings
        siblings_groups = group_member.group.get_siblings()
        siblings_perms = permissions.get('groups_siblings', [])
        assign_related(siblings_groups, siblings_perms, obj)


def assign_object_to_group(group, obj, **kwargs):
    """Assign an object to a Group instance object.

    :Parameters:
      - `group`: groups_manager.model.Group instance
      - `obj`: object to set permissions

    :Kwargs:
      - `custom_permissions`: updates settings.GROUPS_MANAGER['PERMISSIONS']
    """
    from groups_manager.settings import GROUPS_MANAGER
    if GROUPS_MANAGER['AUTH_MODELS_SYNC'] and group.django_group:
        permissions = copy.deepcopy(GROUPS_MANAGER['PERMISSIONS'])
        permissions.update(kwargs.get('custom_permissions', {}))
        # owner is ignored from permissions
        # group
        group_perms = permissions.get('group', [])
        for permission in list(set(group_perms)):
            perm_name = get_permission_name(permission, obj)
            assign_perm(perm_name, group.django_group, obj)

        # groups_upstream
        upstream_groups = group.get_ancestors()
        upstream_perms = permissions.get('groups_upstream', [])
        assign_related(upstream_groups, upstream_perms, obj)

        # groups_downstream
        downstream_groups = group.get_descendants()
        downstream_perms = permissions.get('groups_downstream', [])
        assign_related(downstream_groups, downstream_perms, obj)

        # groups_siblings
        siblings_groups = group.get_siblings()
        siblings_perms = permissions.get('groups_siblings', [])
        assign_related(siblings_groups, siblings_perms, obj)
