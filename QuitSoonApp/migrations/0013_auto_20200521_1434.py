# Generated by Django 3.0.5 on 2020-05-21 12:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('QuitSoonApp', '0012_auto_20200521_1109'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='alternative',
            unique_together={('user', 'type_alternative', 'substitut', 'nicotine'), ('user', 'type_alternative', 'alternative')},
        ),
    ]
