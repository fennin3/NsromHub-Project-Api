# Generated by Django 3.2.2 on 2021-10-30 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constituent_operations', '0002_incidentreport_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestform',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
