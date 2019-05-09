# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-09 16:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=20)),
                ('semester', models.CharField(choices=[('Primavera', 'Primavera'), ('Oto\xf1o', 'Oto\xf1o')], default='Primavera', max_length=15)),
                ('section', models.IntegerField(choices=[(1, 1), (2, 2)], default=1)),
                ('year', models.CharField(default='2019', max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Ingrese el(los) nombre(s) del estudiante (Ej: Juan Pedro)', max_length=100)),
                ('family_name', models.CharField(help_text='Ingrese el(los) apellido(s) del estudiante (Ej: P\xe9rez Gonz\xe1lez)', max_length=100)),
            ],
            options={
                'ordering': ['family_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Ingrese el nombre del equipo (Ej: ReAL Soluciones)', max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
            options={
                'ordering': ['course', 'name'],
            },
        ),
        migrations.AddField(
            model_name='student',
            name='team',
            field=models.ManyToManyField(help_text='Seleccione un equipo para el estudiante', to='courses.Team'),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('code', 'section', 'year', 'semester')]),
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together=set([('first_name', 'family_name')]),
        ),
    ]
