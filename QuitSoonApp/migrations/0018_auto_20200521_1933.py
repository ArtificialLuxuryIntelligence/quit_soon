# Generated by Django 3.0.5 on 2020-05-21 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuitSoonApp', '0017_auto_20200521_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='alternative',
            name='type_activity',
            field=models.CharField(choices=[('Sp', 'Sport'), ('Lo', 'Loisir'), ('So', 'Soin')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='alternative',
            name='activity',
            field=models.CharField(max_length=200, null=True),
        ),
    ]