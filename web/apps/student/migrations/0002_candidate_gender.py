# Generated by Django 3.1 on 2024-07-10 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='gender',
            field=models.PositiveBigIntegerField(blank=True, choices=[(0, 'Masculino'), (1, 'Femenino'), (2, 'Otro')], null=True, verbose_name='Genero'),
        ),
    ]
