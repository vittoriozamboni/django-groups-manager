.. _custom-signals:

Custom signals
--------------

If you redefine models via proxy or subclass and you need to manage sync permissions with
a different setting (like ``MY_APP['AUTH_MODELS_SYNC']`` you need to use different signals functions
when saving objects and relations.
Signals functions accept kwargs:

- ``get_auth_models_sync_func``: a function that returns a boolean (default honours ``GROUPS_MANAGER['AUTH_MODELS_SYNC']`` setting), that also take an ``instance`` parameter to allow additional checks;
- ``prefix`` and ``suffix`` on `group_save```: override ``GROUPS_MANAGER['GROUP_NAME_PREFIX']`` and ``GROUPS_MANAGER['GROUP_NAME_SUFFIX']``;
- ``prefix`` and ``suffix`` on `member_save```: override ``GROUPS_MANAGER['USER_USERNAME_PREFIX']`` and ``GROUPS_MANAGER['USER_USERNAME_SUFFIX']``;

So, for example, your wrapping functions will be like this::

    class ProjectGroup(Group):

        class Meta:
            permissions = (('view_projectgroup', 'View Project Group'), )

        class GroupsManagerMeta:
            member_model = 'testproject.ProjectGroupMember'
            group_member_model = 'testproject.ProjectGroupMember'


    class ProjectMember(Member):

        class Meta:
            permissions = (('view_projectmember', 'View Project Member'), )


    class ProjectGroupMember(GroupMember):
        pass


    def project_get_auth_models_sync_func(instance):
        return MY_APP['AUTH_MODELS_SYNC']


    def project_group_save(*args, **kwargs):
        group_save(*args, get_auth_models_sync_func=project_get_auth_models_sync_func,
                   prefix='PGS_', suffix='_Project', **kwargs)


    def project_group_delete(*args, **kwargs):
        group_delete(*args, get_auth_models_sync_func=project_get_auth_models_sync_func, **kwargs)


    def project_member_save(*args, **kwargs):
        member_save(*args, get_auth_models_sync_func=project_get_auth_models_sync_func,
                    prefix='PMS_', suffix='_Member', **kwargs)


    def project_member_delete(*args, **kwargs):
        member_delete(*args, get_auth_models_sync_func=project_get_auth_models_sync_func, **kwargs)


    def project_group_member_save(*args, **kwargs):
        group_member_save(*args, get_auth_models_sync_func=project_get_auth_models_sync_func, **kwargs)


    def project_group_member_delete(*args, **kwargs):
        group_member_delete(*args, get_auth_models_sync_func=project_get_auth_models_sync_func, **kwargs)


    post_save.connect(project_group_save, sender=ProjectGroup)
    post_delete.connect(project_group_delete, sender=ProjectGroup)

    post_save.connect(project_member_save, sender=ProjectMember)
    post_delete.connect(project_member_delete, sender=ProjectMember)

    post_save.connect(project_group_member_save, sender=ProjectGroupMember)
    post_delete.connect(project_group_member_delete, sender=ProjectGroupMember)


.. note::
 A tested example is available in repository source code, ``testproject``'s ``tests.py`` under
 ``test_signals_kwargs`` method.