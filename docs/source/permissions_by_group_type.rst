.. _custom-permissions-by-group-type:

Resource assignment via group type permissions
----------------------------------------

Permissions can also be applied to related groups filtered by group types.
Instead of simply using a list to specify permissions one can use a ``dict`` to
specify which group types get which permissions.


Example
#######


John Money is the commercial referent of the company; Patrick Html is the web
developer. John and Patrick can view the site, but only Patrick can change and
delete it.

**1) Define models in models.py**::

    class Site(Group):
        name = models.CharField(max_length=100)

        class Meta:
            permissions = (('view_site', 'View site'),
                           ('sell_site', 'Sell site'), )

**2) Create models and relations**::

    from groups_manager.models import Group, GroupType, Member
    from models import Site

    # Parent Group
    company = Group.objects.create(name='Company')

    # Group Types
    developer = GroupType.objects.create(label='developer')
    referent = GroupType.objects.create(label='referent')

    # Child groups
    developers = Group.objects.create(name='Developers', group_type=developer, parent=company)
    referents = Group.objects.create(name='Referents', group_type=referent, parent=company)

    # Members
    john = Member.objects.create(first_name='John', last_name='Money')
    patrick = Member.objects.create(first_name='Patrick', last_name='Html')

    # Add to groups
    referents.add_member(john)
    developers.add_member(patrick)

    # Create the site
    site = Site.objects.create(name='Django groups manager website')

**3) Define custom permissions and assign the site object**::

    custom_permissions = {
        'owner': [],
        'group': ['view'],
        'groups_downstream': {'developer': ['change', 'delete'], 'default': ['view']},
    }
    john.assign_object(company, site, custom_permissions=custom_permissions)

**4) Check permissions**::

    john.has_perm('view_site', site)  # True
    john.has_perm('change_site', site)  # False
    john.has_perm('delete_site', site)  # False
    patrick.has_perms(['view_site', 'change_site', 'delete_site'], site)  # True

.. note::
 The full tested example is available in repository source code, ``testproject``'s ``tests.py`` under ``test_group_types_permissions`` method.
