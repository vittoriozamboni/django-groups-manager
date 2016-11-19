# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('groups_manager', '0002_0_4_3_remove_m2m_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_entities',
            field=models.ManyToManyField(related_name='groups_manager_group_set', to='groups_manager.GroupEntity', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='group_members',
            field=models.ManyToManyField(related_name='groups_manager_group_set', through='groups_manager.GroupMember', to='groups_manager.Member'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='group_type',
            field=models.ForeignKey(related_name='groups_manager_group_set', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='groups_manager.GroupType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='sub_groups_manager_group_set', blank=True, to='groups_manager.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='django_user',
            field=models.ForeignKey(related_name='groups_manager_member_set', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
