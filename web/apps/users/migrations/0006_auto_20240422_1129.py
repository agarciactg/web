# Generated by Django 3.1 on 2024-04-22 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20240422_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='document_number',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='Numero de Documento'),
        ),
    ]
