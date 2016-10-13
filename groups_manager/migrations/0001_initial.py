# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import mptt.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('codename', models.SlugField(max_length=255, blank=True)),
                ('description', models.TextField(default=b'', blank=True)),
                ('comment', models.TextField(default=b'', blank=True)),
                ('full_name', models.CharField(default=b'', max_length=255, blank=True)),
                ('properties', jsonfield.fields.JSONField(default={}, blank=True)),
                ('django_auth_sync', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('django_group', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='auth.Group', null=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('codename', models.SlugField(unique=True, max_length=255, blank=True)),
            ],
            options={
                'ordering': ('label',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(related_name='group_membership', to='groups_manager.Group')),
            ],
            options={
                'ordering': ('group', 'member'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupMemberRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('codename', models.SlugField(unique=True, max_length=255, blank=True)),
            ],
            options={
                'ordering': ('label',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('codename', models.SlugField(unique=True, max_length=255, blank=True)),
            ],
            options={
                'ordering': ('label',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('username', models.CharField(default=b'', max_length=255, blank=True)),
                ('email', models.EmailField(default=b'', max_length=255, blank=True)),
                ('django_auth_sync', models.BooleanField(default=True)),
                ('django_user', models.ForeignKey(related_name='groups_manager_member', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('last_name', 'first_name'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='member',
            field=models.ForeignKey(related_name='group_membership', to='groups_manager.Member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupmember',
            name='roles',
            field=models.ManyToManyField(to='groups_manager.GroupMemberRole', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='groupmember',
            unique_together=set([('group', 'member')]),
        ),
        migrations.AddField(
            model_name='group',
            name='group_entities',
            field=models.ManyToManyField(related_name='groups', null=True, to='groups_manager.GroupEntity', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='group_members',
            field=models.ManyToManyField(related_name='groups', through='groups_manager.GroupMember', to='groups_manager.Member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='group_type',
            field=models.ForeignKey(related_name='groups', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='groups_manager.GroupType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='subgroups', blank=True, to='groups_manager.Group', null=True),
            preserve_default=True,
        ),
    ]
