# Generated by Django 3.1.7 on 2021-03-06 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210306_0500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='userid',
            new_name='system_id_for_user',
        ),
    ]
