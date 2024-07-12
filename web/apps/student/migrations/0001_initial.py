# Generated by Django 3.1 on 2024-07-10 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Activo'), (2, 'Inactivo')], default=1, verbose_name='Estado')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha Actualizado')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('place_of_bird', models.CharField(max_length=350, verbose_name='Lugar de nacimiento')),
                ('date_of_bird', models.DateField(verbose_name='Fecha de nacimiento')),
                ('years', models.IntegerField(verbose_name='edad')),
                ('laterality', models.PositiveBigIntegerField(choices=[(0, 'Izquierdo'), (1, 'Diestro'), (2, 'Ambidiestro')], verbose_name='Lateralidad')),
                ('degrees', models.PositiveSmallIntegerField(choices=[(1, 'Primero'), (2, 'Segundo'), (3, 'Tercero'), (4, 'Cuarto'), (5, 'Quinto'), (6, 'Sexto'), (7, 'Septimo'), (8, 'Octavo'), (9, 'Noveno'), (10, 'Decimo'), (11, 'Once')], help_text='Grado educativo', verbose_name='Grado')),
                ('elective_year', models.IntegerField(verbose_name='Anio electivo')),
                ('address', models.CharField(max_length=350, verbose_name='Direccion')),
                ('city', models.CharField(max_length=350, verbose_name='ciudad')),
                ('neighborhood', models.CharField(max_length=350, verbose_name='Barrio')),
                ('stratum', models.IntegerField(verbose_name='Estrato')),
                ('phone', models.CharField(blank=True, max_length=350, null=True, verbose_name='Telefono')),
                ('email', models.CharField(max_length=350, verbose_name='Correo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='candidate_user', to=settings.AUTH_USER_MODEL, verbose_name='usuario')),
            ],
            options={
                'verbose_name': 'Candidato',
                'verbose_name_plural': 'Candidatos',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Activo'), (2, 'Inactivo')], default=1, verbose_name='Estado')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha Actualizado')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('candiate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='student.candidate', verbose_name='Candidato')),
            ],
            options={
                'verbose_name': 'Estudiante',
                'verbose_name_plural': 'Estudiantes',
                'ordering': ['-id'],
            },
        ),
    ]
