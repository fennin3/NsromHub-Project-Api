# Generated by Django 3.2.2 on 2021-10-24 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp_operations', '0002_comment_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=5000),
        ),
    ]
