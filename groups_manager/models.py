from collections import OrderedDict
from uuid import uuid4
import warnings

from django.contrib.auth.models import Group as DjangoGroup
from django.db import models
from django.db.models.signals import post_save, post_delete

from django.apps import apps
django_get_model = apps.get_model

from django.conf import settings as django_settings
from django.contrib.auth.models import User as DefaultUser
DjangoUser = getattr(django_settings, 'AUTH_USER_MODEL', DefaultUser)

from jsonfield import JSONField
from mptt.models import MPTTModel, TreeForeignKey
from slugify import slugify

from groups_manager import exceptions_gm
from groups_manager.perms import assign_object_to_member, assign_object_to_group


def get_auth_models_sync_func_default(instance):
    from groups_manager.settings import GROUPS_MANAGER
    return GROUPS_MANAGER['AUTH_MODELS_SYNC']


class MemberRelationsMixin(object):

    class GroupsManagerMeta:
        group_model = 'groups_manager.Group'
        group_member_model = 'groups_manager.GroupMember'

    @property
    def group_model(self):
        group_model_path = getattr(self.GroupsManagerMeta, 'group_model', 'groups_manager.Group')
        return django_get_model(*group_model_path.split('.'))

    @property
    def group_member_model(self):
        group_member_model_path = getattr(self.GroupsManagerMeta,
                                          'group_member_model', 'groups_manager.GroupMember')
        return django_get_model(*group_member_model_path.split('.'))


class MemberMixin(MemberRelationsMixin, models.Model):
    """Member represents a person that can be related to one or more groups.

    :Parameters:
      - `first_name`: member's first name (required)
      - `last_name`: member's last name (required)
      - `username`: member's username, used as base for django auth's integration
      - `email`: member's email
      - `django_user`: django auth related User
      - `django_auth_sync`: synchronize or not the member (if setting DJANGO_AUTH_SYNC is True)
        (default: True)
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, default='', blank=True)
    email = models.EmailField(max_length=255, default='', blank=True)

    django_auth_sync = models.BooleanField(default=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('last_name', 'first_name')

    def __unicode__(self):
        return self.full_name

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = slugify(self.full_name, to_lower=True, separator="_")
        super(MemberMixin, self).save(*args, **kwargs)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def groups(self):
        message = 'The "groups" attribute will be removed in next version. ' + \
                  'Use "groups_manager_group_set" instead.'
        warnings.warn(message, DeprecationWarning)
        return self.groups_manager_group_set

    def has_perm(self, perm, obj=None):
        """Bind of django user's ``has_perm`` method (use it as a shortcut). """
        try:
            return self.django_user.has_perm(perm, obj)
        except AttributeError:
            raise exceptions_gm.MemberDjangoUserSyncError(
                "Can't check for perm %s since member %s has no django_user" % (perm, self))

    def has_perms(self, perm_list, obj=None):
        """Bind of django user's ``has_perms`` method (use it as a shortcut). """
        try:
            return self.django_user.has_perms(perm_list, obj)
        except AttributeError:
            raise exceptions_gm.MemberDjangoUserSyncError(
                "Can't check for perms %s since member %s has no django_user" % (perm_list, self))

    def assign_object(self, group, obj, **kwargs):
        """Assign an object to the member honours the group relation.

        :Parameters:
          - `group`: the member group (required)
          - `obj`: the object to assign (required)

        :Kwargs:
          - `custom_permissions`: a full or partial redefinition of PERMISSIONS setting.

        .. note::
         This method needs django-guardian.
        """
        group_member = self.group_member_model.objects.get(group=group, member=self)
        return assign_object_to_member(group_member, obj, **kwargs)


class Member(MemberMixin):

    django_user = models.ForeignKey(DjangoUser, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='%(app_label)s_%(class)s_set')

    class Meta(MemberMixin.Meta):
        abstract = False


