Installation
============

First of all, install the latest build with ``pip``::

   pip install django-groups-manager

or the repository master version for latest updates::

   pip install https://github.com/vittoriozamboni/django-groups-manager/archive/master.zip

Add ``groups_manager`` to installed apps::
   
   INSTALLED_APPS += (
       'groups_manager',
   )

Run ``syncdb`` or ``migrate``::

   python manage.py migrate

If you are upgrading from version <0.4.2, fake the initial migration::

   python manage.py migrate groups_manager 0001 --fake

If you want to use standard templates, add groups_manager's urls from ``urls.py``::

    urlpatterns = ('',
        # ...
        url(r'^groups-manager/', include('groups_manager.urls', namespace='groups_manager')),
        # ...
    )

Supported templates are based on bootstrap3, and ``django-bootstrap3`` application is required::

    pip install django-bootstrap3

If you don't want to use bootstrap3, you can override forms (see ``Templates`` documentation).

Basic usage
===========

A simple use case for this application is the tracking of customers groups. Each *organization* can have more than one *division*, and a *member* can be in more than one::

    from groups_manager.models import Group, GroupType, Member
	
    # Create group types (optional)
    organization = models.GroupType.objects.create(label='Organization')
    division = models.GroupType.objects.create(label='Division')

    # Organization A has 'commercials' and 'managers'
    org_a = Group.objects.create(name='Org A, Inc.', group_type=organization)
    org_a_commercials = Group.objects.create(name='Commercials', group_type=division, parent=org_a)
    org_a_managers = Group.objects.create(name='Managers', group_type=division, parent=org_a)
    # Tina is a commercial
    tina = Member.objects.create(first_name='Tina', last_name='Rossi')
    org_a_commercials.add_member(tina)
    # Jack is a manager
    jack = Member.objects.create(first_name='Jack', last_name='Black')
    org_a_managers.add_member(jack)

    #Assign objects to members or groups
    product = Product.objects.create(name='Fancy product')  # Product has 'sell_product' permission
    tina.assign_object(org_a_commercials, product)
    tina.has_perm('sell_product', product)  # True
    jack.has_perm('sell_product', product)  # False
    budget = Budget.objects.create(name='Facilities', amount=5000)  #  has 'use_budget' permission
    org_a_managers.assign_object(budget)
    tina.has_perm('use_budget', budget)  # False
    jack.has_perm('use_budget', budget)  # True
