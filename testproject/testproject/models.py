from django.db import models
from django.db.models.signals import post_save, post_delete

from mptt.models import TreeManager

from groups_manager.models import Group, Member, GroupType, \
    group_save, group_delete, member_save, member_delete

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
    home = models.ForeignKey(Group, related_name='match_home')
    away = models.ForeignKey(Group, related_name='match_away')

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
