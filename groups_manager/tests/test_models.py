import os
import re

from django.contrib.auth.models import Group as DjangoGroup
from django.test import TestCase

from groups_manager import models, exceptions


GROUPS_MANAGER_MOCK = {
    'AUTH_MODELS_SYNC': True,
    'GROUP_NAME_PREFIX': 'DGM_',
    'GROUP_NAME_SUFFIX': '_$$random',
    'USER_USERNAME_PREFIX': 'DGM_',
    'USER_USERNAME_SUFFIX': '_$$random',
    'PERMISSIONS': {
        'owner': ['view', 'change', 'delete'],
        'group': ['view', 'change'],
        'groups_upstream': ['view'],
        'groups_downstream': [],
        'groups_siblings': ['view'],
    },
}

random_end = re.compile(r'.*_[a-z0-9]{8}$')


class TestMember(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.member = models.Member(
            first_name='Lucio',
            last_name='Silla',
            username='lucio_silla',)

    def test_unicode(self):
        self.assertEqual(unicode(self.member), 'Lucio Silla')

    def test_full_name(self):
        self.assertEqual(self.member.full_name, 'Lucio Silla')

    def test_save_auto_create_username(self):
        member = models.Member.objects.create(first_name='Giulio', last_name='Cesare',
                                              email='julius_caesar@ancient_rome.com')
        self.assertEqual(member.username, 'giulio_cesare')

    def test_member_save(self):
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        member = models.Member.objects.create(first_name='Caio', last_name='Mario')
        self.assertIsNotNone(member.django_user)
        self.assertTrue(member.django_user.username.startswith(
                GROUPS_MANAGER_MOCK['USER_USERNAME_PREFIX']))
        self.assertTrue(re.search(random_end, member.django_user.username))

    def test_member_save_no_prefix_suffix(self):
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        settings.GROUPS_MANAGER['USER_USERNAME_PREFIX'] = ''
        settings.GROUPS_MANAGER['USER_USERNAME_SUFFIX'] = ''
        member = models.Member.objects.create(first_name='Caio', last_name='Mario')
        self.assertEqual(member.username, member.django_user.username)

    def test_has_perm_exception(self):
        member = models.Member(first_name='Caio', last_name='Mario')
        with self.assertRaises(exceptions.MemberDjangoUserSyncError):
            member.has_perm('view_member', member)

    def test_has_perms_exception(self):
        member = models.Member(first_name='Caio', last_name='Mario')
        with self.assertRaises(exceptions.MemberDjangoUserSyncError):
            member.has_perms(['view_member'], member)


class TestGroupType(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.group_type = models.GroupType(label='Organization')

    def test_unicode(self):
        self.assertEqual(str(self.group_type), self.group_type.label)

    def test_save(self):
        self.group_type.save()
        self.assertEqual(self.group_type.codename, 'organization')


class TestGroupEntity(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.group_entity = models.GroupEntity(label='Organization Partner')

    def test_unicode(self):
        self.assertEqual(str(self.group_entity), self.group_entity.label)

    def test_save(self):
        self.group_entity.save()
        self.assertEqual(self.group_entity.codename, 'organization-partner')


class TestGroup(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.group = models.Group(name='Istituto di Genomica Applicata')

    def test_unicode(self):
        self.assertEqual(str(self.group), self.group.name)

    def test_save(self):
        group = models.Group.objects.create(name='Istituto di Genomica Applicata')
        self.assertEqual(group.codename, 'istituto-di-genomica-applicata')
        self.assertEqual(group.full_name, group.name)

    def test_nested_group(self):
        main = models.Group.objects.create(name='Main')
        subgroup = models.Group.objects.create(name='Sub Group', parent=main)
        self.assertEqual(subgroup.full_name, 'Main - Sub Group')

    def test_nested_entities(self):
        e1 = models.GroupEntity.objects.create(label='Partner')
        e2 = models.GroupEntity.objects.create(label='Customer')
        main = models.Group.objects.create(name='Main')
        main.group_entities.add(e1)
        subgroup = models.Group.objects.create(name='Sub Group', parent=main)
        subgroup.group_entities.add(e2)
        self.assertEqual(main.entities, [e1, e2])
        self.assertEqual(subgroup.entities, [e2])

    def test_nested_members(self):
        m1 = models.Member.objects.create(first_name='Caio', last_name='Mario')
        m2 = models.Member.objects.create(first_name='Lucio', last_name='Silla')
        main = models.Group.objects.create(name='Main')
        subgroup = models.Group.objects.create(name='Sub Group', parent=main)
        models.GroupMember.objects.create(group=main, member=m1)
        models.GroupMember.objects.create(group=subgroup, member=m2)
        self.assertEqual(main.members, [m1, m2])
        self.assertEqual(subgroup.members, [m2])

    def test_group_save(self):
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        group = models.Group(name='Main Group')
        group.save()
        self.assertIsNotNone(group.django_group)
        self.assertTrue(group.django_group.name.startswith(
                GROUPS_MANAGER_MOCK['GROUP_NAME_PREFIX']))
        self.assertTrue(re.search(random_end, group.django_group.name))

    def test_group_save_no_prefix_suffix(self):
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        settings.GROUPS_MANAGER['GROUP_NAME_PREFIX'] = ''
        settings.GROUPS_MANAGER['GROUP_NAME_SUFFIX'] = ''
        group = models.Group.objects.create(name='Main Group')
        self.assertEqual(group.name, group.django_group.name)

    def test_group_save_parent_no_prefix_suffix(self):
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        settings.GROUPS_MANAGER['GROUP_NAME_PREFIX'] = ''
        settings.GROUPS_MANAGER['GROUP_NAME_SUFFIX'] = ''
        group = models.Group.objects.create(name='Main Group')
        subgroup = models.Group(name='Sub group', parent=group)
        subgroup.save()
        self.assertEqual(subgroup.django_group.name, 'Main Group-Sub group')

    def test_group_save_django_group_change_name(self):
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        settings.GROUPS_MANAGER['GROUP_NAME_PREFIX'] = ''
        settings.GROUPS_MANAGER['GROUP_NAME_SUFFIX'] = ''
        group = models.Group.objects.create(name='Main Group')
        group.name = 'Test change'
        group.save()
        self.assertEqual(group.django_group.name, group.name)

    def test_nested_users(self):
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        m1 = models.Member.objects.create(first_name='Caio', last_name='Mario')
        m2 = models.Member.objects.create(first_name='Lucio', last_name='Silla')
        main = models.Group.objects.create(name='Main')
        subgroup = models.Group.objects.create(name='Sub Group', parent=main)
        models.GroupMember.objects.create(group=main, member=m1)
        models.GroupMember.objects.create(group=subgroup, member=m2)
        self.assertEqual(main.users, [m1.django_user, m2.django_user])
        self.assertEqual(subgroup.users, [m2.django_user])

    def test_add_member(self):
        dictators = models.Group(name='Dictators')
        dictators.save()
        sulla = models.Member(first_name='Lucius', last_name='Sulla')
        sulla.save()
        membership = dictators.add_member(sulla)
        self.assertEqual(membership.group, dictators)
        self.assertEqual(membership.member, sulla)

    def test_add_member_unsaved_group(self):
        dictators = models.Group(name='Dictators')
        sulla = models.Member(first_name='Lucius', last_name='Sulla')
        sulla.save()
        with self.assertRaises(exceptions.GroupNotSavedError):
            dictators.add_member(sulla)

    def test_add_member_unsaved_member(self):
        dictators = models.Group.objects.create(name='Dictators')
        sulla = models.Member(first_name='Lucius', last_name='Sulla')
        with self.assertRaises(exceptions.MemberNotSavedError):
            dictators.add_member(sulla)

    def test_add_member_with_role(self):
        romans = models.Group.objects.create(name='Romans')
        sulla = models.Member.objects.create(first_name='Lucius', last_name='Sulla')
        dictator = models.GroupMemberRole.objects.create(label='Dictator')
        membership = romans.add_member(sulla, [dictator])
        self.assertEqual(membership.group, romans)
        self.assertEqual(membership.member, sulla)
        self.assertIn(dictator, membership.roles.all())
        # role from ID
        caesar = models.Member.objects.create(first_name='Julius', last_name='Caesar')
        membership = romans.add_member(caesar, [dictator.id])
        self.assertIn(dictator, membership.roles.all())
        # role from codename
        plebeian = models.GroupMemberRole.objects.create(label='Plebeian')
        manlius = models.Member.objects.create(first_name='Quintus', last_name='Manlius')
        membership = romans.add_member(manlius, ['plebeian'])
        self.assertIn(plebeian, membership.roles.all())
        # role from label
        caius = models.Member.objects.create(first_name='Caius', last_name='Petronius')
        membership = romans.add_member(caius, ['Plebeian'])
        self.assertIn(plebeian, membership.roles.all())
        # invalid role
        valerius = models.Member.objects.create(first_name='Valerius', last_name='Postumos')
        with self.assertRaises(exceptions.GetRoleError):
            romans.add_member(valerius, [{'role': 'invalid'}])

    def test_assign_object(self):
        romans = models.Group.objects.create(name='Romans')
        with self.assertRaises(NotImplementedError):
            romans.assign_object(romans)


class TestGroupMemberRole(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.group_member_role = models.GroupMemberRole(label='Administrator')

    def test_unicode(self):
        self.assertEqual(str(self.group_member_role), self.group_member_role.label)

    def test_save(self):
        self.group_member_role.save()
        self.assertEqual(self.group_member_role.codename, 'administrator')


class TestGroupMember(TestCase):

    def test_unicode(self):
        m1 = models.Member.objects.create(first_name='Caio', last_name='Mario')
        main = models.Group.objects.create(name='Main')
        gm = models.GroupMember.objects.create(group=main, member=m1)
        self.assertEqual(str(gm), '%s - %s' % (gm.group.name, gm.member.full_name))

    def test_groups_membership_django_integration(self):
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        m1 = models.Member.objects.create(first_name='Caio', last_name='Mario')
        m2 = models.Member.objects.create(first_name='Lucio', last_name='Silla')
        main = models.Group.objects.create(name='Main')
        subgroup = models.Group.objects.create(name='Sub Group', parent=main)
        gm1 = models.GroupMember.objects.create(group=main, member=m1)
        models.GroupMember.objects.create(group=subgroup, member=m2)
        self.assertTrue(main.django_group in m1.django_user.groups.all())
        self.assertTrue(subgroup.django_group in m2.django_user.groups.all())
        # Test remove membership
        gm1.delete()
        self.assertFalse(main.django_group in m1.django_user.groups.all())
        # Test remove user
        username = m1.django_user.username
        m1.delete()
        UserModel = m1._meta.get_field('django_user').rel.to
        self.assertEqual(len(UserModel.objects.filter(username=username)), 0)
        # Test remove group
        name = main.django_group.name
        main.delete()
        self.assertEqual(len(DjangoGroup.objects.filter(name=name)), 0)