def member_save(sender, instance, created, *args, **kwargs):
    """
    Add User to Django Users
    """
    from groups_manager.settings import GROUPS_MANAGER
    get_auth_models_sync_func = kwargs.get('get_auth_models_sync_func',
                                           get_auth_models_sync_func_default)
    if get_auth_models_sync_func(instance) and instance.django_auth_sync:
        original_prefix = kwargs.get('prefix', GROUPS_MANAGER['USER_USERNAME_PREFIX'])
        original_suffix = kwargs.get('suffix', GROUPS_MANAGER['USER_USERNAME_SUFFIX'])
        prefix = original_prefix
        suffix = original_suffix
        if suffix == '_$$random':
            suffix = '_%s' % str(uuid4())[:8]
        username = '%s%s%s' % (prefix, instance.username, suffix)
        if not instance.django_user:
            UserModel = instance._meta.get_field('django_user').rel.to
            if GROUPS_MANAGER['AUTH_MODELS_GET_OR_CREATE']:
                django_user, _ = UserModel.objects.get_or_create(username=username)
            else:
                django_user = UserModel(username=username)
            django_user.first_name = instance.first_name
            django_user.last_name = instance.last_name
            if instance.email:
                django_user.email = instance.email
            django_user.save()
            instance.django_user = django_user
            instance.save()
        else:
            if (instance.django_user.username != username and suffix != '_$$random') \
                or (instance.django_user.username[:-len(suffix)] != username[:-len(suffix)] and
                    original_suffix == '_$$random'):
                instance.django_user.username = username
            instance.django_user.first_name = instance.first_name
            instance.django_user.last_name = instance.last_name
            instance.django_user.email = instance.email
            instance.django_user.save()


def member_delete(sender, instance, *args, **kwargs):
    """
    Remove the related Django Group
    """
    get_auth_models_sync_func = kwargs.get('get_auth_models_sync_func',
                                           get_auth_models_sync_func_default)
    if get_auth_models_sync_func(instance) and instance.django_auth_sync:
        if instance.django_user:
            django_user = instance.django_user
            django_user.delete()


post_save.connect(member_save, sender=Member)
post_delete.connect(member_delete, sender=Member)


class GroupTypeMixin(models.Model):
    """This model represents the kind of the group. One group could have only one type.
    This objects could describe the group's nature (i.e. Organization, Division, ecc).

    :Parameters:
      - `label`: (required)
      - `codename`: unique codename; if not set, it's autogenerated by slugifying the label
        (lower case)
    """
    label = models.CharField(max_length=255)
    codename = models.SlugField(unique=True, blank=True, max_length=255)

    class Meta:
        abstract = True
        ordering = ('label', )

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.codename:
            self.codename = slugify(self.label, to_lower=True)
        super(GroupTypeMixin, self).save(*args, **kwargs)

    @property
    def groups(self):
        message = 'The "groups" attribute will be removed in next version. ' + \
                  'Use "groups_manager_group_set" instead.'
        warnings.warn(message, DeprecationWarning)
        return self.groups_manager_group_set


class GroupType(GroupTypeMixin):

    class Meta(GroupTypeMixin.Meta):
        abstract = False


class GroupEntityMixin(models.Model):
    """This model represents the entities of a group. One group could have more than one entity.
    This objects could describe the group's properties (i.e. Administrators, Users, ecc).

    :Parameters:
      - `label`: (required)
      - `codename`: unique codename; if not set, it's autogenerated by slugifying the label
        (lower case)
    """
    label = models.CharField(max_length=255)
    codename = models.SlugField(unique=True, blank=True, max_length=255)

    class Meta:
        abstract = True
        ordering = ('label', )

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.codename:
            self.codename = slugify(self.label, to_lower=True)
        super(GroupEntityMixin, self).save(*args, **kwargs)

    @property
    def groups(self):
        message = 'The "groups" attribute will be removed in next version. ' + \
                  'Use "groups_manager_group_set" instead.'
        warnings.warn(message, DeprecationWarning)
        return self.groups_manager_group_set


class GroupEntity(GroupEntityMixin):

    class Meta(GroupEntityMixin.Meta):
        abstract = False


