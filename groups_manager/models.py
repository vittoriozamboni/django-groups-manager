from collections import OrderedDict
from uuid import uuid4

from django.contrib.auth.models import Group as DjangoGroup
from django.db import models
from django.db.models.signals import post_save, m2m_changed, post_delete

from django.conf import settings as django_settings
from django.contrib.auth.models import User as DefaultUser
DjangoUser = getattr(django_settings, 'AUTH_USER_MODEL', DefaultUser)

from guardian.shortcuts import assign_perm
from jsonfield import JSONField
from mptt.models import MPTTModel, TreeForeignKey
from slugify import slugify

import exceptions
import perms


class Member(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, default='', blank=True)
    email = models.EmailField(max_length=255, default='', blank=True)

    django_user = models.ForeignKey(DjangoUser, null=True, blank=True, on_delete=models.SET_NULL)
    django_auth_sync = models.BooleanField(default=True, blank=True)

    class Meta:
        ordering = ('last_name', 'first_name')

    def __unicode__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = slugify(self.full_name, to_lower=True, separator="_")
        super(Member, self).save(*args, **kwargs)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        try:
            return self.django_user.has_perm(perm, obj)
        except AttributeError:
            raise exceptions.MemberDjangoUserSyncError(
                "Can't check for perm %s since member %s has no django_user" % (perm, self))

    def has_perms(self, perm_list, obj=None):
        try:
            return self.django_user.has_perms(perm_list, obj)
        except AttributeError:
            raise exceptions.MemberDjangoUserSyncError(
                "Can't check for perms %s since member %s has no django_user" % (perm_list, self))


def member_save(sender, instance, created, *args, **kwargs):
    '''
    Add User to Django Users
    '''
    from settings import GROUPS_MANAGER
    if GROUPS_MANAGER['AUTH_MODELS_SYNC'] and instance.django_auth_sync:
        prefix = GROUPS_MANAGER['USER_USERNAME_PREFIX']
        suffix = GROUPS_MANAGER['USER_USERNAME_SUFFIX']
        if suffix == '_$$random':
            suffix = '_%s' % str(uuid4())[:8]
        username = '%s%s%s' % (prefix, instance.username, suffix)
        if not instance.django_user:
            UserModel = instance._meta.get_field('django_user').rel.to
            django_user = UserModel(
                first_name=instance.first_name,
                last_name=instance.last_name,
                username=username
            )
            if instance.email:
                django_user.email = instance.email
            django_user.save()
            instance.django_user = django_user
            instance.save()
        else:
            if (instance.django_user.username != username and
                suffix != '_$$random') \
                or (instance.django_user.username[:-len(suffix)] != username[:-len(suffix)] and
                    GROUPS_MANAGER['USER_USERNAME_SUFFIX'] == '_$$random'):
                instance.django_user.username = username
            instance.django_user.first_name = instance.first_name
            instance.django_user.last_name = instance.last_name
            instance.django_user.email = instance.email
            instance.django_user.save()


def member_delete(sender, instance, *args, **kwargs):
    '''
    Remove the related Django Group
    '''
    from settings import GROUPS_MANAGER
    if GROUPS_MANAGER['AUTH_MODELS_SYNC'] and instance.django_auth_sync:
        if instance.django_user:
            django_user = instance.django_user
            django_user.delete()


post_save.connect(member_save, sender=Member)
post_delete.connect(member_delete, sender=Member)


class GroupType(models.Model):
    label = models.CharField(max_length=255)
    codename = models.SlugField(unique=True, blank=True, max_length=255)

    class Meta:
        ordering = ('label', )

    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.codename:
            self.codename = slugify(self.label, to_lower=True)
        super(GroupType, self).save(*args, **kwargs)


class GroupEntity(models.Model):
    label = models.CharField(max_length=255)
    codename = models.SlugField(unique=True, blank=True, max_length=255)

    class Meta:
        ordering = ('label', )

    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.codename:
            self.codename = slugify(self.label, to_lower=True)
        super(GroupEntity, self).save(*args, **kwargs)


