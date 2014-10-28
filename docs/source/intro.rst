Installation
============

First of all, install the repository master version with ``pip``::

   pip install https://github.com/vittoriozamboni/django-groups-manager/archive/master.zip

Add ``groups_manager`` to installed apps::
   
   INSTALLED_APPS += (
       'groups_manager',
   )

If you want to use standard templates, add groups_manager's urls from ``urls.py``::

	urlpatterns = ('',
		# ...
		url(r'^groups-manager/', include('groups_manager.urls', namespace='groups_manager')),
		# ...
	)

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

