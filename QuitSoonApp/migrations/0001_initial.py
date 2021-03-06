# Generated by Django 3.0.5 on 2020-05-13 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alternative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_alternative', models.CharField(choices=[('Sp', 'Sport'), ('Lo', 'Loisir'), ('So', 'Soin'), ('Su', 'Substitut')], default='Sp', max_length=200)),
                ('alternative', models.CharField(max_length=200)),
                ('nicotine', models.FloatField(null=True)),
            ],
            options={
                'unique_together': {('type_alternative', 'alternative', 'nicotine')},
            },
        ),
        migrations.CreateModel(
            name='Paquet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_cig', models.CharField(choices=[('IND', 'Cigarettes industrielles'), ('ROL', 'Cigarettes roulées'), ('CIGARES', 'Cigares'), ('CIGARIOS', 'Cigarios'), ('PIPE', 'Pipe'), ('NB', 'Autres(en nb/paquet)'), ('GR', 'Autres(en g/paquet)')], default='IND', max_length=8)),
                ('brand', models.CharField(max_length=200)),
                ('qt_paquet', models.IntegerField(default=20)),
                ('unit', models.CharField(choices=[('U', 'Unités'), ('G', 'Grammes')], default='U', max_length=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('g_per_cig', models.DecimalField(decimal_places=1, max_digits=3)),
                ('display', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('starting_nb_cig', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Objectif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qt', models.IntegerField(unique=True)),
                ('datetime_creation', models.DateTimeField()),
                ('datetime_objectif', models.DateTimeField()),
                ('respected', models.BooleanField(default=False)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuitSoonApp.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='ConsoCig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_cig', models.DateField()),
                ('time_cig', models.TimeField()),
                ('given', models.BooleanField(default=False)),
                ('id_paquet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='QuitSoonApp.Paquet')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuitSoonApp.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='ConsoAlternative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_alter', models.DateField()),
                ('time_alter', models.TimeField()),
                ('duree', models.IntegerField(null=True)),
                ('id_alter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuitSoonApp.Alternative')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuitSoonApp.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Trophee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_cig', models.IntegerField()),
                ('nb_jour', models.IntegerField()),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuitSoonApp.UserProfile')),
            ],
            options={
                'unique_together': {('nb_cig', 'nb_jour')},
            },
        ),
    ]
