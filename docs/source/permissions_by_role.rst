.. _custom-permissions-by-role:

Resource assignment via role permissions
----------------------------------------

John Money is the commercial referent of the company; Patrick Html is the web
developer. The company has only one group, but different roles.
John can view and sell the site, and Patrick can view, change and delete the site.

**1) Define models in models.py**::

    class Site(Group):
        name = models.CharField(max_length=100)
    
        class Meta:
            permissions = (('view_site', 'View site'),
                           ('sell_site', 'Sell site'), )

**2) Create models and relations**::

    from groups_manager.models import Group, GroupMemberRole, Member
    from models import Site
    # Group
    company = Group.objects.create(name='Company')
    # Group Member roles
    commercial_referent = GroupMemberRole.objects.create(label='Commercial referent')
    web_developer = GroupMemberRole.objects.create(label='Web developer')
    # Members
    john = Member.objects.create(first_name='John', last_name='Money')
    patrick = Member.objects.create(first_name='Patrick', last_name='Html')
    # Add to company
    company.add_member(john, [commercial_referent])
    company.add_member(patrick, [web_developer])
    # Create the site
    site = Site.objects.create(name='Django groups manager website')

**3) Define custom permissions and assign the site object**::

    custom_permissions = {
        'owner': {'commercial-referent': ['sell_site'],
                  'web-developer': ['change', 'delete'],
                  'default': ['view']},
        'group': ['view'],
        'groups_upstream': ['view', 'change', 'delete'],
        'groups_downstream': ['view'],
        'groups_siblings': ['view'],
    }
    john.assign_object(company, site, custom_permissions=custom_permissions)
    patrick.assign_object(company, site, custom_permissions=custom_permissions)

**4) Check permissions**::

    john.has_perms(['view_site', 'sell_site'], site)  # True
    john.has_perm('change_site', site)  # False
    patrick.has_perms(['view_site', 'change_site', 'delete_site'], site)  # True
    patrick.has_perm('sell_site', site)  # False

.. note::
 The full tested example is available in repository source code, ``testproject``'s ``tests.py`` under ``test_roles`` method.