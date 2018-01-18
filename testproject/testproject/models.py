from django.db import models
from django.db.models.signals import post_save, post_delete

from mptt.models import TreeManager

from groups_manager.models import Group, Member, GroupType, GroupMember, \
    GroupMixin, MemberMixin, GroupMemberMixin, GroupMemberRoleMixin, GroupEntityMixin, GroupTypeMixin, \
    group_save, group_delete, member_save, member_delete, group_member_save, group_member_delete, \
    DjangoUser, DjangoGroup

'''
Legion main example
'''


class Legion(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (('view_legion', 'View Legion'), )

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


'''
Football team example
'''


class TeamBudget(models.Model):
    euros = models.IntegerField()

    class Meta:
        permissions = (('view_teambudget', 'View team budget'), )


class Match(models.Model):
    home = models.ForeignKey(Group, related_name='match_home', on_delete=models.CASCADE)
    away = models.ForeignKey(Group, related_name='match_away', on_delete=models.CASCADE)

    class Meta:
        permissions = (('view_match', 'View match'),
                       ('play_match', 'Play match'), )


'''
Group permissions example
'''


class ITObject(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (('view_itobject', 'View IT Object'),
                       ('manage_itobject', 'Manage IT Object'), )


class Newsletter(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (('view_newsletter', 'View Newsletter'),
                       ('send_newsletter', 'Send Newsletter'), )


'''
Signals kwargs example with subclass
'''


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
    return True


def project_group_save(*args, **kwargs):
    group_save(*args, get_auth_models_sync_func=project_get_auth_models_sync_func,
               prefix='PGS_', suffix='_Project', **kwargs)


def project_group_delete(*args, **kwargs):
    group_delete(*args, get_auth_models_sync_func=project_get_auth_models_sync_func, **kwargs)


def project_member_save(*args, **kwargs):
    member_save(*args, get_auth_models_sync_func=project_get_auth_models_sync_func,
                prefix='PGS_', suffix='_Project', **kwargs)


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


'''
Roles example
'''


class Site(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (('view_site', 'View site'),
                       ('sell_site', 'Sell site'), )


'''
Proxy example
'''


class ProjectManager(TreeManager):

    def all(self, *args, **kwargs):
        queryset = super(ProjectManager, self).all(*args, **kwargs)
        return queryset.filter(group_type__codename='project')

    def filter(self, *args, **kwargs):
        queryset = super(ProjectManager, self).filter(*args, **kwargs)
        return queryset.filter(group_type__codename='project')


class Project(Group):
    objects = ProjectManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.group_type:
            self.group_type = GroupType.objects.get_or_create(label='Project')[0]
        super(Project, self).save(*args, **kwargs)

post_save.connect(group_save, sender=Project)
post_delete.connect(group_delete, sender=Project)


class WorkGroupManager(TreeManager):

    def all(self, *args, **kwargs):
        queryset = super(WorkGroupManager, self).all(*args, **kwargs)
        return queryset.filter(group_type__codename='workgroup')

    def filter(self, *args, **kwargs):
        queryset = super(WorkGroupManager, self).filter(*args, **kwargs)
        return queryset.filter(group_type__codename='workgroup')


class WorkGroup(Group):
    objects = WorkGroupManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.group_type:
            self.group_type = GroupType.objects.get_or_create(label='Workgroup')[0]
        super(WorkGroup, self).save(*args, **kwargs)

post_save.connect(group_save, sender=WorkGroup)
post_delete.connect(group_delete, sender=WorkGroup)


'''
Proxy Group and Member
'''

def organization_get_auth_models_sync_func(instance):
    return False

class OrganizationMember(Member):

    class Meta:
        proxy = True

post_save.connect(member_save, sender=OrganizationMember)
post_delete.connect(member_delete, sender=OrganizationMember)


class Organization(Group):

    class Meta:
        proxy = True

    class GroupsManagerMeta:
        member_model = 'testproject.OrganizationMember'

post_save.connect(group_save, sender=Organization)
post_delete.connect(group_delete, sender=Organization)


class OrganizationMemberSubclass(Member):
    phone_number = models.CharField(max_length=20)

post_save.connect(member_save, sender=OrganizationMemberSubclass)
post_delete.connect(member_delete, sender=OrganizationMemberSubclass)


class OrganizationSubclass(Group):
    address = models.CharField(max_length=200)

    class GroupsManagerMeta:
        member_model = 'testproject.OrganizationMemberSubclass'

post_save.connect(group_save, sender=OrganizationSubclass)
post_delete.connect(group_delete, sender=OrganizationSubclass)


class Pipeline(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (('view_pipeline', 'View Pipeline'), )


'''
Mixins example
'''


def organization_with_mixin_get_auth_models_sync_func(instance):
    return True


class OrganizationMemberRoleWithMixin(GroupMemberRoleMixin):

    class Meta:
        abstract = False


class OrganizationEntityWithMixin(GroupEntityMixin):

    class Meta:
        abstract = False


class OrganizationTypeWithMixin(GroupMemberRoleMixin):

    class Meta:
        abstract = False


class OrganizationGroupMemberWithMixin(GroupMemberMixin):
    group = models.ForeignKey('OrganizationGroupWithMixin', related_name='group_membership',
                              on_delete=models.CASCADE)
    member = models.ForeignKey('OrganizationMemberWithMixin', related_name='group_membership',
                               on_delete=models.CASCADE)
    roles = models.ManyToManyField(OrganizationMemberRoleWithMixin, blank=True)
    expiration_date = models.DateTimeField(null=True, default=None)


def organization_group_member_save(*args, **kwargs):
    group_member_save(*args, get_auth_models_sync_func=organization_with_mixin_get_auth_models_sync_func, **kwargs)


def organization_group_member_delete(*args, **kwargs):
    group_member_delete(*args, get_auth_models_sync_func=organization_with_mixin_get_auth_models_sync_func, **kwargs)


class OrganizationGroupWithMixin(GroupMixin):
    last_edit_date = models.DateTimeField(auto_now=True, null=True)
    short_name = models.CharField(max_length=50, default='', blank=True)
    city = models.CharField(max_length=200, blank=True, default='')

    group_type = models.ForeignKey(GroupType, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='%(app_label)s_%(class)s_set')
    group_entities = models.ManyToManyField(OrganizationEntityWithMixin, blank=True,
                                            related_name='%(app_label)s_%(class)s_set')

    django_group = models.ForeignKey(DjangoGroup, null=True, blank=True, on_delete=models.SET_NULL)
    group_members = models.ManyToManyField('OrganizationMemberWithMixin', through=OrganizationGroupMemberWithMixin,
                                           through_fields=('group', 'member'),
                                           related_name='%(app_label)s_%(class)s_set')

    class GroupsManagerMeta:
        member_model = 'testproject.OrganizationMemberWithMixin'
        group_member_model = 'testproject.OrganizationGroupMemberWithMixin'

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.name
        super(OrganizationGroupWithMixin, self).save(*args, **kwargs)

    @property
    def members_names(self):
        return [member.full_name for member in self.group_members.all()]


post_save.connect(group_save, sender=OrganizationGroupWithMixin)
post_delete.connect(group_delete, sender=OrganizationGroupWithMixin)


class OrganizationMemberWithMixin(MemberMixin):
    last_edit_date = models.DateTimeField(auto_now=True, null=True)

    django_user = models.ForeignKey(DjangoUser, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='%(app_label)s_%(class)s_set')

    class GroupsManagerMeta:
        group_model = 'testproject.OrganizationGroupWithMixin'
        group_member_model = 'testproject.OrganizationGroupMemberWithMixin'

    def __unicode__(self):
        if self.email:
            return '%s (%s)' % (self.full_name, self.email)
        return self.full_name

    def __str__(self):
        if self.email:
            return '%s (%s)' % (self.full_name, self.email)
        return self.full_name


post_save.connect(member_save, sender=OrganizationMemberWithMixin)
post_delete.connect(member_delete, sender=OrganizationMemberWithMixin)


post_save.connect(organization_group_member_save, sender=OrganizationGroupMemberWithMixin)
post_delete.connect(organization_group_member_delete, sender=OrganizationGroupMemberWithMixin)


class CloudPlatform(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (('view_cloudplatform', 'View Cloud Platform'), )


class SurfaceProduct(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (('view_surfaceproduct', 'View Surface Product'), )


