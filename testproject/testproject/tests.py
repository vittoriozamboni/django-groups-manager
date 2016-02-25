import re

from django.test import TestCase

from groups_manager import models
from testproject import models as testproject_models

GROUPS_MANAGER_MOCK = {
    'AUTH_MODELS_SYNC': True,
    'GROUP_NAME_PREFIX': '',
    'GROUP_NAME_SUFFIX': '',
    'USER_USERNAME_PREFIX': '',
    'USER_USERNAME_SUFFIX': '',
    'PERMISSIONS': {
        'owner': ['view', 'change', 'delete'],
        'group': ['view', 'change'],
        'groups_upstream': ['view'],
        'groups_downstream': [],
        'groups_siblings': ['view'],
    },
}

random_end = re.compile(r'.*_[a-z0-9]{8}$')


class TestPermissions(TestCase):

    def setUp(self):
        pass

    def create_legions(self):
        """
        Sulla owns one Legion. There are three groups:
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
        """
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
        relation.assign_object(legio_4)

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
            'owner': ['view', 'change', 'delete'],
            'group': ['view', 'change', 'delete'],
            'groups_upstream': ['view', 'change', 'delete'],
            'groups_downstream': ['view', 'change', 'delete'],
            'groups_siblings': ['view', 'change', 'delete'],
        }
        legio_4 = testproject_models.Legion(name='Legio IV')
        legio_4.save()
        legio_5 = testproject_models.Legion(name='Legio V')
        legio_5.save()
        relation = models.GroupMember.objects.get(group=self.consuls, member=self.sulla)
        relation.assign_object(legio_4, custom_permissions=custom_permissions)

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

    def test_roles(self):
        """
        John and Patrick are member of the group. John is the commercial referent,
        and Patrick is the web developer. John can sell the site, but only Patrcik can change it.
        Standard permissions for owners are based on global roles.
        """
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        custom_permissions = {
            'owner': {'commercial-referent': ['sell_site'],
                      'web-developer': ['change', 'delete'],
                      'default': ['view']},
            'group': ['view'],
            'groups_upstream': ['view', 'change', 'delete'],
            'groups_downstream': ['view'],
            'groups_siblings': ['view'],
        }
        company = models.Group.objects.create(name='Company')
        commercial_referent = models.GroupMemberRole.objects.create(label='Commercial referent')
        web_developer = models.GroupMemberRole.objects.create(label='Web developer')
        john = models.Member.objects.create(first_name='John', last_name='Money')
        patrick = models.Member.objects.create(first_name='Patrick', last_name='Html')
        company.add_member(john, [commercial_referent])
        company.add_member(patrick, [web_developer])
        site = testproject_models.Site.objects.create(name='Django groups manager website')
        john.assign_object(company, site, custom_permissions=custom_permissions)
        patrick.assign_object(company, site, custom_permissions=custom_permissions)
        self.assertTrue(john.has_perms(['view_site', 'sell_site'], site))
        self.assertFalse(john.has_perm('change_site', site))
        self.assertFalse(john.has_perm('delete_site', site))
        self.assertTrue(patrick.has_perms(['view_site', 'change_site', 'delete_site'], site))
        self.assertFalse(patrick.has_perm('sell_site', site))

    def test_football_match(self):
        """
        Thohir is the president of FC Internazionale, and Palacio is a team player.
        Thohir organize a friendly match against FC Barcelona. Palacio can play the match, but
        Thohir can't. In the same way, Thohir can change the FC Internazionale budget, but
        Palacio can't.
        """
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        custom_permissions = {
            'owner': ['view', 'change', 'delete'],
            'group': ['view', 'change'],
            'groups_upstream': ['view', 'change', 'delete'],
            'groups_downstream': ['view'],
            'groups_siblings': ['view'],
        }
        fc_internazionale = models.Group.objects.create(name='F.C. Internazionale Milan')
        staff = models.Group.objects.create(name='Staff', parent=fc_internazionale)
        players = models.Group.objects.create(name='Players', parent=fc_internazionale)
        thohir = models.Member.objects.create(first_name='Eric', last_name='Thohir')
        staff.add_member(thohir)
        palacio = models.Member.objects.create(first_name='Rodrigo', last_name='Palacio')
        players.add_member(palacio)
        # test budget
        small_budget = testproject_models.TeamBudget.objects.create(euros='1000')
        thohir.assign_object(staff, small_budget)
        self.assertTrue(thohir.has_perm('change_teambudget', small_budget))
        self.assertFalse(palacio.has_perm('change_teambudget', small_budget))
        # test match
        fc_barcelona = models.Group.objects.create(name='FC Barcelona')
        friendly_match = testproject_models.Match.objects.create(
            home=fc_internazionale, away=fc_barcelona)
        palacio.assign_object(players, friendly_match,
            custom_permissions={'owner': ['play_match'], 'group': ['play_match']})
        self.assertFalse(thohir.has_perm('play_match', friendly_match))
        self.assertTrue(palacio.has_perm('play_match', friendly_match))

    def test_group_permissions(self):
        """
        On company IT Stars, Mike is the sys admin and Juliet is the marketing manager.
        Of course, Mike can administrate infrastructures (Juliet can't),
        and Juliet can create newsletters, and Mike too (tech newsletters!).
        """
        from groups_manager import settings
        settings.GROUPS_MANAGER = GROUPS_MANAGER_MOCK
        it_stars = models.Group.objects.create(name='IT stars')
        sys_admins = models.Group.objects.create(name='Sys Admins', parent=it_stars)
        marketing = models.Group.objects.create(name='Marketing', parent=it_stars)
        mike = models.Member.objects.create(first_name='Mike', last_name='Sys')
        sys_admins.add_member(mike)
        juliet = models.Member.objects.create(first_name='Juliet', last_name='Marks')
        marketing.add_member(juliet)
        sysadmins_permissions = {'group': ['manage_itobject']}
        newsletter_permissions = {'group': ['send_newsletter'],
                                  'groups_siblings': ['send_newsletter']}
        # test sysadmins
        pc1 = testproject_models.ITObject.objects.create(name='PC 1')
        sys_admins.assign_object(pc1, custom_permissions=sysadmins_permissions)
        self.assertTrue(mike.has_perm('manage_itobject', pc1))
        self.assertFalse(juliet.has_perm('manage_itobject', pc1))
        # test newsletters
        newsletter_tech = testproject_models.Newsletter.objects.create(name='Tech news')
        marketing.assign_object(newsletter_tech, custom_permissions=newsletter_permissions)
        self.assertTrue(mike.has_perm('send_newsletter', newsletter_tech))
        self.assertTrue(juliet.has_perm('send_newsletter', newsletter_tech))

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
            'owner': ['view', 'change', 'delete'],
            'group': ['view', 'change'],
            'groups_upstream': ['view', 'change', 'delete'],
            'groups_downstream': ['view'],
            'groups_siblings': [],
        }
        project_main = testproject_models.Project.objects.create(name='Workgroups Main Project')
        django_backend = testproject_models.WorkGroup.objects.create(
            name='WorkGroup Backend', parent=project_main)
        django_backend_watchers = testproject_models.WorkGroup.objects.create(
            name='Backend Watchers', parent=django_backend)
        django_frontend = testproject_models.WorkGroup.objects.create(
            name='WorkGroup FrontEnd', parent=project_main)
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
        marcus.assign_object(django_backend, pipeline, custom_permissions=custom_permissions)

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

    def test_proxy_model_custom_member(self):
        organization = testproject_models.Organization.objects.create(name='Awesome Org, Inc.')
        john_boss = testproject_models.OrganizationMember.objects.create(
            first_name='John', last_name='Boss')
        organization.add_member(john_boss)
        org_members = organization.members
        self.assertIsInstance(org_members[0], testproject_models.OrganizationMember)

    def test_subclassed_model_custom_member(self):
        organization = testproject_models.OrganizationSubclass.objects.create(
            name='Awesome Org, Inc.', address='First Street')
        john_boss = testproject_models.OrganizationMemberSubclass.objects.create(
            first_name='John', last_name='Boss', phone_number='033 32 33 34')
        organization.add_member(john_boss)
        org_members = organization.members
        self.assertIsInstance(org_members[0], testproject_models.OrganizationMemberSubclass)
