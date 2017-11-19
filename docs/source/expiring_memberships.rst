Expiring memberships
-------------------------------------

Members can be added to groups with an (optional) date that specifies when the
membership expires.

.. note::
 The ``expiration_date`` is only a field that is used to indicate when the
 membership expires. How this is used is up to the user of the library. For
 example to filter out expired memberships or periodically delete them.

**Set expiration date to one week from today** ::

    import datetime
    from django.utils import timezone

    john = models.Member.objects.create(first_name='John', last_name='Boss')
    expiration = timezone.now() + datetime.timedelta(days=7)
    project_main.add_member(john, expiration_date=expiration)
