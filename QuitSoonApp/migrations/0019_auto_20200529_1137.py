# Generated by Django 3.0.5 on 2020-05-29 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuitSoonApp', '0018_auto_20200521_1933'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consoalternative',
            old_name='duration',
            new_name='activity_duration',
        ),
        migrations.AddField(
            model_name='consoalternative',
            name='ecig_choice',
            field=models.CharField(choices=[('V', 'Vape ecig today'), ('S', 'Start new bottle'), ('VS', 'Vape and start bottle')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='paquet',
            name='type_cig',
            field=models.CharField(choices=[('IND', 'Cigarettes industrielles'), ('ROL', 'Cigarettes roulées'), ('CIGARES', 'Cigares'), ('PIPE', 'Pipe'), ('NB', 'Autres(en nb/paquet)'), ('GR', 'Autres(en g/paquet)')], default='IND', max_length=8),
        ),
    ]