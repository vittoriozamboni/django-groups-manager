# Generated by Django 4.2.1 on 2023-06-13 13:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "groups_manager",
            "0007_1_2_0_alter_group_group_entities_alter_group_group_members_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="properties",
            field=models.JSONField(blank=True, default=dict, verbose_name="properties"),
        ),
    ]