class Group(MPTTModel):
    name = models.CharField(max_length=255, unique=True)
    codename = models.SlugField(unique=True, blank=True, max_length=255)
    description = models.TextField(default='', blank=True)
    comment = models.TextField(default='', blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='subgroups')
    full_name = models.CharField(max_length=255, default='', blank=True)
    properties = JSONField(default={}, blank=True,
                            load_kwargs={'object_pairs_hook': OrderedDict})
    group_members = models.ManyToManyField(Member, through='GroupMember', related_name='groups')

    group_type = models.ForeignKey(GroupType, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='groups')
    group_entities = models.ManyToManyField(GroupEntity, null=True, blank=True,
                                            related_name='groups')

    django_group = models.ForeignKey(DjangoGroup, null=True, blank=True, on_delete=models.SET_NULL)
    django_auth_sync = models.BooleanField(default=True, blank=True)

    class Meta:
        ordering = ('name', )

    class MPTTMeta:
        level_attr = 'level'
        order_insertion_by = ['name', ]

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self.full_name = self._get_full_name()[:255]
        if not self.codename:
            self.codename = slugify(self.name, to_lower=True)
        super(Group, self).save(*args, **kwargs)

    def _get_full_name(self):
        if self.parent:
            return '%s - %s' % (self.parent._get_full_name(), self.name)
        return self.name

    def get_members(self, subgroups=False):
        members = list(self.group_members.all())
        if subgroups:
            for subgroup in self.subgroups.all():
                members += subgroup.members
        members = list(set(members))
        return members

    @property
    def members(self):
        return self.get_members(True)

    @property
    def users(self):
        users = []
        for member in self.members:
            if member.django_user:
                users.append(member.django_user)
        return users

    def get_entities(self, subgroups=False):
        entities = list(self.group_entities.all())
        if subgroups:
            for subgroup in self.subgroups.all():
                entities += subgroup.entities
            entities = list(set(entities))
        return entities

    @property
    def entities(self):
        return self.get_entities(True)


def group_save(sender, instance, created, *args, **kwargs):
    '''
    Add Group to Django Groups
    '''
    from settings import GROUPS_MANAGER
    if GROUPS_MANAGER['AUTH_MODELS_SYNC'] and instance.django_auth_sync:
        # create a name compatible with django group name limit of 80 chars
        prefix = GROUPS_MANAGER['GROUP_NAME_PREFIX']
        suffix = GROUPS_MANAGER['GROUP_NAME_SUFFIX']
        if suffix == '_$$random':
            suffix = '_%s' % str(uuid4())[:8]
        parent_name = ''
        if instance.parent:
            parent_name = '%s-' % instance.parent.name
        name = '%s%s%s%s' % (prefix, parent_name, instance.name, suffix)
        if not instance.django_group:
            django_group = DjangoGroup(name=name)
            django_group.save()
            instance.django_group = django_group
            instance.save()
        elif (instance.django_group.name != name and
              GROUPS_MANAGER['GROUP_NAME_SUFFIX'] != '_$$random') \
                or (instance.django_group.name[:-len(suffix)] != name[:-len(suffix)] and
                    GROUPS_MANAGER['GROUP_NAME_SUFFIX'] == '_$$random'):
            instance.django_group.name = name
            instance.django_group.save()


def group_delete(sender, instance, *args, **kwargs):
    '''
    Remove the related Django Group
    '''
    from settings import GROUPS_MANAGER
    if GROUPS_MANAGER['AUTH_MODELS_SYNC'] and instance.django_auth_sync:
        if instance.django_group:
            django_group = instance.django_group
            django_group.delete()


post_save.connect(group_save, sender=Group)
post_delete.connect(group_delete, sender=Group)


