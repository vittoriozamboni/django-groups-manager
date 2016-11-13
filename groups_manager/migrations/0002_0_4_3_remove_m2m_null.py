# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_entities',
            field=models.ManyToManyField(related_name='groups', to='groups_manager.GroupEntity', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='roles',
            field=models.ManyToManyField(to='groups_manager.GroupMemberRole', blank=True),
            preserve_default=True,
        ),
    ]
