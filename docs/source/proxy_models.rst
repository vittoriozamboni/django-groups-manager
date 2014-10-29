Projects management with Proxy Models
-------------------------------------

John Boss is the project leader. Marcus Worker and Julius Backend are the
django backend guys; Teresa Html is the front-end developer and Jack College is the
student that has to learn to write good backends.
The Celery pipeline is owned by Marcus, and Jack must see it without intercations.
Teresa can't see the pipeline, but John has full permissions as project leader.
As part of the backend group, Julius has the right of viewing and editing, but not to
stop (delete) the pipeline.

**1) Define models in models.py**::

    from groups_manager.models import Group, GroupType

    class Project(Group):
        # objects = ProjectManager()
    
        class Meta:
            proxy = True
    
        def save(self, *args, **kwargs):
            if not self.group_type:
                self.group_type = GroupType.objects.get_or_create(label='Project')[0]
            super(Project, self).save(*args, **kwargs)

    class WorkGroup(Group):
        # objects = WorkGroupManager()
    
        class Meta:
            proxy = True
    
        def save(self, *args, **kwargs):
            if not self.group_type:
                self.group_type = GroupType.objects.get_or_create(label='Workgroup')[0]
            super(WorkGroup, self).save(*args, **kwargs)

    class Pipeline(models.Model):
        name = models.CharField(max_length=100)
    
        class Meta:
            permissions = (('view_pipeline', 'View Pipeline'), )

.. warning::
 Remember to define a ``view_modelname`` permission.
	
**2) Connect creation and deletion signals to the proxy models**
*(This step is required if you want to sync with django auth models)*::

    from django.db.models.signals import post_save, post_delete
    from groups_manager.models import group_save, group_delete

    post_save.connect(group_save, sender=Project)
    post_delete.connect(group_delete, sender=Project)
    post_save.connect(group_save, sender=WorkGroup)
    post_delete.connect(group_delete, sender=WorkGroup)


**3) Creates groups**::

    project_main = testproject_models.Project(name='Workgroups Main Project')
    project_main.save()
    django_backend = testproject_models.WorkGroup(name='WorkGroup Backend', parent=project_main)
    django_backend.save()
    django_backend_watchers = testproject_models.WorkGroup(name='Backend Watchers',
                                                        parent=django_backend)
    django_backend_watchers.save()
    django_frontend = testproject_models.WorkGroup(name='WorkGroup FrontEnd', parent=project_main)
    django_frontend.save()

**4) Creates members and assign them to groups**::

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

**5) Create the pipeline and assign custom permissions**::

    custom_permissions = {
        'owner': ['view', 'change', 'delete'],
        'group': ['view', 'change'],
        'groups_upstream': ['view', 'change', 'delete'],
        'groups_downstream': ['view'],
        'groups_siblings': [],
    }
    pipeline = testproject_models.Pipeline.objects.create(name='Test Runner')
    marcus.assing_object(django_backend, pipeline, custom_permissions=custom_permissions)


.. note::
 The full tested example is available in repository source code, ``testproject``'s ``tests.py`` under ``test_proxy_models`` method.