# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import mptt.fields
import groups_manager.models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('groups_manager', '0003_0_5_0_rename_reverse_relations_with_vars'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudPlatform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'permissions': (('view_cloudplatform', 'View Cloud Platform'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ITObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'permissions': (('view_itobject', 'View IT Object'), ('manage_itobject', 'Manage IT Object')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Legion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'permissions': (('view_legion', 'View Legion'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'permissions': (('view_match', 'View match'), ('play_match', 'Play match')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'permissions': (('view_newsletter', 'View Newsletter'), ('send_newsletter', 'Send Newsletter')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationEntityWithMixin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('codename', models.SlugField(unique=True, max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationGroupMemberWithMixin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ('group', 'member'),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationGroupWithMixin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('codename', models.SlugField(max_length=255, blank=True)),
                ('description', models.TextField(default=b'', blank=True)),
                ('comment', models.TextField(default=b'', blank=True)),
                ('full_name', models.CharField(default=b'', max_length=255, blank=True)),
                ('properties', jsonfield.fields.JSONField(default={}, blank=True)),
                ('django_auth_sync', models.BooleanField(default=True)),
                ('last_edit_date', models.DateTimeField(auto_now=True, null=True)),
                ('short_name', models.CharField(default=b'', max_length=50, blank=True)),
                ('city', models.CharField(default=b'', max_length=200, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
            bases=(groups_manager.models.GroupRelationsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrganizationMemberRoleWithMixin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('codename', models.SlugField(unique=True, max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationMemberSubclass',
            fields=[
                ('member_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='groups_manager.Member')),
                ('phone_number', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('last_name', 'first_name'),
                'abstract': False,
            },
            bases=('groups_manager.member',),
        ),
        migrations.CreateModel(
            name='OrganizationMemberWithMixin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('username', models.CharField(default=b'', max_length=255, blank=True)),
                ('email', models.EmailField(default=b'', max_length=255, blank=True)),
                ('django_auth_sync', models.BooleanField(default=True)),
                ('last_edit_date', models.DateTimeField(auto_now=True, null=True)),
                ('django_user', models.ForeignKey(related_name='testproject_organizationmemberwithmixin_set', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('last_name', 'first_name'),
                'abstract': False,
            },
            bases=(groups_manager.models.MemberRelationsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrganizationSubclass',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='groups_manager.Group')),
                ('address', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
            bases=('groups_manager.group',),
        ),
        migrations.CreateModel(
            name='OrganizationTypeWithMixin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('codename', models.SlugField(unique=True, max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'permissions': (('view_pipeline', 'View Pipeline'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectGroup',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='groups_manager.Group')),
            ],
            options={
                'permissions': (('view_projectgroup', 'View Project Group'),),
            },
            bases=('groups_manager.group',),
        ),
        migrations.CreateModel(
            name='ProjectGroupMember',
            fields=[
                ('groupmember_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='groups_manager.GroupMember')),
            ],
            options={
                'ordering': ('group', 'member'),
                'abstract': False,
            },
            bases=('groups_manager.groupmember',),
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('member_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='groups_manager.Member')),
            ],
            options={
                'permissions': (('view_projectmember', 'View Project Member'),),
            },
            bases=('groups_manager.member',),
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'permissions': (('view_site', 'View site'), ('sell_site', 'Sell site')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SurfaceProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'permissions': (('view_surfaceproduct', 'View Surface Product'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamBudget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('euros', models.IntegerField()),
            ],
            options={
                'permissions': (('view_teambudget', 'View team budget'),),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='organizationgroupwithmixin',
            name='django_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='auth.Group', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizationgroupwithmixin',
            name='group_entities',
            field=models.ManyToManyField(related_name='testproject_organizationgroupwithmixin_set', null=True, to='testproject.OrganizationEntityWithMixin', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizationgroupwithmixin',
            name='group_members',
            field=models.ManyToManyField(related_name='testproject_organizationgroupwithmixin_set', through='testproject.OrganizationGroupMemberWithMixin', to='testproject.OrganizationMemberWithMixin'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizationgroupwithmixin',
            name='group_type',
            field=models.ForeignKey(related_name='testproject_organizationgroupwithmixin_set', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='groups_manager.GroupType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizationgroupwithmixin',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='sub_testproject_organizationgroupwithmixin_set', blank=True, to='testproject.OrganizationGroupWithMixin', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizationgroupmemberwithmixin',
            name='group',
            field=models.ForeignKey(related_name='group_membership', to='testproject.OrganizationGroupWithMixin'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizationgroupmemberwithmixin',
            name='member',
            field=models.ForeignKey(related_name='group_membership', to='testproject.OrganizationMemberWithMixin'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizationgroupmemberwithmixin',
            name='roles',
            field=models.ManyToManyField(to='testproject.OrganizationMemberRoleWithMixin', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='away',
            field=models.ForeignKey(related_name='match_away', to='groups_manager.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='home',
            field=models.ForeignKey(related_name='match_home', to='groups_manager.Group'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('groups_manager.group',),
        ),
        migrations.CreateModel(
            name='OrganizationMember',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('groups_manager.member',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('groups_manager.group',),
        ),
        migrations.CreateModel(
            name='WorkGroup',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('groups_manager.group',),
        ),
    ]
