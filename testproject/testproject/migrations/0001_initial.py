# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups_manager', '0002_auto_20160317_1325'),
    ]

    operations = [
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
            name='OrganizationMemberSubclass',
            fields=[
                ('member_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='groups_manager.Member')),
                ('phone_number', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=('groups_manager.member',),
        ),
        migrations.CreateModel(
            name='OrganizationSubclass',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='groups_manager.Group')),
                ('address', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('groups_manager.group',),
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
