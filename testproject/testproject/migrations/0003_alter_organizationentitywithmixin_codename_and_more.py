# Generated by Django 4.2.1 on 2023-06-14 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):
    dependencies = [
        ("groups_manager", "0008_1_3_0_jsonfield_from_django"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("testproject", "0002_organizationgroupmemberwithmixin_expiration_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizationentitywithmixin",
            name="codename",
            field=models.SlugField(
                blank=True, max_length=255, unique=True, verbose_name="codename"
            ),
        ),
        migrations.AlterField(
            model_name="organizationentitywithmixin",
            name="label",
            field=models.CharField(max_length=255, verbose_name="label"),
        ),
        migrations.AlterField(
            model_name="organizationgroupmemberwithmixin",
            name="roles",
            field=models.ManyToManyField(
                blank=True, to="testproject.organizationmemberrolewithmixin"
            ),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="city",
            field=models.CharField(blank=True, default="", max_length=200),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="codename",
            field=models.SlugField(blank=True, max_length=255, verbose_name="codename"),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="comment",
            field=models.TextField(blank=True, default="", verbose_name="comment"),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="description",
            field=models.TextField(blank=True, default="", verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="django_auth_sync",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="full_name",
            field=models.CharField(
                blank=True, default="", max_length=255, verbose_name="full name"
            ),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="group_entities",
            field=models.ManyToManyField(
                blank=True,
                related_name="%(app_label)s_%(class)s_set",
                to="testproject.organizationentitywithmixin",
            ),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="group_members",
            field=models.ManyToManyField(
                related_name="%(app_label)s_%(class)s_set",
                through="testproject.OrganizationGroupMemberWithMixin",
                to="testproject.organizationmemberwithmixin",
            ),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="group_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(app_label)s_%(class)s_set",
                to="groups_manager.grouptype",
            ),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="level",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="lft",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="name",
            field=models.CharField(max_length=255, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sub_%(app_label)s_%(class)s_set",
                to="testproject.organizationgroupwithmixin",
                verbose_name="parent",
            ),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="properties",
            field=models.JSONField(blank=True, default=dict, verbose_name="properties"),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="rght",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="organizationgroupwithmixin",
            name="short_name",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
        migrations.AlterField(
            model_name="organizationmemberrolewithmixin",
            name="codename",
            field=models.SlugField(
                blank=True, max_length=255, unique=True, verbose_name="codename"
            ),
        ),
        migrations.AlterField(
            model_name="organizationmemberrolewithmixin",
            name="label",
            field=models.CharField(max_length=255, verbose_name="label"),
        ),
        migrations.AlterField(
            model_name="organizationmemberwithmixin",
            name="django_auth_sync",
            field=models.BooleanField(
                blank=True, default=True, verbose_name="django auth sync"
            ),
        ),
        migrations.AlterField(
            model_name="organizationmemberwithmixin",
            name="django_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(app_label)s_%(class)s_set",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="organizationmemberwithmixin",
            name="email",
            field=models.EmailField(
                blank=True, default="", max_length=255, verbose_name="email"
            ),
        ),
        migrations.AlterField(
            model_name="organizationmemberwithmixin",
            name="first_name",
            field=models.CharField(max_length=255, verbose_name="first name"),
        ),
        migrations.AlterField(
            model_name="organizationmemberwithmixin",
            name="last_name",
            field=models.CharField(max_length=255, verbose_name="last name"),
        ),
        migrations.AlterField(
            model_name="organizationmemberwithmixin",
            name="username",
            field=models.CharField(
                blank=True, default="", max_length=255, verbose_name="username"
            ),
        ),
        migrations.AlterField(
            model_name="organizationtypewithmixin",
            name="codename",
            field=models.SlugField(
                blank=True, max_length=255, unique=True, verbose_name="codename"
            ),
        ),
        migrations.AlterField(
            model_name="organizationtypewithmixin",
            name="label",
            field=models.CharField(max_length=255, verbose_name="label"),
        ),
    ]
