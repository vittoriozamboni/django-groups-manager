import re

from django.test import TestCase

from groups_manager import models
import models as testproject_models

GROUPS_MANAGER_MOCK = {
    'AUTH_MODELS_SYNC': True,
    'GROUP_NAME_PREFIX': '',
    'GROUP_NAME_SUFFIX': '',
    'USER_USERNAME_PREFIX': '',
    'USER_USERNAME_SUFFIX': '',
    'PERMISSIONS': {
        'self': 'vcd',
        'group': 'vc',
        'groups_upstream': 'v',
        'groups_downstream': '',
        'groups_siblings': 'v',
    },
}

random_end = re.compile(r'.*_[a-z0-9]{8}$')


class TestPermissions(TestCase):

    def setUp(self):
        '''
        Silla owns one Legion. There are three groups:
         - Gods, with Mars,
         - Consuls, which Sulla and Metellus Pius are part of,
         - Generals, which Marius is part of,
         - and Plebeians, that has no permissions.
         - Greeks, which Archelaus cannot see anything.
        Mario as General can see Sulla's Legion, and Plebeians neither; Gods can see anything, and
        Metellus Pius has full acess too.
        Gods -|- Consuls - Plebeians
              |- Generals
        Greeks
        '''
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        self.mars = models.Member(first_name='Mars', last_name='Gradivus')
        self.mars.save()
        self.sulla = models.Member(first_name='Lucius', last_name='Sulla')
        self.sulla.save()
        self.metellus = models.Member(first_name='Quintus', last_name='Metellus Pius')
        self.metellus.save()
        self.marius = models.Member(first_name='Caius', last_name='Marius')
        self.marius.save()
        self.quintus = models.Member(first_name='Quintus', last_name='Balbo')
        self.quintus.save()
        self.archelaus = models.Member(first_name='Archelaus', last_name='Cappadocian')
        self.archelaus.save()
        self.gods = models.Group(name='Gods')
        self.gods.save()
        self.generals = models.Group(name='Generals', parent=self.gods)
        self.generals.save()
        self.consuls = models.Group(name='Consuls', parent=self.gods)
        self.consuls.save()
        self.plebeians = models.Group(name='Plebeians', parent=self.consuls)
        self.plebeians.save()
        self.greeks = models.Group(name='Greeks')
        self.greeks.save()
        models.GroupMember.objects.create(group=self.gods, member=self.mars)
        models.GroupMember.objects.create(group=self.consuls, member=self.sulla)
        models.GroupMember.objects.create(group=self.consuls, member=self.metellus)
        models.GroupMember.objects.create(group=self.generals, member=self.marius)
        models.GroupMember.objects.create(group=self.plebeians, member=self.quintus)
        models.GroupMember.objects.create(group=self.greeks, member=self.archelaus)

    def test_standard_permissions(self):
        legio_4 = testproject_models.Legion(name='Legio IV')
        legio_4.save()
        legio_5 = testproject_models.Legion(name='Legio V')
        legio_5.save()
        relation = models.GroupMember.objects.get(group=self.consuls, member=self.sulla)
        relation.assing_object(legio_4)

        # self - read
        self.assertTrue(self.sulla.has_perm('testproject.view_legion', legio_4))
        self.assertFalse(self.sulla.has_perm('testproject.view_legion', legio_5))
        # self - write
        self.assertTrue(self.sulla.has_perm('testproject.change_legion', legio_4))
        # self - delete
        self.assertTrue(self.sulla.has_perm('testproject.delete_legion', legio_4))
        # group
        self.assertTrue(self.metellus.has_perm('testproject.view_legion', legio_4))
        self.assertTrue(self.metellus.has_perm('testproject.change_legion', legio_4))
        self.assertFalse(self.metellus.has_perm('testproject.delete_legion', legio_4))
        # groups - upstream
        self.assertTrue(self.mars.has_perm('testproject.view_legion', legio_4))
        self.assertFalse(self.mars.has_perm('testproject.change_legion', legio_4))
        self.assertFalse(self.mars.has_perm('testproject.delete_legion', legio_4))
        # groups - downstream
        self.assertFalse(self.quintus.has_perm('testproject.view_legion', legio_4))
        self.assertFalse(self.quintus.has_perm('testproject.change_legion', legio_4))
        self.assertFalse(self.quintus.has_perm('testproject.delete_legion', legio_4))
        # groups - sibling
        self.assertTrue(self.marius.has_perm('testproject.view_legion', legio_4))
        self.assertFalse(self.marius.has_perm('testproject.change_legion', legio_4))
        self.assertFalse(self.marius.has_perm('testproject.delete_legion', legio_4))
        # groups - other
        self.assertFalse(self.archelaus.has_perm('testproject.view_legion', legio_4))
        self.assertFalse(self.archelaus.has_perm('testproject.change_legion', legio_4))
        self.assertFalse(self.archelaus.has_perm('testproject.delete_legion', legio_4))

    def test_all_true_permissions(self):
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        custom_permissions = {
            'self': 'vcd',
            'group': 'vcd',
            'groups_upstream': 'vcd',
            'groups_downstream': 'vcd',
            'groups_siblings': 'vcd',
        }
        legio_4 = testproject_models.Legion(name='Legio IV')
        legio_4.save()
        legio_5 = testproject_models.Legion(name='Legio V')
        legio_5.save()
        relation = models.GroupMember.objects.get(group=self.consuls, member=self.sulla)
        relation.assing_object(legio_4, custom_permissions=custom_permissions)

        # self - read
        self.assertTrue(self.sulla.has_perm('testproject.view_legion', legio_4))
        self.assertFalse(self.sulla.has_perm('testproject.view_legion', legio_5))
        # self - write
        self.assertTrue(self.sulla.has_perm('testproject.change_legion', legio_4))
        # self - delete
        self.assertTrue(self.sulla.has_perm('testproject.change_legion', legio_4))
        # group
        self.assertTrue(self.metellus.has_perm('testproject.view_legion', legio_4))
        self.assertTrue(self.metellus.has_perm('testproject.change_legion', legio_4))
        self.assertTrue(self.metellus.has_perm('testproject.delete_legion', legio_4))
        # groups - upstream
        self.assertTrue(self.mars.has_perm('testproject.view_legion', legio_4))
        self.assertTrue(self.mars.has_perm('testproject.change_legion', legio_4))
        self.assertTrue(self.mars.has_perm('testproject.delete_legion', legio_4))
        # groups - downstream
        self.assertTrue(self.quintus.has_perms(
            ['testproject.view_legion', 'testproject.change_legion', 'testproject.delete_legion'],
            legio_4))
        # groups - sibling
        self.assertTrue(self.marius.has_perms(
            ['testproject.view_legion', 'testproject.change_legion', 'testproject.delete_legion'],
            legio_4))
        # groups - other
        self.assertFalse(self.archelaus.has_perms(
            ['testproject.view_legion', 'testproject.change_legion', 'testproject.delete_legion'],
            legio_4))