class GroupMemberRole(models.Model):
    label = models.CharField(max_length=255)
    codename = models.SlugField(unique=True, blank=True, max_length=255)

    class Meta:
        ordering = ('label', )

    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.codename:
            self.codename = slugify(self.label, to_lower=True)
        super(GroupMemberRole, self).save(*args, **kwargs)


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='group_membership')
    member = models.ForeignKey(Member, related_name='group_membership')
    roles = models.ManyToManyField(GroupMemberRole, null=True, blank=True)

    class Meta:
        ordering = ('group', 'member')

    def __unicode__(self):
        return '%s - %s' % (self.group.name, self.member.full_name)

    def assing_object(self, obj, **kwargs):
        from settings import GROUPS_MANAGER
        if GROUPS_MANAGER['AUTH_MODELS_SYNC'] and \
                self.group.django_group and self.member.django_user:
            permissions = {}
            permissions.update(GROUPS_MANAGER['PERMISSIONS'])
            permissions.update(kwargs.get('custom_permissions', {}))
            view_perm = perms.get_permission_name('view', obj)
            change_perm = perms.get_permission_name('change', obj)
            delete_perm = perms.get_permission_name('delete', obj)
            # self
            if 'v' in permissions['self']:
                assign_perm(view_perm, self.member.django_user, obj)
            if 'c' in permissions['self']:
                assign_perm(change_perm, self.member.django_user, obj)
            if 'd' in permissions['self']:
                assign_perm(delete_perm, self.member.django_user, obj)
            # group
            if 'v' in permissions['group']:
                assign_perm(view_perm, self.group.django_group, obj)
            if 'c' in permissions['group']:
                assign_perm(change_perm, self.group.django_group, obj)
            if 'd' in permissions['group']:
                assign_perm(delete_perm, self.group.django_group, obj)
            # groups_upstream
            upstream_groups = [group.django_group for group in self.group.get_ancestors()]
            for django_group in upstream_groups:
                if 'v' in permissions['groups_upstream']:
                    assign_perm(view_perm, django_group, obj)
                if 'c' in permissions['groups_upstream']:
                    assign_perm(change_perm, django_group, obj)
                if 'd' in permissions['groups_upstream']:
                    assign_perm(delete_perm, django_group, obj)
            # groups_downstream
            downstream_groups = [group.django_group for group in self.group.get_descendants()]
            for django_group in downstream_groups:
                if 'v' in permissions['groups_downstream']:
                    assign_perm(view_perm, django_group, obj)
                if 'c' in permissions['groups_downstream']:
                    assign_perm(change_perm, django_group, obj)
                if 'd' in permissions['groups_downstream']:
                    assign_perm(delete_perm, django_group, obj)
            # groups_siblings
            siblings_groups = [group.django_group for group in self.group.get_siblings()]
            for django_group in siblings_groups:
                if 'v' in permissions['groups_siblings']:
                    assign_perm(view_perm, django_group, obj)
                if 'c' in permissions['groups_siblings']:
                    assign_perm(change_perm, django_group, obj)
                if 'd' in permissions['groups_siblings']:
                    assign_perm(delete_perm, django_group, obj)


def group_member_save(sender, instance, created, *args, **kwargs):
    '''
    Add Django User to Django Groups
    '''
    from settings import GROUPS_MANAGER
    if GROUPS_MANAGER['AUTH_MODELS_SYNC']:
        django_user = instance.member.django_user
        django_group = instance.group.django_group
        if django_user and django_group:
            if django_group not in django_user.groups.all():
                django_user.groups.add(django_group)


def group_member_delete(sender, instance, *args, **kwargs):
    '''
    Remove Django User from Django Groups
    '''
    from settings import GROUPS_MANAGER
    if GROUPS_MANAGER['AUTH_MODELS_SYNC']:
        django_user = instance.member.django_user
        django_group = instance.group.django_group
        if django_user and django_group:
            if django_group in django_user.groups.all():
                django_user.groups.remove(django_group)

post_save.connect(group_member_save, sender=GroupMember)
post_delete.connect(group_member_delete, sender=GroupMember)
