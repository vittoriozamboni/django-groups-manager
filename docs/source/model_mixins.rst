Projects management with Model Mixins
-------------------------------------

Mixins allows to create shared apps based on django-groups-manager.
The mixins approach has pros and cons.

Pros:
 - models are completely customizable (add all fields you need);
 - all fields are in the same table (with subclassed models, only extra fields are stored in the subclass table);
 - better for shared applications (the "original" django-groups-manager tables don't share entries from different models).

Cons:
 - all external foreign keys must be declared in the concrete model;
 - all signals must be declared with concrete models.

Model mixins example
--------------------

The following models allow to manage a set of Organizations with related members (from ``organization`` app).
In this example, a ``last_edit_date`` is added to models, and member display name has the user email (if defined).

**1) Define models in models.py**::

    from groups_manager.models import GroupMixin, MemberMixin, GroupMemberMixin, GroupMemberRoleMixin, \
        GroupEntity, GroupType, \
        group_save, group_delete, member_save, member_delete, group_member_save, group_member_delete


    class OrganizationMemberRole(GroupMemberRoleMixin):
        pass


    class OrganizationGroupMember(GroupMemberMixin):
        group = models.ForeignKey('OrganizationGroup', related_name='group_membership')
        member = models.ForeignKey('OrganizationMember', related_name='group_membership')
        roles = models.ManyToManyField(OrganizationMemberRole, blank=True)


    class OrganizationGroup(GroupMixin):
        last_edit_date = models.DateTimeField(auto_now=True, null=True)
        short_name = models.CharField(max_length=50, default='', blank=True)
        country = CountryField(null=True, blank=True)
        city = models.CharField(max_length=200, blank=True, default='')

        group_type = models.ForeignKey(GroupType, null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='%(app_label)s_%(class)s_set')
        group_entities = models.ManyToManyField(GroupEntity, null=True, blank=True,
                                                related_name='%(app_label)s_%(class)s_set')

        django_group = models.ForeignKey(DjangoGroup, null=True, blank=True, on_delete=models.SET_NULL)
        group_members = models.ManyToManyField('OrganizationMember', through=OrganizationGroupMember,
                                               through_fields=('group', 'member'),
                                               related_name='%(app_label)s_%(class)s_set')

        class Meta:
            permissions = (('manage_organization', 'Manage Organization'),
                           ('view_organization', 'View Organization'))

        class GroupsManagerMeta:
            member_model = 'organizations.OrganizationMember'
            group_member_model = 'organizations.OrganizationGroupMember'

        def save(self, *args, **kwargs):
            if not self.short_name:
                self.short_name = self.name
            super(OrganizationGroup, self).save(*args, **kwargs)

        @property
        def members_names(self):
            return [member.full_name for member in self.group_members.all()]


    class OrganizationMember(MemberMixin):
        last_edit_date = models.DateTimeField(auto_now=True, null=True)
        django_user = models.ForeignKey(DjangoUser, null=True, blank=True, on_delete=models.SET_NULL,
                                        related_name='%(app_label)s_%(class)s_set')

        class GroupsManagerMeta:
            group_model = 'organizations.OrganizationGroup'
            group_member_model = 'organizations.OrganizationGroupMember'

        def __unicode__(self):
            if self.email:
                return '%s (%s)' % (self.full_name, self.email)
            return self.full_name

        def __str__(self):
            if self.email:
                return '%s (%s)' % (self.full_name, self.email)
            return self.full_name


**2) Connect creation and deletion signals to the models**

*(This step is required if you want to sync with django auth models)*::

    post_save.connect(group_save, sender=OrganizationGroup)
    post_delete.connect(group_delete, sender=OrganizationGroup)

    post_save.connect(member_save, sender=OrganizationMember)
    post_delete.connect(member_delete, sender=OrganizationMember)

    post_save.connect(group_member_save, sender=OrganizationGroupMember)
    post_delete.connect(group_member_delete, sender=OrganizationGroupMember)


**3) Customize the flag for AUTH_MODEL_SYNC**

If you plan to create a reusable app and to let users decide if sync or not with Django auth models
**independently** from ``groups_manager`` settings, you should define a separated function that
returns the boolean value from your own settings:
::

    def organization_with_mixin_get_auth_models_sync_func(instance):
        return organization.SETTINGS['DJANGO_AUTH_MODEL_SYNC']  # example

    def organization_group_member_save(*args, **kwargs):
        group_member_save(*args, get_auth_models_sync_func=organization_get_auth_models_sync_func, **kwargs)


    def organization_group_member_delete(*args, **kwargs):
        group_member_delete(*args, get_auth_models_sync_func=organization_get_auth_models_sync_func, **kwargs)


    post_save.connect(organization_group_member_save, sender=OrganizationGroupMember)
    post_delete.connect(organization_group_member_delete, sender=OrganizationGroupMember)


.. note::
 The full tested example is available in repository source code, ``testproject``'s ``tests.py`` under ``test_model_mixins`` method.