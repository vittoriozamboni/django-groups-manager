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
        'owner': 'vcd',
        'group': 'vc',
        'groups_upstream': 'v',
        'groups_downstream': '',
        'groups_siblings': 'v',
    },
}

random_end = re.compile(r'.*_[a-z0-9]{8}$')


class TestPermissions(TestCase):

    def setUp(self):
        pass

    def create_legions(self):
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
        self.mars = models.Member.objects.create(first_name='Mars', last_name='Gradivus')
        self.sulla = models.Member.objects.create(first_name='Lucius', last_name='Sulla')
        self.metellus = models.Member.objects.create(first_name='Quintus', last_name='Metellus Pius')
        self.marius = models.Member.objects.create(first_name='Caius', last_name='Marius')
        self.quintus = models.Member.objects.create(first_name='Quintus', last_name='Balbo')
        self.archelaus = models.Member.objects.create(first_name='Archelaus', last_name='Cappadocian')
        self.gods = models.Group.objects.create(name='Gods')
        self.generals = models.Group.objects.create(name='Generals', parent=self.gods)
        self.consuls = models.Group.objects.create(name='Consuls', parent=self.gods)
        self.plebeians = models.Group.objects.create(name='Plebeians', parent=self.consuls)
        self.greeks = models.Group.objects.create(name='Greeks')
        models.GroupMember.objects.create(group=self.gods, member=self.mars)
        models.GroupMember.objects.create(group=self.consuls, member=self.sulla)
        models.GroupMember.objects.create(group=self.consuls, member=self.metellus)
        models.GroupMember.objects.create(group=self.generals, member=self.marius)
        models.GroupMember.objects.create(group=self.plebeians, member=self.quintus)
        models.GroupMember.objects.create(group=self.greeks, member=self.archelaus)

    def test_standard_permissions(self):
        self.create_legions()
        legio_4 = testproject_models.Legion(name='Legio IV')
        legio_4.save()
        legio_5 = testproject_models.Legion(name='Legio V')
        legio_5.save()
        relation = models.GroupMember.objects.get(group=self.consuls, member=self.sulla)
        relation.assing_object(legio_4)

        # owner - read
        self.assertTrue(self.sulla.has_perm('testproject.view_legion', legio_4))
        self.assertFalse(self.sulla.has_perm('testproject.view_legion', legio_5))
        # owner - write
        self.assertTrue(self.sulla.has_perm('testproject.change_legion', legio_4))
        # owner - delete
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
        self.create_legions()
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        custom_permissions = {
            'owner': 'vcd',
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

        # owner - read
        self.assertTrue(self.sulla.has_perm('testproject.view_legion', legio_4))
        self.assertFalse(self.sulla.has_perm('testproject.view_legion', legio_5))
        # owner - write
        self.assertTrue(self.sulla.has_perm('testproject.change_legion', legio_4))
        # owner - delete
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

    def test_proxy_models(self):
        """
        John Boss is the project leader. Marcus Worker and Julius Backend are the
        django backend guys; Teresa Html is the front-end developer and Jack College is the
        student that has to learn to write good backends.
        The Celery pipeline is owned by Marcus, and Jack must see it without intercations.
        Teresa can't see the pipeline, but John has full permissions as project leader.
        As part of the backend group, Julius has the right of viewing and editing, but not to
        stop (delete) the pipeline.
        """
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        custom_permissions = {
            'owner': 'vcd',
            'group': 'vc',
            'groups_upstream': 'vcd',
            'groups_downstream': 'v',
            'groups_siblings': '',
        }
        project_main = testproject_models.Project(name='Workgroups Main Project')
        project_main.save()
        django_backend = testproject_models.WorkGroup(name='WorkGroup Backend', parent=project_main)
        django_backend.save()
        django_backend_watchers = testproject_models.WorkGroup(name='Backend Watchers',
                                                            parent=django_backend)
        django_backend_watchers.save()
        django_frontend = testproject_models.WorkGroup(name='WorkGroup FrontEnd', parent=project_main)
        django_frontend.save()
        self.assertTrue(len(testproject_models.Project.objects.all()), 1)
        self.assertTrue(len(testproject_models.WorkGroup.objects.all()), 3)
        self.assertTrue(len(testproject_models.WorkGroup.objects.filter(name__startswith='W')), 2)

        john = models.Member.objects.create(first_name='John', last_name='Boss')
        project_main.add_member(john)
        marcus = models.Member.objects.create(first_name='Marcus', last_name='Worker')
        julius = models.Member.objects.create(first_name='Julius', last_name='Backend')
        django_backend.add_member(marcus)
        django_backend.add_member(julius)
        teresa = models.Member.objects.create(first_name='Teresa', last_name='Html')
        django_frontend.add_member(teresa)
        jack = models.Member.objects.create(first_name='Jack', last_name='College')
        django_backend_watchers.add_member(jack)

        pipeline = testproject_models.Pipeline.objects.create(name='Test Runner')
        marcus.assing_object(django_backend, pipeline, custom_permissions=custom_permissions)

        # owner
        self.assertTrue(marcus.has_perms(
            ['testproject.view_pipeline', 'testproject.change_pipeline',
             'testproject.delete_pipeline'], pipeline))
        # backend group
        self.assertTrue(julius.has_perms(
            ['testproject.view_pipeline', 'testproject.change_pipeline'], pipeline))
        self.assertFalse(julius.has_perm('testproject.delete_pipeline', pipeline))
        # watcher group
        self.assertTrue(jack.has_perm('testproject.view_pipeline', pipeline))
        self.assertFalse(jack.has_perm('testproject.change_pipeline', pipeline))
        self.assertFalse(jack.has_perm('testproject.delete_pipeline', pipeline))
        # frontend group
        self.assertFalse(teresa.has_perm('testproject.view_pipeline', pipeline))
        self.assertFalse(teresa.has_perm('testproject.change_pipeline', pipeline))
        self.assertFalse(teresa.has_perm('testproject.delete_pipeline', pipeline))
        # owner
        self.assertTrue(john.has_perms(
            ['testproject.view_pipeline', 'testproject.change_pipeline',
             'testproject.delete_pipeline'], pipeline))
