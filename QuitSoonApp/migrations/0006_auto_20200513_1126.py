# Generated by Django 3.0.5 on 2020-05-13 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuitSoonApp', '0005_auto_20200513_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paquet',
            name='g_per_cig',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True),
        ),
    ]
