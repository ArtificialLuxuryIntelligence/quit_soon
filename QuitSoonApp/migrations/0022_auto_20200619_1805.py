# Generated by Django 3.0.5 on 2020-06-19 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuitSoonApp', '0021_paquet_first'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alternative',
            name='substitut',
            field=models.CharField(choices=[('P', 'Patchs'), ('PAST', 'Pastilles'), ('GM', 'Gommes à mâcher'), ('GS', 'Gommes à sucer'), ('CS', 'Comprimés sublinguaux'), ('ECIG', 'Cigarette éléctronique')], max_length=4, null=True),
        ),
    ]
