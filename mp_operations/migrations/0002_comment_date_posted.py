
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp_operations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
