# Generated by Django 3.0.5 on 2020-06-24 17:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('QuitSoonApp', '0023_auto_20200620_2344'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trophee',
            unique_together={('user', 'nb_cig', 'nb_jour')},
        ),
    ]