class GroupRelationsMixin(object):

    class GroupsManagerMeta:
        member_model = 'groups_manager.Member'
        group_member_model = 'groups_manager.GroupMember'
        group_members_attribute = 'group_members'

    @property
    def member_model(self):
        member_model_path = getattr(self.GroupsManagerMeta,
                                    'member_model', 'groups_manager.Member')
        return django_get_model(*member_model_path.split('.'))

    @property
    def group_member_model(self):
        group_member_model_path = getattr(self.GroupsManagerMeta,
                                          'group_member_model', 'groups_manager.GroupMember')
        return django_get_model(*group_member_model_path.split('.'))

    @property
    def group_members_attribute(self):
        return getattr(self.GroupsManagerMeta, 'group_members_attribute', 'group_members')


class GroupMixin(GroupRelationsMixin, MPTTModel):
    """This model represents the group. Each group could have a parent group (via the `parent`
    attribute).

    :Parameters:
      - `name`: (required)
      - `codename`: NON unique codename; if not set, it's autogenerated by slugifying the label
        (lower case)
      - `description`: text field
      - `comment`: text field
      - `full_name`: auto generated full name starting from tree root
      - `properties`: jsonfield properties
      - `group_members`: m2m to Member, through GroupMember model (related name: `groups`)
      - `group_type`: foreign key to GroupType (related name: `groups`)
      - `group_entities`: m2m to GroupEntity (related name: `groups`)
      - `django_group`: django auth related group
      - `django_auth_sync`: synchronize or not the group (if setting DJANGO_AUTH_SYNC is True)
        (default: True)
      - `level`: ``django-mptt`` level attribute
        (default: True)

    .. note::
     If you want to add a custom manager for a sublcass of Group, use django-mptt
     mptt.models.TreeManager.

    """
    name = models.CharField(max_length=255)
    codename = models.SlugField(blank=True, max_length=255)
    description = models.TextField(default='', blank=True)
    comment = models.TextField(default='', blank=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='sub_%(app_label)s_%(class)s_set')
    full_name = models.CharField(max_length=255, default='', blank=True)
    properties = JSONField(default={}, blank=True,
                            load_kwargs={'object_pairs_hook': OrderedDict})

    django_auth_sync = models.BooleanField(default=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('name', )

    class MPTTMeta:
        level_attr = 'level'
        order_insertion_by = ['name', ]

    class GroupsManagerMeta(GroupRelationsMixin.GroupsManagerMeta):
        pass

    def __unicode__(self):
        return '%s' % self.name

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self.full_name = self._get_full_name()[:255]
        if not self.codename:
            self.codename = slugify(self.name, to_lower=True)
        super(GroupMixin, self).save(*args, **kwargs)

    def _get_full_name(self):
        if self.parent:
            return '%s - %s' % (self.parent._get_full_name(), self.name)
        return self.name

    @property
    def subgroups(self):
        message = 'The "subgroups" attribute will be removed in next version. ' + \
                  'Use "sub_groups_manager_group_set" instead.'
        warnings.warn(message, DeprecationWarning)
        return self.sub_groups_manager_group_set

    def get_members(self, subgroups=False):
        """Return group members.
        The result is a list of GroupsManagerMeta's attribute ``member_model`` instances.

        :Parameters:
          - `subgroups`: return also descendants members (default: `False`)
        """
        member_model = self.member_model
        group_member_model = self.group_member_model
        if group_member_model == GroupMember:
            members_relation = getattr(self, self.group_members_attribute)
            if member_model == Member:
                members = list(members_relation.all())
            else:
                # proxy model
                if member_model._meta.proxy:
                    members = list(member_model.objects.filter(
                        id__in=members_relation.values_list('id', flat=True)))
                # subclassed
                else:
                    members = list(member_model.objects.filter(
                        member_ptr__in=members_relation.all()))
        else:
            members = [gm.member for gm in group_member_model.objects.filter(group=self)]
        if subgroups:
            for subgroup in self.subgroups.all():
                members += subgroup.members
        members = list(set(members))
        return members

    @property
    def members(self):
        """Return group members. """
        return self.get_members(True)

    @property
    def users(self):
        """Return group django users. """
        users = []
        for member in self.members:
            if member.django_user:
                users.append(member.django_user)
        return users

    def get_entities(self, subgroups=False):
        """Return group entities.

        :Parameters:
          - `subgroups`: return also descendants entities (default: `False`)
        """
        entities = list(self.group_entities.all())
        if subgroups:
            for subgroup in self.subgroups.all():
                entities += subgroup.entities
            entities = list(set(entities))
        return entities

    @property
    def entities(self):
        """Return group entities."""
        return self.get_entities(True)

    def add_member(self, member, roles=None):
        """Add a member to the group.

        :Parameters:
          - `member`: member (required)
          - `roles`: list of roles. Each role could be a role id, a role label or codename,
            a role instance (optional, default: ``[]``)
        """
        if roles is None:
            roles = []
        if not self.id:
            raise exceptions_gm.GroupNotSavedError(
                "You must save the group before to create a relation with members")
        if not member.id:
            raise exceptions_gm.MemberNotSavedError(
                "You must save the member before to create a relation with groups")
        group_member_model = self.group_member_model
        group_member = group_member_model(member=member, group=self)
        group_member.save()
        if roles:
            for role in roles:
                if isinstance(role, GroupMemberRole):
                    group_member.roles.add(role)
                elif isinstance(role, int):
                    role_obj = GroupMemberRole.objects.get(id=role)
                    group_member.roles.add(role_obj)
                else:
                    try:
                        role_obj = GroupMemberRole.objects.get(models.Q(label=role) |
                                                               models.Q(codename=role))
                        group_member.roles.add(role_obj)
                    except Exception as e:
                        raise exceptions_gm.GetRoleError(e)
        return group_member

    def remove_member(self, member):
        """Remove a member from the group.

        :Parameters:
          - `member`: member (required)
        """
        group_member_model = self.group_member_model
        try:
            group_member = group_member_model.objects.get(member=member, group=self)
        except Exception as e:
            raise exceptions_gm.GetGroupMemberError(e)
        group_member.delete()

    def assign_object(self, obj, **kwargs):
        """Assign an object to the group.

        :Parameters:
          - `obj`: the object to assign (required)

        :Kwargs:
          - `custom_permissions`: a full or partial redefinition of PERMISSIONS setting.

        .. note::
         This method needs django-guardian.
        """
        return assign_object_to_group(self, obj, **kwargs)


class Group(GroupMixin):

    group_type = models.ForeignKey(GroupType, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='%(app_label)s_%(class)s_set')
    group_entities = models.ManyToManyField(GroupEntity, blank=True,
                                            related_name='%(app_label)s_%(class)s_set')

    django_group = models.ForeignKey(DjangoGroup, null=True, blank=True, on_delete=models.SET_NULL)
    group_members = models.ManyToManyField(Member, through='GroupMember',
                                           related_name='%(app_label)s_%(class)s_set')

    class Meta(GroupMixin.Meta):
        abstract = False


def group_save(sender, instance, created, *args, **kwargs):
    """
    Add Group to Django Groups
    """
    from groups_manager.settings import GROUPS_MANAGER
    get_auth_models_sync_func = kwargs.get('get_auth_models_sync_func',
                                           get_auth_models_sync_func_default)
    if get_auth_models_sync_func(instance) and instance.django_auth_sync:
        # create a name compatible with django group name limit of 80 chars
        original_prefix = kwargs.get('prefix', GROUPS_MANAGER['GROUP_NAME_PREFIX'])
        original_suffix = kwargs.get('suffix', GROUPS_MANAGER['GROUP_NAME_SUFFIX'])
        prefix = original_prefix
        suffix = original_suffix
        if suffix == '_$$random':
            suffix = '_%s' % str(uuid4())[:8]
        parent_name = ''
        if instance.parent:
            parent_name = '%s-' % instance.parent.name
        # Django 80-len group name fix: remove from parent
        mid_name = '%s%s' % (parent_name, instance.name)
        name = '%s%s%s' % (prefix, mid_name, suffix)
        if len(name) > 80:
            fix_length = len(prefix) + len(instance.name) + len(suffix)
            name = '%s%s%s%s' % (prefix, parent_name[-(80-fix_length):], instance.name, suffix)
        if not instance.django_group:
            if GROUPS_MANAGER['AUTH_MODELS_GET_OR_CREATE']:
                django_group, _ = DjangoGroup.objects.get_or_create(name=name)
            else:
                django_group = DjangoGroup(name=name)
            django_group.save()
            instance.django_group = django_group
            if instance.parent:
                instance.move_to(instance.parent)
            instance.save(update_fields=['django_group'])
        elif (instance.django_group.name != name and original_suffix != '_$$random') \
                or (instance.django_group.name[:-len(suffix)] != name[:-len(suffix)] and
                    original_suffix == '_$$random'):
            instance.django_group.name = name
            instance.django_group.save()


def group_delete(sender, instance, *args, **kwargs):
    """
    Remove the related Django Group
    """
    get_auth_models_sync_func = kwargs.get('get_auth_models_sync_func',
                                           get_auth_models_sync_func_default)
    if get_auth_models_sync_func(instance) and instance.django_auth_sync:
        if instance.django_group:
            django_group = instance.django_group
            django_group.delete()


post_save.connect(group_save, sender=Group)
post_delete.connect(group_delete, sender=Group)


class GroupMemberRoleMixin(models.Model):
    """This model represents the role of a user in a relation with a group
    (i.e. Administrator, User, ecc).

    :Parameters:
      - `label`: (required)
      - `codename`: unique codename; if not set, it's autogenerated by slugifying the label
        (lower case)
    """
    label = models.CharField(max_length=255)
    codename = models.SlugField(unique=True, blank=True, max_length=255)

    class Meta:
        abstract = True
        ordering = ('label', )

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.codename:
            self.codename = slugify(self.label, to_lower=True)
        super(GroupMemberRoleMixin, self).save(*args, **kwargs)


class GroupMemberRole(GroupMemberRoleMixin):

    class Meta(GroupMemberRoleMixin.Meta):
        abstract = False


class GroupMemberMixin(models.Model):

    class Meta:
        abstract = True
        ordering = ('group', 'member')
        # BUG in Django: https://code.djangoproject.com/ticket/16732
        # unique_together = (('group', 'member'), )

    def __unicode__(self):
        return '%s - %s' % (self.group.name, self.member.full_name)

    def __str__(self):
        return '%s - %s' % (self.group.name, self.member.full_name)

    def assign_object(self, obj, **kwargs):
        """Assign an object to the member.

        :Parameters:
          - `obj`: the object to assign (required)

        :Kwargs:
          - `custom_permissions`: a full or partial redefinition of PERMISSIONS setting.

        .. note::
         This method needs django-guardian.
        """
        return assign_object_to_member(self, obj, **kwargs)


class GroupMember(GroupMemberMixin):
    """This model represents the intermediate model of the relation between a Member and a Group.
    This middleware can have one or more GroupMemberRole associated.
    A member could be in a group only once (group - member pair is unique).

    :Parameters:
      - `group`: Group (required) (defined in non abstract model)
      - `member`: Member (required) (defined in non abstract model)
      - `roles`: m2m to GroupMemberRole
    """

    group = models.ForeignKey(Group, related_name='group_membership')
    member = models.ForeignKey(Member, related_name='group_membership')
    roles = models.ManyToManyField(GroupMemberRole, blank=True)

    class Meta(GroupMemberMixin.Meta):
        unique_together = (('group', 'member'), )  # compatibility with Django < 1.8
        abstract = False


def group_member_save(sender, instance, created, *args, **kwargs):
    """
    Add Django User to Django Groups
    """
    get_auth_models_sync_func = kwargs.get('get_auth_models_sync_func',
                                           get_auth_models_sync_func_default)
    if get_auth_models_sync_func(instance):
        django_user = instance.member.django_user
        django_group = instance.group.django_group
        if django_user and django_group:
            if django_group not in django_user.groups.all():
                django_user.groups.add(django_group)


def group_member_delete(sender, instance, *args, **kwargs):
    """
    Remove Django User from Django Groups
    """
    get_auth_models_sync_func = kwargs.get('get_auth_models_sync_func',
                                           get_auth_models_sync_func_default)
    if get_auth_models_sync_func(instance):
        django_user = instance.member.django_user
        django_group = instance.group.django_group
        if django_user and django_group:
            if django_group in django_user.groups.all():
                django_user.groups.remove(django_group)

post_save.connect(group_member_save, sender=GroupMember)
post_delete.connect(group_member_delete, sender=GroupMember)
