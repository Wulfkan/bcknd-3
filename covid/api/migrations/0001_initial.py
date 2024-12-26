# Generated by Django 5.1.4 on 2024-12-23 01:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Examen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FichaMedica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='medico', to=settings.AUTH_USER_MODEL)),
                ('especialidades', models.ManyToManyField(blank=True, to='api.especialidad')),
            ],
        ),
        migrations.CreateModel(
            name='Atencion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_atencion', models.DateTimeField(auto_now_add=True)),
                ('anamnesis', models.TextField()),
                ('diagnostico', models.TextField()),
                ('medico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='atenciones', to='api.doctor')),
                ('examenes', models.ManyToManyField(blank=True, related_name='atenciones', to='api.examen')),
                ('ficha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atenciones', to='api.fichamedica')),
                ('medicamentos', models.ManyToManyField(blank=True, related_name='atenciones', to='api.medicamento')),
            ],
        ),
        migrations.AddField(
            model_name='fichamedica',
            name='paciente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ficha', to='api.paciente'),
        ),
    ]
