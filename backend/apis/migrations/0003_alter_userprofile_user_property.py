# Generated by Django 4.1.1 on 2022-09-22 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apis", "0002_userprofile_is_audit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="user_property",
            field=models.JSONField(default=list),
        ),
    ]
