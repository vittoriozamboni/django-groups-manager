Django auth models integration
==============================

It is possibile to auto-map ``Group`` and ``Member`` instances with ``django.contrib.auth.models`` ``Group`` and ``User``.
To enable mapping, ``"AUTH_MODELS_SYNC"`` setting must be set to ``True`` (default: ``False``), and also ``Group`` and ``Member`` instances attribute ``django_auth_sync`` (that is ``True`` by default).

Add to your ``settings`` file::

	
	GROUPS_MANAGER = {
	    'AUTH_MODELS_SYNC': True,
	}

This will generate auth's groups and users each time a new groups_manager's group or member is created.
In addition, every time a groups_manager's ``GroupMember`` instance is generated (either via instance creation or via ``Group``'s ``add_member`` method), the django user is added to django group.
