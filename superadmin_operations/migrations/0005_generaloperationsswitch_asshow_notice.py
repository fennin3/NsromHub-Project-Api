# Generated by Django 3.2.2 on 2021-11-05 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin_operations', '0004_rename_show_notice_generaloperationsswitch_acshow_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='generaloperationsswitch',
            name='asshow_notice',
            field=models.BooleanField(default=False),
        ),
    ]
