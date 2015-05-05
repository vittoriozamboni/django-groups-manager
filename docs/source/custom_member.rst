.. _custom-member-model:

Custom member model
-------------------

By default, ``Group``'s attribute ``members`` returns a list of ``Member`` instances.
If you want to create also a custom Member model in addition to custom Group, maybe you
want to obtain a list of custom Member model instances with ``members`` attribute.
This can be obtained with ``GroupsManagerMeta``'s ``member_model`` attribute. This class
must be defined in Group subclass/proxy.
The value of the attribute is in ``<application>.<model_name>`` form.

**1) Define models in models.py**::

    from groups_manager.models import Group, Member

    class Organization(Group):
    
        class GroupsModelMeta:
            model_name = 'myApp.OrganizationMember'
    

    class OrganizationMember(Member):
        pass

**2) Call Organization members attribute**::

    org_a = Organization.objects.create(name='Org, Inc.')
    boss = OrganizationMember.objects.create(first_name='John', last_name='Boss')
    org_a.add_member(boss)
    org_members = org_a.members  # [<OrganizationMember: John Boss>]


.. note::
 A tested example is available in repository source code, ``testproject``'s ``tests.py`` under
 ``test_proxy_model_custom_member`` and ``test_subclassed_model_custom_member`` methods.