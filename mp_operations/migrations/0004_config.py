# Generated by Django 3.2.2 on 2021-10-31 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp_operations', '0003_alter_comment_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=50)),
            ],
        ),
    ]
